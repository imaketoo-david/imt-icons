#!/usr/bin/env bash
# IMT Icons 배포 — 빌드 → 커밋·푸시 → 맥미니 전송 → 라이브 확인
# 사용: ./deploy.sh ["커밋 메시지"]
set -euo pipefail
cd "$(dirname "$0")"
HOST="${IMT_HOST:-mini-ts}"
DEST="/Users/songsmac-mini/Documents/Project/imt-icons/"
SITE="https://icons.imaketoo.com"

echo "▸ 1. 빌드"
./build.sh | tail -4

echo "▸ 2. 커밋·푸시"
if [[ -n "$(git status --porcelain)" ]]; then
  git add -A
  git commit -q -m "${1:-배포 $(date '+%Y-%m-%d %H:%M')}"
fi
git push -q origin main
echo "  $(git log --oneline -1)"

echo "▸ 3. 맥미니 전송 (${HOST})"
rsync -a --delete \
  --exclude '.git' --exclude 'src' --exclude 'build.sh' --exclude 'deploy.sh' \
  --exclude '__pycache__' --exclude '*.bak_*' \
  ./ "${HOST}:${DEST}"

echo "▸ 4. 라이브 확인"
B="$(date +%s)"
printf "  catalog.html -> %s\n" "$(curl -s -o /dev/null -w '%{http_code}' "${SITE}/catalog.html?b=${B}")"
printf "  아이콘 수     -> %s\n" "$(curl -s "${SITE}/icons.json?b=${B}" | python3 -c 'import json,sys;d=json.load(sys.stdin);print(len(d.get("icons",d)))')"
printf "  웹폰트 글리프 -> %s\n" "$(curl -s "${SITE}/font/codepoints.json?b=${B}" | python3 -c 'import json,sys;print(len(json.load(sys.stdin)))')"
printf "  신규 확인     -> %s\n" "$(curl -s "${SITE}/sprite.svg?b=${B}" | grep -o 'id="i-\(undo\|redo\|share\|paste\|check-circle\|thumbs-up\|thumbs-down\|sort\|text-search\)"' | wc -l | tr -d ' ')"
echo "완료."
