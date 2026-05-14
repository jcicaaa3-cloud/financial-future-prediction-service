# GitHub Pages Live Lab 설명

이 버전의 목적은 리뷰어가 설치 없이 바로 만져볼 수 있는 포트폴리오 체험면을 만드는 것입니다.

## 브라우저에서 가능한 것

- 샘플 회사 선택
- 재무 지표 슬라이더 조정
- Growth upside / Margin shock / Liquidity crunch / Market stress / Disclosure event 시나리오 적용
- 리스크 스코어와 설명 즉시 확인
- decision packet JSON 복사 및 다운로드
- 여러 회사 batch scoring
- CSV 붙여넣기 또는 업로드 후 브라우저 내 scoring
- cURL 요청 예시 복사

## 정적 사이트와 백엔드의 역할 분리

GitHub Pages는 정적 파일을 배포하는 구조라 FastAPI 서버를 직접 실행하지 않습니다. 따라서 `site/app.js`는 synthetic sample과 설명 가능한 heuristic scoring을 사용합니다.

실제 백엔드 파이프라인은 다음 파일들에서 실행됩니다.

```text
app/main.py
src/financial_risk_scoring/
run_demo.py
scripts/build_portfolio_snapshot.py
```

## 배포 체크포인트

GitHub 저장소에서 다음 설정을 확인합니다.

```text
Settings → Pages → Build and deployment → Source → GitHub Actions
```

그리고 workflow는 `site/` 디렉터리를 artifact로 업로드합니다.

```text
.github/workflows/pages.yml
site/index.html
site/app.js
site/styles.css
```

혹시 Pages가 README만 보여주면 branch deploy 모드로 잡혀 있을 가능성이 있습니다. 이 V6에는 root `index.html` fallback도 들어 있어서, branch/root 모드에서도 최소한 interactive lab이 열리도록 보완했습니다.
