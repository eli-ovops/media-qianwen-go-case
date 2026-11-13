#!/bin/zsh
set -e
cd "$(dirname "$0")"
/Users/USER/.local/nodejs/node-v22.16.0-darwin-arm64/bin/node node_modules/@remotion/cli/remotion-cli.js render src/index.ts QianwenGoV1 ../output/candidate-v1.mp4 --codec=h264 --crf=18 --concurrency=1 --gl=swangle --browser-executable='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' --overwrite=false
