#!/bin/bash
set -e
mkdir -p ~/bones-forge/cloudflare-workers/_private
cp ~/bones-forge/cloudflare-workers/heuremen-door/worker.js ~/bones-forge/cloudflare-workers/_private/heuremen-door-worker-source-20261114.js
cp ~/bones-forge/cloudflare-workers/heuremen-door/wrangler.toml ~/bones-forge/cloudflare-workers/_private/heuremen-door-wrangler-20261114.toml
cp ~/bones-forge/field-runs/worker-clean/build/worker.js ~/bones-forge/cloudflare-workers/heuremen-door/worker.js
cp ~/bones-forge/field-runs/worker-clean/build/wrangler.toml ~/bones-forge/cloudflare-workers/heuremen-door/wrangler.toml
rm -f ~/bones-forge/cloudflare-workers/heuremen-door/worker_public.js ~/bones-forge/cloudflare-workers/heuremen-door/wrangler_public.toml
echo installed
