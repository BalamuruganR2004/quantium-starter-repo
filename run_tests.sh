#!/usr/bin/env bash
set -u

echo "🔹 Locating virtual environment…"
if [ -f ".venv/bin/activate" ]; then
  VENV_PATH=".venv/bin/activate"
elif [ -f "venv/bin/activate" ]; then
  VENV_PATH="venv/bin/activate"
else
  echo "⚠️  No virtual environment found."
  VENV_PATH=""
fi

if [ -n "${VENV_PATH}" ]; then
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
