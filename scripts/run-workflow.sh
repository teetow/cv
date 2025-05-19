#!/bin/bash

cd "$(dirname "$0")/.." || exit

WORKFLOW_FILE=".github/workflows/github-pages.yml"

echo "Running GitHub Actions workflow locally with Act..."
echo "Using workflow file: $WORKFLOW_FILE"

./bin/act --workflows $WORKFLOW_FILE "$@" --bind --env ACT=true
