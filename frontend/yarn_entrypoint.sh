#!/bin/sh
set -e

# 1. Build al
yarn build

# 2. Output'u volume ile paylaşılan klasöre kopyala
mkdir -p /app/frontend/out
cp -r /app/out/* /app/frontend/out/

# 3. Sunucu başlat
exec node watch-build.js