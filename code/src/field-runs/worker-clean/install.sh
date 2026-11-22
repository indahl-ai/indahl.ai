#!/bin/bash
set -e
mkdir -p ~/forge/cloudflare-workers/_private
cp ~/forge/cloudflare-workers/heuremen-door/worker.js ~/forge/cloudflare-workers/_private/heuremen-door-worker-source-20261114.js
cp ~/forge/cloudflare-workers/heuremen-door/wrangler.toml ~/forge/cloudflare-workers/_private/heuremen-door-wrangler-20261114.toml
cp ~/forge/field-runs/worker-clean/build/worker.js ~/forge/cloudflare-workers/heuremen-door/worker.js
cp ~/forge/field-runs/worker-clean/build/wrangler.toml ~/forge/cloudflare-workers/heuremen-door/wrangler.toml
rm -f ~/forge/cloudflare-workers/heuremen-door/worker_public.js ~/forge/cloudflare-workers/heuremen-door/wrangler_public.toml
echo installed
