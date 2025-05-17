#!/bin/bash

echo "⏳ Queueing all assassin reskin frames into ComfyUI..."

for json in ./ComfyUI/input/assassin_batch_jsons/*.json; do
  curl -X POST http://127.0.0.1:8188/prompt \
       -H "Content-Type: application/json" \
       -d @"$json"
done

echo "✅ All prompts queued."
