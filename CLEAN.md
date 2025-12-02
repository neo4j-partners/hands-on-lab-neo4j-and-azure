# Cleaning Up Soft-Deleted Azure Resources

Azure Cognitive Services resources are soft-deleted by default and continue to count against quota for up to 48 days. If you're hitting quota limits after deleting resources, you may need to purge soft-deleted resources.

## Find Soft-Deleted Cognitive Services Resources

```bash
az cognitiveservices account list-deleted --subscription <subscription-id>
```

Or to see all in a table format:

```bash
az cognitiveservices account list-deleted -o table
```

## Purge a Soft-Deleted Resource

```bash
az cognitiveservices account purge \
  --name <resource-name> \
  --resource-group <original-resource-group> \
  --location <location> \
  --subscription <subscription-id>
```

## Via Azure Portal

1. Go to Azure Portal
2. Search for "Cognitive Services"
3. Click "Manage deleted resources" in the top menu bar
4. Select the subscription to see all soft-deleted resources
5. Select and purge them

After purging, the quota should be released almost immediately.
