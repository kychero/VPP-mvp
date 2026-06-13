# SMP 예측 MVP — 온라인 개발 환경 설정 가이드 (SETUP.md)

개인 개발 + GitHub + 바이브 코딩(AI 보조 코딩)으로 **작은 SMP 예측 툴**을 MVP로 만들기 위한 환경 구성 문서다. 노트북에 아무것도 설치하지 않고 **브라우저만으로** 시작하는 것을 목표로 한다.

---

## 0. 추천 환경 한눈에

| 구성 | 추천 | 이유 |
|---|---|---|
| 온라인 개발 환경 | **GitHub Codespaces** | GitHub 저장소에 바로 붙는 클라우드 VS Code. 브라우저만으로 개발, 환경 재현(devcontainer) |
| AI 코딩 도구 | **여러 도구 병행** (Gemini CLI / ChatGPT(Codex) / Copilot / Claude Code) | 비용·취향에 따라 선택·혼용. 컨텍스트는 `AGENTS.md` 하나로 공유 |
| 언어/프레임워크 | **Python + FastAPI** | 예측·ML 표준, API화 간단. VPP 아키텍처의 "SMP 예측 서비스"와 일관 |
| ML | **scikit-learn + XGBoost** | 시계열·가격 예측 표준 라이브러리 |
| 버전관리 | **GitHub** | 저장소 + Codespaces + (선택)Actions 일원화 |

**왜 Codespaces인가:** 개인 Free 플랜에 매월 일정 무료 사용량(컴퓨트 코어-시간 + 스토리지)이 포함되어 개인 MVP에 충분하고, 머신을 끄고 켜도 작업 상태가 유지된다. 로컬 설치/환경 오염이 없다.

> 참고(2026년 기준, 변동 가능): GitHub 공식 안내상 **개인 Free 계정은 월 120 core-hours**(2코어 머신이면 실사용 약 60시간) **+ 15GB 스토리지**, **Pro는 180 core-hours + 20GB**가 포함된다. 정확한 최신 한도·요금은 GitHub Billing 문서에서 재확인할 것.

---

## 1. 사전 준비

1. **GitHub 계정** (없으면 github.com에서 생성).
2. **AI 코딩 도구는 여러 개를 골라 쓸 수 있다.** 컨텍스트 파일(`AGENTS.md`)을 공유하므로 도구를 섞어 써도 된다. 비용 관점 정리:
   - **Gemini CLI** — 개인용 무료 한도가 비교적 넉넉. 비용 부담이 가장 적은 편.
   - **ChatGPT(Codex)** — ChatGPT 구독으로 Codex(에이전트) 사용. `AGENTS.md`를 기본으로 읽음.
   - **GitHub Copilot** — 개인 무료 티어 존재, Codespaces/VS Code에 바로 통합.
   - **Claude Code** — 품질 좋지만 유료 플랜(Pro/Max 등) 또는 API 크레딧 필요. 필요할 때만 선택적으로.
3. 결제수단은 도구별 정책에 따른다. 각 도구의 최신 무료 한도·요금은 공식 페이지에서 확인.

> 비용 메모: Codespaces 무료 한도 + 무료/저비용 AI 도구(Gemini CLI, Copilot 무료 티어)만으로도 개인 MVP는 충분히 진행할 수 있다. Codespaces는 **정지(stop)해도 스토리지 비용이 누적**되므로, 안 쓰는 코드스페이스는 **삭제(delete)**한다.

---

## 2. 1단계 — GitHub 저장소 만들기

1. GitHub에서 **New repository** → 이름 예: `smp-forecast-mvp`.
2. **Private** 권장(개인 개발), `Add a README` 체크.
3. 생성 완료.

이 저장소에 아래 §3의 스캐폴드 파일을 올린다(웹 UI 업로드 또는 Codespaces에서 직접 생성). 본 문서와 함께 제공된 `smp-forecast-mvp/` 폴더를 그대로 커밋하면 된다.

---

## 3. 2단계 — 프로젝트 스캐폴드

제공된 스캐폴드의 구조:

