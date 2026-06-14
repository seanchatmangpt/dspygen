#!/usr/bin/env bash
set -euo pipefail

# 1. Run tests
make test

# 2. Build
poetry build

# 3. Tag
VERSION="$(poetry version -s)"
git tag -a "v${VERSION}" -m "Release v${VERSION}"

# 4. Push tag
git push origin --tags

echo "Released v${VERSION}"
