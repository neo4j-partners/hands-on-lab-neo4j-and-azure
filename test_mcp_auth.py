"""
Test Neo4j Aura MCP server OAuth flows and output Databricks configuration.

Flow:
1. Register an OAuth client via Auth0 dynamic registration
2. Run OAuth Authorization Code + PKCE flow (opens browser)
3. Test the MCP endpoint with the user token
4. Print Databricks configuration values

Key finding: The audience parameter must be OMITTED from the authorization
request. Auth0 then defaults to audience=https://console.neo4j.io, which
is what the MCP server validates against.
"""

import base64
import hashlib
import http.server
import json
import os
import secrets
import sys
import urllib.error
import urllib.parse
import urllib.request
import webbrowser

# OAuth endpoints (discovered from https://mcp.neo4j.io/.well-known/oauth-authorization-server)
AUTH0_ISSUER = "https://aura-mcp.eu.auth0.com"
AUTHORIZATION_ENDPOINT = f"{AUTH0_ISSUER}/authorize"
TOKEN_ENDPOINT = f"{AUTH0_ISSUER}/oauth/token"
REGISTRATION_ENDPOINT = f"{AUTH0_ISSUER}/oidc/register"
SCOPES = "openid profile email"

LOCAL_PORT = 8976
REDIRECT_URI = f"http://localhost:{LOCAL_PORT}/callback"


def load_env(path):
    """Load .env file into a dict."""
    env = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            key, _, value = line.partition("=")
            env[key.strip()] = value.strip().strip('"')
    return env


def register_oauth_client(redirect_uri=None):
    """Register a client via Auth0 dynamic client registration."""
    uri = redirect_uri or REDIRECT_URI
    payload = json.dumps({
        "client_name": "neo4j-mcp-databricks-test",
        "redirect_uris": [uri],
        "grant_types": ["authorization_code"],
        "response_types": ["code"],
        "token_endpoint_auth_method": "none",
    }).encode()

    req = urllib.request.Request(
        REGISTRATION_ENDPOINT,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    print("1. Registering OAuth client via dynamic registration ...")
    print(f"   Redirect URI: {uri}")
    try:
        with urllib.request.urlopen(req) as resp:
            body = json.loads(resp.read())
            client_id = body["client_id"]
            client_secret = body.get("client_secret", "")
            print(f"   SUCCESS")
            print(f"   Client ID:     {client_id}")
            if client_secret:
                print(f"   Client Secret: {client_secret}")
            return client_id, client_secret
    except urllib.error.HTTPError as e:
        print(f"   FAILED - {e.code} {e.reason}")
        print(f"   {e.read().decode()}")
        return None, None


def generate_pkce():
    """Generate PKCE code_verifier and code_challenge."""
    verifier = secrets.token_urlsafe(43)
    challenge = base64.urlsafe_b64encode(
        hashlib.sha256(verifier.encode()).digest()
    ).rstrip(b"=").decode()
    return verifier, challenge


def do_oauth_flow(client_id):
    """Run OAuth Authorization Code + PKCE flow with local callback server.

    IMPORTANT: Do NOT set the 'audience' parameter. Auth0 defaults to
    audience=https://console.neo4j.io, which the MCP server requires.
    Setting audience explicitly (e.g. to Auth0's /api/v2/) produces a
    token the MCP server rejects with 401.
    """
    code_verifier, code_challenge = generate_pkce()
    state = secrets.token_urlsafe(16)

    # Build authorization URL — NO audience parameter
    auth_params = urllib.parse.urlencode({
        "client_id": client_id,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": SCOPES,
        "state": state,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
        # audience is intentionally omitted — Auth0 defaults to
        # https://console.neo4j.io which the MCP server expects
    })
    auth_url = f"{AUTHORIZATION_ENDPOINT}?{auth_params}"

    # Capture the authorization code via local HTTP server
    result = {"code": None, "error": None}

    class CallbackHandler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            parsed = urllib.parse.urlparse(self.path)
            params = urllib.parse.parse_qs(parsed.query)

            if "code" in params:
                result["code"] = params["code"][0]
                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.end_headers()
                self.wfile.write(
                    b"<h2>Authorization successful!</h2>"
                    b"<p>You can close this tab and return to the terminal.</p>"
                )
            else:
                result["error"] = params.get("error", ["unknown"])[0]
                self.send_response(400)
                self.send_header("Content-Type", "text/html")
                self.end_headers()
                self.wfile.write(f"<h2>Error: {result['error']}</h2>".encode())

        def log_message(self, format, *args):
            pass  # Suppress server logs

    server = http.server.HTTPServer(("localhost", LOCAL_PORT), CallbackHandler)

    print(f"\n2. Starting OAuth Authorization Code + PKCE flow ...")
    print(f"   Opening browser for Neo4j Aura login ...")
    print(f"   (Log in with your Aura Console credentials)\n")

    # Open browser in background
    webbrowser.open(auth_url)

    # Wait for callback (single request)
    server.handle_request()
    server.server_close()

    if result["error"]:
        print(f"   FAILED - OAuth error: {result['error']}")
        return None

    if not result["code"]:
        print(f"   FAILED - No authorization code received")
        return None

    print(f"   Got authorization code, exchanging for token ...")

    # Exchange code for token
    token_data = urllib.parse.urlencode({
        "grant_type": "authorization_code",
        "client_id": client_id,
        "code": result["code"],
        "redirect_uri": REDIRECT_URI,
        "code_verifier": code_verifier,
    }).encode()

    req = urllib.request.Request(
        TOKEN_ENDPOINT,
        data=token_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req) as resp:
            body = json.loads(resp.read())
            token = body["access_token"]
            expires = body.get("expires_in", "unknown")
            print(f"   SUCCESS - got user token (expires in {expires}s)")
            print(f"   Token prefix: {token[:30]}...")

            # Decode JWT to show audience (for debugging)
            if token.startswith("eyJ"):
                parts = token.split(".")
                payload_b64 = parts[1] + "=" * (4 - len(parts[1]) % 4)
                decoded = json.loads(base64.urlsafe_b64decode(payload_b64))
                print(f"   Token audience: {decoded.get('aud')}")

            return token
    except urllib.error.HTTPError as e:
        print(f"   FAILED - {e.code} {e.reason}")
        print(f"   {e.read().decode()}")
        return None


def test_mcp_endpoint(mcp_url, token, label="3"):
    """Send MCP initialize request to test auth."""
    payload = json.dumps({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2025-03-26",
            "capabilities": {},
            "clientInfo": {"name": "databricks-auth-test", "version": "1.0.0"},
        },
    }).encode()

    req = urllib.request.Request(
        mcp_url,
        data=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
        },
        method="POST",
    )

    print(f"\n{label}. Testing MCP endpoint with user token ...")
    print(f"   URL: {mcp_url}")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read().decode()
            print(f"   SUCCESS - HTTP {resp.status}")
            print(f"   Response: {body[:500]}")
            return True
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"   FAILED - HTTP {e.code} {e.reason}")
        print(f"   Response: {body[:500]}")
        return False


