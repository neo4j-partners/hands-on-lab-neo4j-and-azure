# Screenshots That Need Updating

After the entity resolution rebuild, company names changed from CSV uppercase (e.g., "APPLE INC") to canonical names (e.g., "Apple Inc."). The screenshots below show old entity names and need to be retaken.

## Lab 1 — Aura Setup

### `Lab_1_Aura_Setup/images/apple_query_agent.png`
- **Issue**: Shows `"company_name": "APPLE INC"` in the Cypher template input and `"company": "APPLE INC"` in the output
- **Fix**: Retake after restoring the new backup. Input should show `"Apple Inc."` and output should show `"Apple Inc."`

### `Lab_1_Aura_Setup/images/apple_agent_reasoning.png`
- **Issue**: Shows "APPLE INC" throughout the reasoning output and asset manager list
- **Fix**: Retake with a query using "Apple Inc." as the company name

### `Lab_1_Aura_Setup/images/company_risk_factors.png`
- **Issue**: Shows `"companyName": "PG&E CORP"` with 202 risk factors
- **Fix**: Retake — will now show "PG&E Corporation". Risk factor count may differ after entity resolution.

## Lab 2 — Aura Agents

### `Lab_2_Aura_Agents/images/apple_query_agent.png`
- **Issue**: Same as Lab 1 — shows "APPLE INC" in input and output
- **Fix**: Retake with `"Apple Inc."` as the company_name parameter

### `Lab_2_Aura_Agents/images/apple_agent_reasoning.png`
- **Issue**: Same as Lab 1 — shows "APPLE INC" in reasoning
- **Fix**: Retake with the new canonical name

### `Lab_2_Aura_Agents/images/company_risk_factors.png`
- **Issue**: Same as Lab 1 — shows "PG&E CORP"
- **Fix**: Retake — will now show "PG&E Corporation"

## Lab 1 — Backup File

### `Lab_1_Aura_Setup/data/finance_data.backup`
- **Issue**: Binary Neo4j backup contains old entity names
- **Fix**: After the rebuild pipeline completes on your Aura instance, go to Aura Console → instance → ... menu → Backup & restore → create a new backup and download it. Replace this file.

## How to Retake Screenshots

1. Restore the new `finance_data.backup` to your Aura instance
2. Recreate the Aura Agent from Lab 2 with updated Cypher templates (use canonical names like "Apple Inc.", "NVIDIA Corporation")
3. Run the test queries from Lab 2 README
4. Capture screenshots at the same points documented in the Lab 2 README
5. Copy the updated screenshots to both `Lab_1_Aura_Setup/images/` and `Lab_2_Aura_Agents/images/`
