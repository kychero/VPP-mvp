# AGENTS.md — AI 코딩 에이전트용 프로젝트 컨텍스트

> 이 파일은 AI 코딩 도구(Codex/ChatGPT, Claude Code, Gemini CLI, Copilot 등)가
> 저장소를 이해하도록 돕는 **단일 원본** 컨텍스트다.
> `CLAUDE.md`, `GEMINI.md` 는 이 파일로의 심볼릭 링크다(내용 중복 없음).
> 바이브 코딩 시 에이전트가 이 규칙을 따르도록 한다.

## 프로젝트
한국 전력시장 **SMP(계통한계가격) 예측** MVP. 작은 단독 서비스로 시작해
이후 VPP 플랫폼의 "SMP 예측 서비스"로 확장 가능하게 한다.

## 스택 / 규칙
- Python 3.12, FastAPI, pandas/numpy, scikit-learn, xgboost.
- 포맷터/린터: ruff. 저장 시 자동 포맷.
- 타입힌트 적극 사용. 함수는 작게, 부수효과 최소화.
- 외부 I/O(데이터 로딩, API 키)는 `app/` 경계에서만.

## 구조
- `app/main.py`     : FastAPI 엔드포인트 (`/`, `/train`, `/forecast`)
- `app/forecaster.py`: 데이터 로딩 + 예측 모델 (현재 베이스라인)
- `data/`           : SMP 이력 CSV (스키마: `datetime`, `smp`). 없으면 합성 데이터 사용.

## 실행
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
# 문서: /docs , 예측: /forecast?date=YYYY-MM-DD
```

## 다음에 해볼 일 (에이전트에게 시킬 작업 예시)
1. `BaselineForecaster` 를 유지하되, `XGBoostForecaster` 추가
   (피처: hour, dayofweek, month, 공휴일, lag/rolling, 기상).
2. 백테스트 함수 + 지표(MAPE) 추가, 베이스라인과 비교.
3. `/forecast` 에 P10/P50/P90 분위수 예측 옵션 추가.
4. KPX SMP 실데이터 적재 스크립트(`scripts/ingest.py`).
5. 간단한 단위 테스트(pytest) 추가.

## 작업 원칙
- 한 번에 하나의 작은 변경 → 실행 확인 → 커밋.
- 모델 교체 시 기존 베이스라인은 비교군으로 남긴다.
- 비밀값은 `.env`(커밋 금지), 예시는 `.env.example`.

## 도구 간 컨텍스트 파일 규약
- **단일 원본**: 이 `AGENTS.md` 한 곳만 편집한다.
- `CLAUDE.md` → `AGENTS.md` 심볼릭 링크 / `GEMINI.md` → `AGENTS.md` 심볼릭 링크.
- 링크가 풀렸다면(예: Windows 클론) 저장소 루트에서 재생성:
  ```bash
  ln -sf AGENTS.md CLAUDE.md
  ln -sf AGENTS.md GEMINI.md
  ```
