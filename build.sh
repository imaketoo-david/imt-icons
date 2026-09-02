#!/usr/bin/env bash
# IMT Icons 빌드
#  주의: A && B && C 형태로 묶으면 중간 실패 시 set -e 가 안 걸린다
#        (bash 가 조건문 맥락으로 취급) → 반드시 한 줄에 하나씩 실행한다
set -euo pipefail
cd "$(dirname "$0")"

# 의존성 확인 — 없으면 설치하고, 그래도 없으면 여기서 멈춘다
if ! python3 -c "import svgpathtools, shapely, fontTools, brotli" 2>/dev/null; then
  echo "▸ 의존성 설치"
  python3 -m pip install -q --break-system-packages svgpathtools shapely brotli fonttools \
    || python3 -m pip install -q svgpathtools shapely brotli fonttools
fi
python3 - <<'PY'
import sys
miss=[m for m in ("svgpathtools","shapely","fontTools","brotli") if not __import__("importlib.util",fromlist=["x"]).find_spec(m)]
if miss:
    sys.exit(f"필수 패키지 없음: {', '.join(miss)} — 폰트가 갱신되지 않으므로 중단한다")
PY

export IMT_ROOT="$(pwd)"
python3 src/build_svg.py
python3 src/build_font.py
python3 src/build_code.py
python3 src/build_catalog.py
python3 src/check_css.py || exit 1
echo "✅ IMT Icons 빌드 완료"
