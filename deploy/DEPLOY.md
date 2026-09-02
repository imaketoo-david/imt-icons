# IMT Icons 배포

## 1. GitHub (원본 1곳)
```bash
cd ~/Documents/Project/_workspace-mini/imt-icons
gh repo create imaketoo-david/imt-icons --public --source=. --remote=origin --push
git push origin v3.0.0
```
공개 리포로 만들어야 jsDelivr CDN 이 동작합니다. 비공개로 두려면 2번(자체 호스팅)만 사용하세요.

## 2. jsDelivr CDN (설정 0)
푸시 직후 바로 사용 가능합니다.
```
https://cdn.jsdelivr.net/gh/imaketoo-david/imt-icons@3/sprite.svg
https://cdn.jsdelivr.net/gh/imaketoo-david/imt-icons@3/font/imt-icons.css
https://cdn.jsdelivr.net/gh/imaketoo-david/imt-icons@3/icons.json
```
`@3` 은 v3.x 최신을 따라갑니다. 고정하려면 `@v3.0.0`.

## 3. 맥미니 자체 호스팅 (icons.imaketoo.com)
```bash
# 맥북에서 맥미니로 복사
rsync -avz --delete ~/Documents/Project/_workspace-mini/imt-icons/ \
  mini:~/Documents/Project/imt-icons/ --exclude .git

# Caddyfile 에 deploy/caddy-icons.conf 블록 추가 후
ssh mini 'caddy reload --config ~/Documents/Project/Caddyfile'
```
Cloudflare 에 `icons` 서브도메인 레코드(프록시 ON)를 기존 서브도메인과 동일하게 추가해야 합니다.

## 사용 시 주의 — `<use href>` 는 동일 출처에서만 동작
브라우저 보안 정책상 `<svg><use href="https://다른도메인/sprite.svg#i-x">` 는 **렌더링되지 않습니다.**

| 상황 | 방법 |
|---|---|
| 사이트에 sprite.svg 를 함께 배포 | `<use href="/static/sprite.svg#i-chart-line">` ✅ |
| CDN·타 도메인에서 가져다 쓰기 | 웹폰트(`imt-icons.css`) 사용 ✅ (CORS 허용됨) |
| 동적으로 스프라이트 주입 | `fetch(url).then(r=>r.text()).then(t=>document.body.insertAdjacentHTML('afterbegin',t))` ✅ |
| 단일 HTML 산출물 | `icons/glyph/<name>.svg` 를 인라인 복붙 ✅ |
