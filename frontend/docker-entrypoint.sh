#!/bin/sh
set -e

echo "Building frontend..."
yarn build || { echo "Build failed"; exit 1; }
mkdir -p /app/frontend/out
cp -r /app/out/* /app/frontend/out/ || { echo "Copy failed"; ls -l /app/out; exit 1; }

cat > /app/frontend/out/.ready <<EOF
ready
EOF

echo "Frontend ready. Starting app server..."
ls -l /app/frontend/out
exec node watch-build.js