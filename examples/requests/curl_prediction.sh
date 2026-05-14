#!/usr/bin/env bash
set -euo pipefail

curl -X POST http://127.0.0.1:8000/v1/predictions \
  -H "Content-Type: application/json" \
  -d @examples/requests/prediction_request.json
