#!/bin/sh
set -eu

PRECOMMIT_CONFIG=".pre-commit-config.yaml"
WORKFLOW_CONFIG=".github/workflows/check.yml"

# get Python version from .pre-commit-config.yaml
PRECOMMIT_VERSION=$(
  yq eval \
  '.default_language_version.python | sub("^python", "")' \
  "$PRECOMMIT_CONFIG"
)

# get Python version from .github/workflows/check.yml
WORKFLOW_VERSION=$(
  yq eval \
  '.jobs.check.steps[] | select(.uses == "actions/setup-python@*") | .with.python-version' \
  "$WORKFLOW_CONFIG"
)

# Compare the versions
if [ "$PRECOMMIT_VERSION" != "$WORKFLOW_VERSION" ]; then
  printf '%s\n' \
    "Python version mismatch:" \
    "${PRECOMMIT_CONFIG} = ${PRECOMMIT_VERSION}" \
    "${WORKFLOW_CONFIG} = ${WORKFLOW_VERSION}" \
    >&2
  exit 1
fi

exit 0
