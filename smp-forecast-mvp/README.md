# smp-forecast-mvp

한국 전력시장 **SMP(계통한계가격) 예측** MVP. GitHub Codespaces에서 바로 실행되는 최소 스캐폴드.

## 빠른 시작 (Codespaces)
1. 이 저장소에서 **Code ▸ Codespaces ▸ Create codespace**.
2. devcontainer가 자동으로 의존성을 설치한다(`postCreateCommand`).
3. 터미널에서:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
4. 포워딩된 8000 포트 열기 → `/docs`(Swagger), `/forecast` 호출.

## 엔드포인트
- `GET /` — 헬스체크
- `POST /train` — (재)학습
- `GET /forecast?date=YYYY-MM-DD` — 해당일 24시간 SMP 예측(기본: 내일)

데이터: `data/smp_history.csv`(`datetime`, `smp`)가 있으면 사용, 없으면 합성 데이터로 동작.

## AI 코딩 도구 (멀티 도구)
프로젝트 컨텍스트는 **`AGENTS.md`** 한 곳에서 관리한다. `CLAUDE.md`·`GEMINI.md`는 이 파일로의 심볼릭 링크라, Claude Code·Gemini CLI·Codex/ChatGPT·Copilot 어느 것을 써도 같은 컨텍스트를 읽는다.

자세한 환경설정·바이브 코딩 워크플로우는 **SETUP.md** 참고.