```
smp-forecast-mvp/
├─ .devcontainer/
│  └─ devcontainer.json     # Codespaces 환경 정의 (Python 3.12 + 확장 + 자동 설치)
├─ app/
│  ├─ __init__.py
│  ├─ main.py               # FastAPI 엔드포인트
│  └─ forecaster.py         # 데이터 로딩 + 베이스라인 예측
├─ data/
│  └─ .gitkeep              # SMP 이력 CSV 자리 (없으면 합성 데이터로 동작)
├─ .env.example            # 향후 API 키 템플릿
├─ .gitignore
├─ AGENTS.md               # AI 코딩 에이전트용 컨텍스트(단일 원본, 중요)
├─ CLAUDE.md  -> AGENTS.md  # 심볼릭 링크 (Claude Code용)
├─ GEMINI.md  -> AGENTS.md  # 심볼릭 링크 (Gemini CLI용)
├─ README.md
└─ requirements.txt
```

핵심: **`.devcontainer/devcontainer.json`** 이 있으면 Codespaces가 매번 동일한 Python 환경을 자동 구성하고 의존성까지 설치한다. **`AGENTS.md`** 는 AI 에이전트가 프로젝트 규칙·구조·다음 작업을 이해하게 해주는 단일 원본 컨텍스트 파일이며, `CLAUDE.md`·`GEMINI.md` 는 이 파일로의 심볼릭 링크라 어떤 도구를 쓰든 동일 내용을 읽는다.

---

## 4. 3단계 — Codespaces 실행

1. 저장소 페이지에서 녹색 **Code** 버튼 → **Codespaces** 탭 → **Create codespace on main**.
2. 잠시 후 브라우저에 VS Code가 뜨고, `postCreateCommand` 로 `requirements.txt` 가 자동 설치된다.
3. 설치가 끝나면 준비 완료.

> 로컬 VS Code를 선호하면, 데스크톱 VS Code의 *GitHub Codespaces* 확장으로 동일 코드스페이스에 접속할 수도 있다.

---

## 5. 4단계 — AI 코딩 도구 설정 (바이브 코딩)

**컨텍스트는 `AGENTS.md` 하나로 공유**되므로, 아래 도구 중 무엇을 쓰든(또는 섞어 써도) 같은 프로젝트 맥락을 읽는다. 비용·취향에 맞춰 고른다.

### 옵션 A) Gemini CLI (무료 한도 넉넉, 비용 부담 최소)
Codespaces 터미널에서 설치(npm). 프로젝트 폴더에서 실행하면 `GEMINI.md`(→`AGENTS.md`)를 읽는다.
```bash
npm install -g @google/gemini-cli   # 또는: npx @google/gemini-cli
gemini                              # 로그인/인증 후 사용
```

### 옵션 B) ChatGPT — Codex CLI
ChatGPT 구독으로 Codex(에이전트)를 사용한다. `AGENTS.md`를 기본 컨텍스트로 읽는다.
```bash
npm install -g @openai/codex        # 설치 후
codex
```

### 옵션 C) GitHub Copilot (에디터 통합, 가장 간단)
devcontainer에 Copilot/Chat 확장이 포함되어 있어, Codespaces에서 GitHub 계정으로 활성화하면 인라인 제안+Chat을 바로 쓴다. 별도 설치 불필요.

### 옵션 D) Claude Code (선택, 유료)
품질은 좋지만 유료 플랜/크레딧이 필요하다. 필요할 때만:
```bash
curl -fsSL https://claude.ai/install.sh | bash   # 네이티브 설치(권장)
claude --version
```
프로젝트 폴더에서 `claude` 실행 시 `CLAUDE.md`(→`AGENTS.md`)를 읽는다.

> 각 도구의 설치 명령·무료 한도·인증 방식은 자주 바뀌므로, 막히면 해당 도구 공식 문서를 확인한다. 어떤 도구든 **저장소 루트에서 실행**해야 컨텍스트 파일을 읽는다.

---

## 6. 5단계 — 앱 실행 & 확인

Codespaces 터미널에서:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
- 8000 포트가 자동 포워딩된다. **Ports** 탭에서 URL 열기.
- `GET /` → 헬스체크
- `GET /docs` → Swagger UI에서 직접 호출
- `GET /forecast?date=2026-06-15` → 해당일 24시간 SMP 예측(기본은 내일)
- `POST /train` → (재)학습