def print_databricks_config(client_id, client_secret, mcp_url):
    """Print the values to enter in Databricks."""
    print("\n" + "=" * 60)
    print("DATABRICKS CONFIGURATION")
    print("=" * 60)
    print()
    print("Step 1 - Connection basics:")
    print(f"  Connection name:     finance_mcp_server")
    print(f"  Connection type:     HTTP")
    print(f"  Auth type:           OAuth User to Machine Per User")
    print(f"  OAuth provider:      Manual configuration")
    print()
    print("Step 2 - Authentication:")
    print(f"  Host:                https://mcp.neo4j.io")
    print(f"  Port:                443")
    print(f"  OAuth scope:         {SCOPES}")
    print(f"  Client ID:           {client_id}")
    print(f"  Client secret:       {client_secret or '(leave empty - public client)'}")
    print(f"  Authorization endpoint: {AUTHORIZATION_ENDPOINT}")
    print(f"  Token endpoint:      {TOKEN_ENDPOINT}")
    print()
    print("IMPORTANT: Do NOT set an OAuth audience parameter.")
    print("Auth0 must default to audience=https://console.neo4j.io")
    print("for the MCP server to accept the token.")
    print()
    print("MCP Server URL (for Databricks MCP tool config):")
    print(f"  {mcp_url}")
    print()
    print("NOTE: The client_id above was registered with redirect_uri")
    print(f"  {REDIRECT_URI}")
    print("If Databricks uses a different redirect_uri, re-register via:")
    print(f"  POST {REGISTRATION_ENDPOINT}")
    print(f"  Body: {{\"client_name\":\"databricks\",\"redirect_uris\":[\"<DATABRICKS_URI>\"],")
    print(f"         \"grant_types\":[\"authorization_code\"],\"response_types\":[\"code\"],")
    print(f"         \"token_endpoint_auth_method\":\"none\"}}")
    print()


def main():
    env_path = os.path.join(os.path.dirname(__file__), "financial_data_load", ".env")
    print(f"Loading credentials from {env_path}\n")
    env = load_env(env_path)

    mcp_url = env.get("AURA_AGENT_MCP_SERVER")
    if not mcp_url:
        print("ERROR: Missing AURA_AGENT_MCP_SERVER in .env")
        sys.exit(1)

    # Step 1: Register OAuth client
    client_id, client_secret = register_oauth_client()
    if not client_id:
        print("\nCannot proceed without a client ID.")
        sys.exit(1)

    # Step 2: OAuth flow (opens browser)
    token = do_oauth_flow(client_id)
    if not token:
        print("\nCannot proceed without a token.")
        sys.exit(1)

    # Step 3: Test MCP endpoint
    mcp_ok = test_mcp_endpoint(mcp_url, token)

    # Print Databricks config
    print_databricks_config(client_id, client_secret, mcp_url)

    # Summary
    print("=" * 60)
    print("RESULT")
    print("=" * 60)
    if mcp_ok:
        print("  User OAuth token WORKS with MCP endpoint!")
        print("  OAuth User to Machine Per User should work in Databricks.")
    else:
        print("  User OAuth token FAILED with MCP endpoint.")
        print("  Further investigation needed.")


if __name__ == "__main__":
    main()
