#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
pip install -q --break-system-packages svgpathtools shapely brotli fonttools 2>/dev/null || true
export IMT_ROOT="$(pwd)"
python3 src/build_svg.py && python3 src/build_font.py && python3 src/build_code.py && python3 src/build_catalog.py
echo "✅ IMT Icons 빌드 완료"