데이터가 없으면 합성 SMP로 동작하므로 **첫 실행부터 결과가 나온다**. 실데이터를 쓰려면 `data/smp_history.csv`(`datetime`, `smp` 컬럼)를 채운다.

---

## 7. 6단계 — 바이브 코딩 워크플로우

작게, 자주, 확인하며 진행하는 루프를 권장한다.

1. **목표를 한 문장으로** 에이전트에게 지시. 예:
   - "`forecaster.py`에 `XGBoostForecaster`를 추가해줘. 피처는 hour, dayofweek, month, lag1, lag24, rolling24 평균. 기존 `BaselineForecaster`는 비교용으로 남겨."
   - "백테스트 함수와 MAPE 지표를 만들고, 베이스라인 대비 표로 출력해줘."
   - "`/forecast`에 P10/P50/P90 분위수 예측 옵션을 추가해줘."
2. **에이전트가 변경 → 즉시 실행/확인** (`/docs`에서 호출, 또는 테스트).
3. **작은 단위로 커밋**:
   ```bash
   git add -A && git commit -m "feat: add XGBoost forecaster" && git push
   ```
4. 문제가 생기면 에이전트에게 에러 로그를 그대로 붙여 수정 요청.

**팁**
- `AGENTS.md`를 최신으로 유지하면 에이전트 품질이 올라간다(스택·구조·규칙·다음 작업). 도구가 여러 개여도 이 파일만 고치면 된다.
- 한 번에 큰 리팩터링을 시키지 말고, **실행 가능한 작은 변경**으로 쪼갠다.
- 모델을 교체할 때 기존 베이스라인을 남겨 **항상 비교군**을 둔다.

---

## 8. 시크릿(비밀값) 관리

- 로컬/코드스페이스용: `.env.example` 을 복사해 `.env` 작성. `.env` 는 `.gitignore`로 **커밋 금지**.
- 초기 MVP(합성/CSV 데이터)에는 키가 필요 없다. 기상·KPX 실데이터 연동 단계에서 사용.
- Codespaces에 안전하게 주입하려면 **GitHub ▸ Settings ▸ Codespaces ▸ Secrets** 에 등록하면 환경변수로 들어온다. (저장소 코드에 키를 절대 하드코딩하지 않는다.)

---

## 9. 비용·한도 주의사항 (Codespaces)

- 무료 한도는 **컴퓨트(core-hours)와 스토리지(GB) 두 가지** 모두에 걸린다. 둘 중 하나라도 소진되면 사용이 제한된다.
- **정지(stop)해도 스토리지 비용은 계속 누적**된다 → 안 쓰는 코드스페이스는 **삭제**.
- 큰 머신(4코어)은 무료 코어-시간을 더 빨리 소모한다. 개인 MVP는 **2코어로 충분**.
- 정확한 최신 한도/요금은 GitHub Billing 문서에서 확인.

---

## 10. 다음 단계 (모델 고도화 로드맵)

1. **베이스라인 → XGBoost/LightGBM**: 달력·lag·rolling·기상 피처.
2. **백테스트 + MAPE**: 베이스라인 대비 정확도 비교, 모델 버전 관리.
3. **확률 예측(P10/P50/P90)**: VPP의 ESS 스케줄링 입력으로 바로 연결 가능.
4. **실데이터 적재**: KPX SMP 이력 수집 스크립트(`scripts/ingest.py`), 기상 API 연동.
5. **배포**: Dockerfile 추가 → 클라우드/컨테이너로 배포(아키텍처 문서의 `smp-forecast-svc`로 승격).
6. (선택) **CI**: GitHub Actions로 테스트/린트 자동화.

---

## 11. 참고 링크

- GitHub Codespaces 빌링/한도: https://docs.github.com/billing/managing-billing-for-github-codespaces/about-billing-for-github-codespaces
- Claude Code 설치/설정: https://code.claude.com/docs/en/setup
- Gemini CLI: https://github.com/google-gemini/gemini-cli
- Codex CLI(ChatGPT): https://github.com/openai/codex
- AGENTS.md 표준: https://agents.md
- FastAPI: https://fastapi.tiangolo.com
- XGBoost: https://xgboost.readthedocs.io

> 본 문서의 무료 한도/요금/설치 명령은 2026년 기준이며 변동될 수 있으니, 진행 전 각 공식 문서에서 최신 내용을 확인할 것.
