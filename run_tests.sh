#!/usr/bin/env bash
# Automate test suite: activate venv, run pytest, return 0/1.
# Usage: ./run_tests.sh

set -u  # treat unset vars as errors

echo "🔹 Locating virtual environment…"
# Prefer .venv, fallback to venv
if [ -f ".venv/bin/activate" ]; then
  VENV_PATH=".venv/bin/activate"
elif [ -f "venv/bin/activate" ]; then
  VENV_PATH="venv/bin/activate"
else
  echo "⚠️  No virtual environment found (.venv/ or venv/)."
  echo "    Continuing without activation (system Python will be used)…"
  VENV_PATH=""
fi

# Activate if available
if [ -n "${VENV_PATH}" ]; then
  # shellcheck disable=SC1090
  source "${VENV_PATH}"
  echo "✅ Activated venv: ${VENV_PATH}"
fi

echo "🔹 Running tests with pytest…"
pytest
status=$?

if [ $status -eq 0 ]; then
  echo "✅ All tests passed."
  exit 0
else
  echo "❌ Tests failed. Exit code: $status"
  exit 1
fi
