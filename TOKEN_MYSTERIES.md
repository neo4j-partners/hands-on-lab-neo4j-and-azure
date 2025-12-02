# Rate Limiting Mystery Investigation

## The Problem
Running workshop solutions in `hands-on-lab-neo4j-and-azure` consistently hits rate limits:
```
RateLimitError: Rate limit exceeded: Error code: 429 - {'error': {'code': '429', 'message': 'Rate limit is exceeded. Try again in 60 seconds.'}}
```

Meanwhile, the identical code in `neo4j-azure-workshop` runs fine.

## Investigation Summary

### What I Checked

| Configuration | hands-on-lab (broken) | neo4j-azure-workshop (working) |
|---------------|----------------------|-------------------------------|
| Azure OpenAI Resource | `aoai-h6ezr4kekiria` | `aoai-3vdwyzccdn4v6` |
| Resource Group | `rg-test-lower-limits` | `rg-token-count` |
| gpt-4o-mini Capacity | 5 TPM | 5 TPM |
| text-embedding-ada-002 Capacity | 5 TPM | 5 TPM |
| SKU | GlobalStandard | GlobalStandard |
| Model Version | Same | Same |
| Bicep Config | Identical | Identical |
| Region | eastus2 | eastus2 |
| Subscription | Same | Same |

### What's Identical
- All Azure deployment configurations (main.bicep, cognitiveservices.bicep)
- Model versions and SKUs
- Deployment capacities (both 5 TPM)
- API call patterns in code
- Same subscription and region

### What's Different
1. **Different Azure OpenAI resources** - Each project deploys its own
2. **Different Neo4j databases** - Different data sets
3. **Different resource group names** (suspicious: `rg-test-lower-limits`)
4. **Token tracking code** - Working project has `TrackedLLM`/`TrackedEmbeddings` wrappers (but these only log, no rate limiting logic)

### Live API Test Results
Both endpoints respond successfully to single curl requests:
```
# Non-working endpoint
HTTP: 200 (worked)

# Working endpoint
HTTP: 200 (worked)
```

## The Unsolved Mystery

Despite identical configurations, the `aoai-h6ezr4kekiria` resource hits rate limits while `aoai-3vdwyzccdn4v6` does not. Single API calls work fine; the issue manifests only under workshop load.

### Possible Explanations (Not Confirmed)

1. **Hidden Azure-side throttling** - Azure AI Foundry may have project-level or resource-level quotas beyond what's visible in the CLI

2. **Timing/state issue** - The `rg-test-lower-limits` resource may have accumulated rate limit "debt" from previous heavy usage

3. **Global quota competition** - With GlobalStandard SKU, quota is pooled globally; other deployments in the subscription could be consuming capacity

4. **Resource group naming prophecy** - The name `rg-test-lower-limits` might have been chosen because this resource consistently behaves as if it has lower limits

## Useful Tools

The `neo4j-azure-workshop` project has a helpful quota checking script at:
```
/Users/ryanknight/projects/workshops/neo4j-azure-workshop/check_azure_quota.sh
```

This script shows:
- All Azure OpenAI resources across the subscription
- Model deployments and their capacity
- Regional quota usage
- Role assignments

## Recommendations

1. **Try deleting and recreating** the Azure resource group `rg-test-lower-limits` completely (not just redeploying)

2. **Point this project to the working resource** by updating `.env`:
   ```
   AZURE_OPENAI_ENDPOINT=https://aoai-3vdwyzccdn4v6.openai.azure.com/
   AZURE_AI_PROJECT_ENDPOINT=https://aoai-3vdwyzccdn4v6.services.ai.azure.com/api/projects/proj-3vdwyzccdn4v6
   AZURE_RESOURCE_GROUP=rg-token-count
   ```

3. **Increase capacity** in both projects' `infra/core/ai/cognitiveservices.bicep` (line 128) from 5 to 20

4. **Check Azure Portal** for any rate limiting alerts or quotas specific to the problematic resource

5. **Contact Azure Support** - If the mystery persists, there may be hidden state on the Azure side

---
*Investigation conducted: 2025-12-01*
