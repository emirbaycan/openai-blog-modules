#!/bin/sh
set -e

echo "Building frontend..."
yarn build
mkdir -p /app/frontend/out
cp -r /app/out/* /app/frontend/out/

# Hazır dosyasını oluştur
cat > /app/frontend/out/.ready <<EOF
ready
EOF

echo "Frontend ready. Starting app server..."
exec node watch-build.js
