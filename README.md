# IMT Icons v3.0 — imaketoo icon system

아이콘 **324종** · **37 카테고리** (애플 단축어 글리프 카테고리 31종 + IMT 실무 6종).
애플의 **렌더링 원칙**만 따르고, 도형은 전부 좌표로 직접 작성했습니다.

## 왜 "애플스럽지만" 문제가 없는가
애플이 보호하는 대상은 SF Symbols의 **개별 도형(아트워크)** 과 **SF 폰트 파일**이며, 라이선스상 애플 플랫폼 밖에서의 사용·변형이 금지됩니다. 반면 아래는 특정 회사가 독점할 수 없는 **일반적 제도(design convention)** 입니다.

| 채택 (자유롭게 사용 가능) | 배제 (법적 위험) |
|---|---|
| 24pt 그리드, 광학 정렬 | SF Symbols 도형 복제·트레이싱 |
| 균일 스트로크 + round cap/join | SF Symbols / SF Pro 폰트 파일 재배포 |
| 연속곡률(슈퍼타원) 코너 | `sf-symbols` 계열 심볼명 그대로 사용 |
| 단색 스퀴클 배지 + 흰색 글리프 | 애플 제품·기기 실루엣, Apple 로고 |
| iOS 시스템 컬러 "계열" 색상 | 애플 색상 토큰·에셋 추출 |
| 카테고리 분류 체계 | 애플 이모지·아이콘 이미지 |

→ 모든 패스는 `src/icondata.py` 에 좌표로 직접 기술되어 있습니다. 추출·트레이싱 없음.

## 디자인 규격
| 항목 | 값 |
|---|---|
| 캔버스 | 24 × 24 |
| 광학 영역 | 가로 17.6 / 세로 15.6 — 넓고 낮게 |
| 스트로크 | **1.6** 균일, round cap / round join, 굵기 변조 없음 |
| 코너 | 연속곡률 슈퍼타원(n=4), 제어점 계수 0.909 — 원호(0.5523) 아님 |
| 면(fill) | 사용 안 함 (점 표기 `more` 만 예외) |
| 요소 수 | 아이콘당 평균 2~3 패스 |
| 배지 | 512 슈퍼타원(n=5) **단색**, 글리프 52% 흰색 |
| 색상 | 12색 (`icons.json`, `imt-icons.css`) |

**금지 규칙** — 액센트 도트, 표정, 기울기, 그림자, 그라디언트, 두 가지 굵기 혼용, 귀여운 디테일.

## 카테고리 (37)
화살표 · 도형 · 기호 · 텍스트 포맷 · 수학 · 인덱스 · 시간 · 통신 · 연결 · 미디어 ·
카메라 및 사진 · 편집 · 기기 · 키보드 · 홈 · 상업 · 건강 · 자연 · 날씨 · 지도 ·
교통 · 자동차 · 게임 · 피트니스 · 인간 · 사람 · 손쉬운 사용 · 개인정보 보호 및 보안 ·
사물 · 사물 및 도구 · 변수 · **코어 UI · 파일 · 데이터 · 금융 · 개발 · 상태**

## 파일 구성
```
icons/glyph/<name>.svg   24px, currentColor — UI 원본
icons/badge/<name>.svg   512px 단색 스퀴클 배지 — 앱/기능 카드
sprite.svg               <use href="#i-<name>"> 참조용
font/imt-icons.woff2     아이콘 웹폰트 (+ .ttf, .css, codepoints.json)
react/IMTIcon.jsx        <Icon /> · <IconBadge />
imt-icons.css            색상 변수 + 크기 유틸
icons.json               메타데이터 (이름·카테고리·한글 키워드·색상)
catalog.html             검색 카탈로그
src/ + build.sh          재빌드 스크립트
```

## 사용법
**스프라이트** (웹, 가장 가벼움)
```html
<svg class="imt-i"><use href="/icons/sprite.svg#i-chart-line"/></svg>
```
**웹폰트**
```html
<link rel="stylesheet" href="/icons/font/imt-icons.css">
<i class="imt imt-chart-line"></i>
```
**React**
```jsx
import Icon, { IconBadge } from "./IMTIcon";
<Icon name="trend-up" size={20} />
<IconBadge name="portfolio" size={72} />
```

## 확장
`src/icondata.py` 에 `add(name, cat, kw, ops, hue)` 한 줄 추가 → `./build.sh`.
`kw` 에는 반드시 한글 키워드를 넣습니다 (카탈로그·스킬 검색용).
헬퍼: `C(cx,cy,r)` 원 · `SR(x,y,w,h,r)` 연속곡률 사각형 · `DOT(x,y)` 점 · `GEAR()` 기어.
