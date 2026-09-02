#!/usr/bin/env bash
# IMT Icons 배포 — 빌드 → 커밋·푸시 → 맥미니 전송 → 라이브 확인
# 사용: ./deploy.sh ["커밋 메시지"]
set -euo pipefail
cd "$(dirname "$0")"
HOST="${IMT_HOST:-mini-ts}"
DEST="/Users/songsmac-mini/Documents/Project/imt-icons/"
# 2026-09-03: design.imaketoo.com/icons/ 로 통합. 폴더와 rsync 목적지는 그대로다
# — Caddy 가 그 폴더를 /icons/ 아래로 붙여 준다(handle_path).
SITE="https://design.imaketoo.com/icons"

echo "▸ 1. 빌드"
./build.sh | tail -4

# design 쪽으로 나가는 링크에 버전을 붙인다 — 브라우저 캐시가 옛 쪽을 붙들지 못하게 (L-0.5)
python3 - <<'PYX'
import re, datetime
v = datetime.datetime.now().strftime("%Y%m%d-%H%M")
s = open("catalog.html", encoding="utf-8").read()
s = re.sub(r'https://design\.imaketoo\.com(/[A-Za-z0-9._/-]*)?(?:\?v=[^"\']*)?(?=["\'])',
           lambda m: f'https://design.imaketoo.com{m.group(1) or "/index.html"}?v={v}', s)
open("catalog.html", "w", encoding="utf-8").write(s)
print(f"  링크 버전 스탬프 v={v}")
PYX

echo "▸ 2. 커밋·푸시"
if [[ -n "$(git status --porcelain)" ]]; then
  git add -A
  git commit -q -m "${1:-배포 $(date '+%Y-%m-%d %H:%M')}"
fi
git push -q origin main 2>/dev/null || echo "  (푸시 건너뜀 — 인증 없음)"
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
