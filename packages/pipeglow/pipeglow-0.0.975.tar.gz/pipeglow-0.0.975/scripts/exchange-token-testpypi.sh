#!/bin/bash

# 🦊✨ Retrieve the OIDC token from GitLab CI/CD, and exchange it for a PyPI API token
oidc_token=$(python -m id PYPI)

# 🪙🥺  Make the request to mint a new PyPI token
resp=$(curl -X POST -s -w '\n%{http_code}' https://test.pypi.org/_/oidc/mint-token \
  -d "{\"token\":\"${oidc_token}\"}")

# 🔬⛽️  Extract the status code and response body
status=$(echo "$resp" | tail -n1)
body=$(echo "$resp" | head -n -1)

# 🔭🥺 Check request status
if [ "$status" != "200" ]; then 
  echo "❎😭  Error: API returned status $status"
  echo "$body" | jq 'del(.token)'
  exit 1
fi

# 🔬🪙  Extract the API token
api_token=$(echo "$body" | jq --raw-output '.token')
echo "🚀✨ Successfully retrieved API token."

# 🚀✨ Upload to TestPyPI
uvx twine upload -u __token__ --repository testpypi -p "${api_token}" dist/*
