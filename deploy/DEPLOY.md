# IMT Icons 배포 (2026-09-02 적용 완료)

## 현재 상태
| 경로 | 상태 |
|---|---|
| GitHub | https://github.com/imaketoo-david/imt-icons (public, tag `v3.0.0`) |
| jsDelivr CDN | `https://cdn.jsdelivr.net/gh/imaketoo-david/imt-icons@3/...` ✅ |
| 자체 호스팅 | https://icons.imaketoo.com ✅ |
| 맥미니 파일 | `/Users/songsmac-mini/Documents/Project/imt-icons` |

## 1. GitHub 갱신
```bash
cd ~/Documents/Project/_workspace-mini/imt-icons
git add -A && git commit -m "..." && git push
git tag -f v3.x.x && git push -f origin v3.x.x    # CDN @3 은 v3 최신을 따라감
```

## 2. 맥미니 갱신 (아이콘 추가/수정 후)
```bash
rsync -az --delete --exclude .git --exclude .gitignore \
  ~/Documents/Project/_workspace-mini/imt-icons/ \
  mini-ts:~/Documents/Project/imt-icons/
```
Caddy·터널 설정은 그대로라 reload 불필요. 브라우저 캐시(max-age 7일)만 유의.

## 3. 인프라 구성 (이미 적용됨 — 참고용)
**Caddy** `/opt/homebrew/etc/Caddyfile` (PM2 `caddy`) → `deploy/caddy-icons.conf` 블록
백업: `/opt/homebrew/etc/Caddyfile.bak_icons_20260902`

**cloudflared** 메인 터널 `~/.cloudflared/config.yml` (`8c6f4998-4448-4850-9e94-8ff40d01e17d`)
```yaml
  - hostname: icons.imaketoo.com
    service: http://127.0.0.1:8080
```
백업: `~/.cloudflared/config.yml.bak_icons_20260902`
DNS: `cloudflared tunnel route dns 8c6f4998-... icons.imaketoo.com` (CNAME 생성 완료)
재시작: `launchctl kickstart -k gui/$(id -u)/com.imaketoo.cloudflared.ppomppu`

## 4. 사용 시 주의 — `<use href>` 는 동일 출처에서만 동작
브라우저 보안 정책상 `<svg><use href="https://다른도메인/sprite.svg#i-x">` 는 **렌더링되지 않습니다.**

| 상황 | 방법 |
|---|---|
| 단일 HTML 산출물 (대시보드·리포트·카드뉴스) | `icons/glyph/<name>.svg` 인라인 복붙 |
| 사이트에 sprite.svg 동봉 | `<use href="/static/sprite.svg#i-chart-line">` |
| CDN·타 도메인에서 바로 | **웹폰트** — CORS 열려 있음 |
| 동적 주입 | `fetch(url).then(r=>r.text()).then(t=>document.body.insertAdjacentHTML('afterbegin',t))` |

웹폰트 예시:
```html
<link rel="stylesheet" href="https://icons.imaketoo.com/font/imt-icons.css">
<i class="imt imt-chart-line"></i>
```

## 5. 검증 명령
```bash
for p in /catalog.html /sprite.svg /icons.json /font/imt-icons.woff2 /icons/glyph/chart-line.svg; do
  printf "%-34s " "$p"; curl -s -o /dev/null -w "%{http_code}\n" "https://icons.imaketoo.com$p"
done
```
