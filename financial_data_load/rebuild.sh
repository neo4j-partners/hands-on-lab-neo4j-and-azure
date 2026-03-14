#!/usr/bin/env bash
# Rebuild the knowledge graph from backup with entity resolution.
#
# Prereqs: backup exists (uv run python main.py backup)
#
# This script is idempotent — safe to re-run at any time.
# It restores from backup, so the database returns to a clean
# post-PDF-processing state before each run.

set -e
cd "$(dirname "$0")"

echo "============================================"
echo "Rebuilding knowledge graph"
echo "============================================"
echo ""

echo ">>> Step 1: Restore database from backup"
uv run python main.py restore
echo ""

echo ">>> Step 2: Export entity snapshot"
uv run python main.py snapshot
echo ""

echo ">>> Step 3: Run entity resolution (prefix, threshold=0.3)"
uv run python main.py resolve --strategy prefix --threshold 0.3
echo ""

echo ">>> Step 4: Apply merge plan"
uv run python main.py apply-merges
echo ""

echo ">>> Step 5: Finalize (constraints, indexes, asset managers)"
uv run python main.py finalize
echo ""

echo ">>> Step 6: Verify"
uv run python main.py verify
echo ""

echo "============================================"
echo "Rebuild complete"
echo "============================================"
