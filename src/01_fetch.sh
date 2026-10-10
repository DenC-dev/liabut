#!/usr/bin/env bash
# Fetch the upstream datasets at the pinned commits into data/upstream/ (not tracked).
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p data/upstream && cd data/upstream
get() {  # name url commit
  if [ ! -d "$1" ]; then git clone -q "$2" "$1"; fi
  git -C "$1" fetch -q --depth 1 origin "$3" 2>/dev/null || true
  git -C "$1" checkout -q "$3"
}
get lexirumah https://github.com/lessersunda/lexirumah-data.git e10af03128094a19ae62de32c14753869acaddbd
get abvd      https://github.com/lexibank/abvd.git            4a5795e153120172428afed10195811ff5e19c6c
get ids       https://github.com/lexibank/ids.git             bf6c9f8c7d25c15e61e338f3ed29ae46b844c0f8
echo "upstream data ready"
