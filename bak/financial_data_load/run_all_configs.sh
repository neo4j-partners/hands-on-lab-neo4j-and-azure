#!/usr/bin/env bash
# Run all 10 entity resolution configs and compare results.
# Usage: ./run_all_configs.sh
#
# Prereqs: snapshot already exists (uv run python main.py snapshot)

set -e
cd "$(dirname "$0")"

echo "============================================"
echo "Running 10 entity resolution configs"
echo "============================================"
echo ""

# --- Group A: Vary fuzzy threshold (binary mode) ---

echo ">>> Config 1: baseline (fuzzy, threshold=0.6, binary)"
uv run python main.py resolve --strategy fuzzy --threshold 0.6 --confidence binary
echo ""

echo ">>> Config 2: wide-net (fuzzy, threshold=0.5, binary)"
uv run python main.py resolve --strategy fuzzy --threshold 0.5 --confidence binary
echo ""

echo ">>> Config 3: tight-filter (fuzzy, threshold=0.7, binary)"
uv run python main.py resolve --strategy fuzzy --threshold 0.7 --confidence binary
echo ""

echo ">>> Config 4: very-wide (fuzzy, threshold=0.4, binary)"
uv run python main.py resolve --strategy fuzzy --threshold 0.4 --confidence binary
echo ""

# --- Group B: Scored confidence mode (fuzzy strategy) ---

echo ">>> Config 5: scored-standard (fuzzy, threshold=0.6, scored@0.8)"
uv run python main.py resolve --strategy fuzzy --threshold 0.6 --confidence scored --confidence-threshold 0.8
echo ""

echo ">>> Config 6: scored-strict (fuzzy, threshold=0.6, scored@0.9)"
uv run python main.py resolve --strategy fuzzy --threshold 0.6 --confidence scored --confidence-threshold 0.9
echo ""

echo ">>> Config 7: wide-scored (fuzzy, threshold=0.5, scored@0.8)"
uv run python main.py resolve --strategy fuzzy --threshold 0.5 --confidence scored --confidence-threshold 0.8
echo ""

# --- Group C: Prefix strategy ---

echo ">>> Config 8: prefix-loose (prefix, threshold=0.3, binary)"
uv run python main.py resolve --strategy prefix --threshold 0.3 --confidence binary
echo ""

echo ">>> Config 9: prefix-standard (prefix, threshold=0.5, binary)"
uv run python main.py resolve --strategy prefix --threshold 0.5 --confidence binary
echo ""

# --- Group D: Structural limit ---

echo ">>> Config 10: small-groups (fuzzy, threshold=0.6, binary, max-group=5)"
uv run python main.py resolve --strategy fuzzy --threshold 0.6 --confidence binary --max-group-size 5
echo ""

# --- Compare all runs ---

echo "============================================"
echo "Comparing all runs"
echo "============================================"
uv run python main.py compare
