# GitHub Pages 사이트 구성 가이드

이 저장소는 포트폴리오 리뷰어가 설치 없이 바로 프로젝트를 체험할 수 있도록 `site/` 디렉터리에 정적 데모 사이트를 포함합니다.

## 왜 정적 사이트인가

GitHub Pages는 정적 사이트 호스팅입니다. 따라서 FastAPI 서버를 직접 실행하지 않고, 브라우저 안에서 synthetic sample과 설명 가능한 휴리스틱 scoring으로 decision packet을 생성합니다.

실제 ML 파이프라인은 계속 아래 경로에서 실행합니다.

```text
app/main.py
src/financial_risk_scoring/
run_demo.py
scripts/build_portfolio_snapshot.py
```

## 포함된 사이트 파일

```text
site/index.html       # 랜딩 페이지 + interactive browser demo
site/styles.css      # 반응형 UI 스타일
site/app.js          # synthetic scoring simulator
site/assets/         # README와 공유하는 이미지 자산
.github/workflows/pages.yml
```

## 배포 방법

1. 이 버전을 `main` 브랜치에 push합니다.
2. GitHub 저장소에서 **Settings → Pages**로 이동합니다.
3. **Build and deployment → Source**를 **GitHub Actions**로 설정합니다.
4. Actions 탭에서 **Deploy GitHub Pages live lab** workflow를 실행하거나, `site/**` 변경사항을 push합니다.
5. 배포가 끝나면 아래 주소에서 접속합니다.

```text
https://jcicaaa3-cloud.github.io/financial-future-prediction-service/
```

## 리뷰어에게 보여줄 포인트

- 설치 없이 회사 샘플을 선택하고 risk score를 바로 확인할 수 있음
- 입력 슬라이더와 시나리오 버튼을 바꾸면 score와 risk factor가 즉시 업데이트됨
- decision packet JSON과 cURL 예시를 복사하거나 다운로드할 수 있음
- 여러 회사 batch scoring을 실행하고 결과 CSV를 다운로드할 수 있음
- 사용자가 CSV를 붙여넣거나 업로드해서 브라우저 내부에서 스코어링할 수 있음
- README의 hero image, pipeline GIF, architecture diagram, dashboard preview가 사이트에서도 이어짐
- FastAPI backend와 정적 demo의 역할 차이를 명확히 설명함

## 면접에서 방어할 문장

> GitHub Pages는 정적 호스팅이라 실제 모델 서버를 올린 것은 아닙니다. 대신 리뷰어가 설치 없이 프로젝트 감을 볼 수 있도록 browser-only simulator를 만들었고, 실제 CSV validation, feature engineering, training/evaluation, artifact generation은 FastAPI 백엔드에서 실행되도록 분리했습니다.

## 주의 문구

사이트와 저장소 모두 synthetic data 기반입니다. 투자 조언, 대출 판단, 신용평가, 실제 기업 평가 용도로 사용할 수 없습니다.
