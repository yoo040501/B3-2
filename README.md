# AI Git Commit / PR Generator

Git 변경 사항을 수집하여 AI API에 전달하고, 변경 내용을 기반으로 **커밋 메시지와 Pull Request 초안**을 자동 생성하는 Python CLI 프로그램입니다.

`git status`와 `git diff` 결과를 AI 입력 데이터로 사용하며, 프롬프트를 통해 커밋 및 PR의 출력 형식을 제어합니다.

---

## 1. 주요 기능

- `git status`를 이용한 변경 파일 확인
- `git diff`를 이용한 변경 내용 수집
- AI API를 이용한 커밋 메시지 자동 생성
- AI API를 이용한 PR 제목 및 본문 자동 생성
- Commit / PR별 프롬프트 분리
- 모델, `temperature`, `max_tokens` CLI 옵션 지원
- API Key 환경변수 관리
- API 요청 실패 및 네트워크 오류 처리
- API 요청 실패 시 제한된 횟수만 재시도
- Safe Mode를 이용한 민감정보 마스킹
- AI 생성 결과의 제목 길이 및 PR 구조 검증
- 변경 사항이 없을 경우 API를 호출하지 않고 종료

---

## 2. 프로젝트 구조

```text
B3-2/
├── main.py
├── README.md
├── .gitignore
│
└── ai_git/
    ├── __init__.py
    ├── api_client.py
    ├── cli.py
    ├── git_utils.py
    ├── prompts.py
    ├── run.py
    ├── sanitizer.py
    └── validator.py
```

각 파일의 역할은 다음과 같습니다.

| 파일 | 역할 |
| --- | --- |
| `main.py` | 프로그램 실행 진입점 |
| `ai_git/run.py` | Git 수집 → Safe Mode → 프롬프트 생성 → API 호출 → 검증 → 출력 흐름 관리 |
| `ai_git/cli.py` | `commit`, `pr` 명령과 CLI 옵션 처리 |
| `ai_git/api_client.py` | AI REST API 호출, timeout 및 재시도 처리 |
| `ai_git/git_utils.py` | `git status`, `git diff` 실행 및 결과 수집 |
| `ai_git/prompts.py` | Commit / PR용 프롬프트 생성 |
| `ai_git/sanitizer.py` | 이메일, API Key, Bearer Token 마스킹 |
| `ai_git/validator.py` | Commit / PR 출력 형식 검증 |
| `ai_git/__init__.py` | `ai_git` Python 패키지 정의 |

---

## 3. 개발 환경

- Python 3.12 이상
- Git
- Terminal CLI 환경

웹 화면 없이 터미널에서 실행합니다.

---

## 4. REST API

REST API는 HTTP를 이용하여 프로그램이 외부 서버에 요청을 보내고 응답을 받는 방식입니다.

이 프로젝트에서는 Python 프로그램이 Git 변경 사항과 프롬프트를 AI 서버에 전송하고, AI가 생성한 커밋 메시지 또는 PR 초안을 JSON 형태로 전달받습니다.

전체 흐름은 다음과 같습니다.

```text
git status / git diff 수집
        ↓
프롬프트 생성
        ↓
HTTP POST 요청
        ↓
AI API
        ↓
JSON 응답
        ↓
생성된 텍스트 추출
        ↓
Commit / PR 출력
```

대표적인 HTTP 요청 방식은 다음과 같습니다.

- `GET` : 데이터 조회
- `POST` : 데이터 전달 및 생성 요청
- `PUT` : 데이터 수정
- `DELETE` : 데이터 삭제

이 프로젝트에서는 AI에게 입력 데이터를 전달하고 새로운 텍스트 생성을 요청하기 때문에 `POST` 방식을 사용합니다.

API 요청에는 다음 정보가 포함됩니다.

```text
URL
→ 요청할 AI API 주소

Headers
→ API Key 등 인증 정보

JSON Body
→ model, messages, temperature, max_tokens 등의 요청 데이터

Response
→ AI 서버가 반환한 HTTP 응답
```

AI 서버가 반환한 JSON 응답에서 생성된 텍스트를 추출하여 커밋 메시지 또는 PR 초안으로 사용합니다.

---

## 5. API Key 설정

API Key는 코드에 직접 작성하지 않고 환경변수로 관리합니다.

macOS / Linux:

```bash
export AI_API_KEY="YOUR_API_KEY"
```

설정 확인:

```bash
echo $AI_API_KEY
```

API Key가 설정되어 있지 않으면 프로그램은 종료됩니다.

```text
[ERROR] AI_API_KEY 환경변수가 설정되지 않았습니다.
```

API Key는 소스 코드나 GitHub 저장소에 직접 저장하지 않습니다.

---

## 6. 사용 방법

프로그램은 Git이 초기화된 프로젝트 디렉토리에서 실행합니다.

### 커밋 메시지 생성

```bash
python3 main.py commit
```

현재 Git 변경사항을 분석하여 커밋 메시지를 생성합니다.

예시:

```text
--- Commit Message ---
Feat: AI 기반 커밋 메시지 생성 기능 추가

- Git 변경사항 수집 기능 추가
- AI API 호출 및 프롬프트 생성 기능 구현
----------------------
```

### PR 초안 생성

```bash
python3 main.py pr
```

현재 Git 변경사항을 분석하여 PR 제목과 본문 초안을 생성합니다.

예시:

```text
--- PR Draft ---
AI 기반 Commit / PR 자동 생성 기능 추가

## Why
- Git 변경사항을 기반으로 작성 작업을 자동화하기 위해 기능을 추가했습니다.

## What
- git status 및 git diff 결과 수집
- AI API 연동
- Commit / PR별 프롬프트 생성

## How to Test
- AI_API_KEY 환경변수를 설정합니다.
- python3 main.py commit을 실행합니다.
- python3 main.py pr을 실행합니다.
----------------
```

---

## 7. CLI 옵션

### Model

사용할 AI 모델을 지정합니다.

```bash
python3 main.py commit --model gpt-5.4-mini
```

기본 모델은 `gpt-5.4-mini`입니다.

### Temperature

```bash
python3 main.py commit --temperature 0.3
```

`temperature`는 AI가 생성하는 결과의 다양성을 조절합니다.

- 낮은 값: 비교적 일관되고 정형화된 결과
- 높은 값: 보다 다양한 표현의 결과

커밋 메시지와 PR처럼 일정한 형식이 필요한 작업에서는 비교적 낮은 값을 사용하는 것이 적합합니다.

기본값:

```text
0.3
```

### Max Tokens

```bash
python3 main.py pr --max-tokens 500
```

`max_tokens`는 AI가 생성할 수 있는 최대 출력 토큰 수를 제한합니다.

기본값:

```text
500
```

### 옵션 조합

```bash
python3 main.py pr \
    --model gpt-5.4-mini \
    --temperature 0.3 \
    --max-tokens 500
```

---

## 8. Safe Mode

`git diff`에는 API Key, 이메일 주소, 인증 Token 등 외부 AI API에 그대로 전달하고 싶지 않은 정보가 포함될 수 있습니다.

Safe Mode는 AI API에 데이터를 전달하기 전에 특정 민감정보 패턴을 정규표현식으로 찾아 마스킹합니다.

사용 방법:

```bash
python3 main.py commit --safe-mode
```

또는:

```bash
python3 main.py pr --safe-mode
```

현재 Safe Mode에서 마스킹하는 항목은 다음과 같습니다.

| 항목 | 마스킹 결과 |
| --- | --- |
| 이메일 주소 | `[REDACTED_EMAIL]` |
| API Key 형태의 값 | `[REDACTED_API_KEY]` |
| Bearer Token | `[REDACTED_TOKEN]` |

예를 들어 다음과 같은 diff가 있다면:

```text
email=test@example.com
API_KEY="abcdef123456"
Authorization: Bearer token123456
```

Safe Mode에서는 다음과 같이 변환한 뒤 AI API로 전달합니다.

```text
email=[REDACTED_EMAIL]
API_KEY=[REDACTED_API_KEY]
Authorization: Bearer [REDACTED_TOKEN]
```

전체 처리 과정은 다음과 같습니다.

```text
git diff
   ↓
Safe Mode 활성화 여부 확인
   ↓
이메일 / API Key / Bearer Token 탐지
   ↓
민감정보 마스킹
   ↓
AI API 전달
```

Safe Mode는 정규표현식으로 정의된 패턴을 기준으로 동작하기 때문에 모든 종류의 민감정보를 완벽하게 탐지하는 것은 아닙니다.

따라서 생성형 AI에 전달하기 전에 실제 Git 변경 내용을 사용자가 확인하는 것이 필요합니다.

---

## 9. Commit 생성 규칙

Commit 프롬프트에는 다음 규칙을 전달합니다.

- 첫 줄은 커밋 제목
- Conventional Commit 형식 사용
- 제목은 가능하면 50자 이내
- 제목은 최대 72자
- 제목 다음에는 빈 줄 사용
- 본문에는 핵심 변경 사항을 bullet 형태로 작성
- 불필요한 설명은 출력하지 않도록 요청

예:

```text
Feat: AI API 연동 기능 추가

- Git diff 기반 프롬프트 생성
- AI 응답 처리 기능 추가
```

---

## 10. PR 생성 규칙

PR 제목은 최대 80자로 생성하도록 요청합니다.

PR 본문은 다음 구조를 사용합니다.

```text
## Why
- 변경 배경

## What
- 핵심 변경 사항

## How to Test
- 테스트 방법
```

각 섹션에는 변경 이유, 변경 내용, 테스트 방법을 작성하도록 프롬프트를 구성합니다.

---

## 11. 출력 검증

AI에게 형식 규칙을 프롬프트로 전달하더라도 생성 결과가 항상 규칙을 만족한다는 보장은 없습니다.

따라서 `validator.py`에서 생성된 결과를 한 번 더 검사합니다.

### Commit 검증

다음 항목을 확인합니다.

```text
1. 커밋 메시지가 비어 있지 않은지 확인
2. 첫 번째 줄을 커밋 제목으로 판단
3. 커밋 제목이 72자를 초과하는지 확인
```

커밋 메시지가 비어 있으면:

```text
커밋 메시지가 비어 있습니다.
```

제목이 72자를 초과하면:

```text
커밋 제목이 72자를 초과했습니다.
```

### PR 검증

다음 항목을 확인합니다.

```text
1. PR 내용이 비어 있지 않은지 확인
2. 첫 번째 줄을 PR 제목으로 판단
3. PR 제목이 80자를 초과하는지 확인
4. ## Why 섹션 존재 여부 확인
5. ## What 섹션 존재 여부 확인
6. ## How to Test 섹션 존재 여부 확인
```

필수 섹션이 없으면 해당 섹션이 없다는 검증 결과를 반환합니다.

예:

```text
## Why 섹션이 없습니다.
```

프롬프트는 AI에게 원하는 출력 형식을 요청하는 역할을 하고, validator는 실제 생성 결과가 기본 형식 조건을 만족하는지 확인하는 역할을 합니다.

---

## 12. 오류 처리

### 변경 사항 없음

Git 변경 사항이 없으면 AI API를 호출하지 않고 종료합니다.

```text
[INFO] 변경 사항이 없습니다.
```

### API Key 없음

```text
[ERROR] AI_API_KEY 환경변수가 설정되지 않았습니다.
```

### API 요청 실패

AI 서버 오류 또는 네트워크 오류가 발생하면 오류 내용을 출력합니다.

예:

```text
[WARN] AI API 호출 실패 (502), 시도 1/2
```

일시적인 API 오류를 고려하여 제한된 횟수만 재시도합니다.

API 요청에는 timeout을 적용하여 서버가 응답하지 않는 상황에서 프로그램이 무한정 대기하지 않도록 처리합니다.

---

## 13. 다른 Git 프로젝트에서 사용

프로그램의 저장 위치와 분석할 Git 프로젝트의 위치가 같을 필요는 없습니다.

예를 들어 프로그램이 다음 위치에 있고:

```text
/Users/user/B3-2
```

분석할 프로젝트가 다음 위치에 있다면:

```text
/Users/user/eval1
```

먼저 분석하려는 Git 프로젝트로 이동합니다.

```bash
cd /Users/user/eval1
```

그다음 프로그램을 실행합니다.

```bash
python3 /Users/user/B3-2/main.py commit
```

PR 초안도 동일하게 생성할 수 있습니다.

```bash
python3 /Users/user/B3-2/main.py pr
```

`git status`와 `git diff`는 프로그램 파일의 위치가 아니라 현재 작업 중인 Git 저장소를 기준으로 실행됩니다.

---

## 14. 프로그램 동작 흐름

```text
python3 main.py commit / pr
            ↓
       CLI 옵션 분석
            ↓
      API Key 확인
            ↓
       git status
            ↓
    변경 사항 존재 확인
            ↓
        git diff
            ↓
   Safe Mode 활성화 시
     민감정보 마스킹
            ↓
   Commit / PR 프롬프트
            ↓
       AI REST API
            ↓
        JSON 응답 처리
            ↓
       출력 형식 검증
            ↓
   Commit / PR 초안 출력
```

---

## 15. 주의사항

- API Key는 환경변수로 관리합니다.
- API Key를 GitHub 저장소에 업로드하지 않습니다.
- `git diff`에는 코드뿐 아니라 민감정보가 포함될 수 있습니다.
- 민감한 변경사항이 있는 경우 `--safe-mode`를 사용합니다.
- Safe Mode가 모든 민감정보를 탐지하는 것은 아닙니다.
- AI API의 불필요한 호출을 피합니다.
- 한 번의 실행에서 API 호출 횟수를 최소화합니다.
- AI가 생성한 커밋 메시지와 PR 초안은 최종 정답이 아닙니다.
- 생성 결과를 사용자가 검토한 후 실제 Git 작업에 사용합니다.

## 테스트 전략

각 모듈은 기능별로 분리되어 있어 독립적으로 테스트할 수 있습니다.

- `git_utils.py`
  - 실제 Git 저장소에서 `git status`, `git diff` 결과 확인
  - `subprocess.run`을 mock하여 Git 명령 성공/실패 상황 테스트

- `api_client.py`
  - 정상 응답(200), 인증 실패, 서버 오류, timeout 등을 mock하여 테스트

- `validator.py`
  - 정상 Commit/PR 문자열
  - 제목 길이 초과
  - PR 필수 섹션 누락
  - 섹션 내 불릿 누락 등을 직접 입력하여 테스트

## AI 파라미터 영향

### temperature

`temperature`가 낮을수록 결과가 비교적 안정적이고 일관되며,
높을수록 다양한 표현이 생성될 가능성이 높아집니다.

커밋 메시지와 PR처럼 일정한 형식과 내용의 일관성이 중요한 경우
낮은 값을 사용하는 것이 적합합니다.

값이 너무 높으면 표현 다양성은 증가하지만
변경 내용 간 연결이나 출력 형식의 일관성이 떨어질 수 있습니다.

### max_tokens

`max_tokens`는 AI가 생성할 수 있는 최대 출력량을 제한합니다.

값이 너무 작으면 PR 본문이 중간에서 잘려
`Why`, `What`, `How to Test` 중 일부가 누락될 수 있습니다.

출력이 잘리는 경우에는 `max_tokens` 값을 늘리거나
프롬프트 및 입력 diff의 길이를 줄이는 방식으로 대응할 수 있습니다.

## 재생성 및 후처리 기준

AI 결과가 규칙을 만족하지 않을 경우 재생성과 후처리 중 하나를 선택할 수 있습니다.

제목 길이 초과, 필수 섹션 누락, 불릿 누락처럼
명확한 규칙으로 판단할 수 있는 문제는 프로그램에서 검증하거나
후처리하는 방식이 빠르고 결과를 제어하기 쉽습니다.

반면 AI가 코드 변경 목적을 잘못 이해했거나
요약 내용 자체가 부정확한 경우에는 단순 후처리보다
프롬프트를 수정하여 다시 생성하는 것이 적합합니다.

## AI 결과 검토

AI가 생성한 결과는 항상 정확하거나 중립적인 것은 아닙니다.

예를 들어 특정 변경 사항을 실제보다 중요하게 표현하거나,
코드의 목적을 추정하여 사실과 다른 설명을 만들 수 있습니다.

따라서 사용자는 다음 내용을 확인한 후 결과를 사용해야 합니다.

- 실제 `git diff` 내용과 설명이 일치하는지
- 존재하지 않는 기능이나 변경 내용을 작성하지 않았는지
- 특정 변경 사항을 과도하게 강조하지 않았는지
- Commit/PR 제목과 본문이 프로젝트 규칙에 맞는지
- 민감정보가 포함되지 않았는지

---

## 16. 실행 예시

커밋 메시지 생성:

```bash
python3 main.py commit
```

PR 초안 생성:

```bash
python3 main.py pr
```

Safe Mode:

```bash
python3 main.py commit --safe-mode
```

CLI 옵션 적용:

```bash
python3 main.py pr \
    --model gpt-5.4-mini \
    --temperature 0.3 \
    --max-tokens 500 \
    --safe-mode
```

---

## 17. 학습 내용

이 프로젝트를 통해 다음 내용을 학습합니다.

- REST API의 기본 구조
- HTTP POST 요청 방식
- JSON 요청 및 응답 처리
- AI API 호출 및 예외 처리
- 환경변수를 이용한 API Key 관리
- Python `subprocess`를 이용한 Git 명령 실행
- `git status`, `git diff` 결과를 프로그램 입력으로 연결하는 방법
- CLI 프로그램 구성 및 옵션 처리
- Commit / PR용 프롬프트 설계
- `temperature`, `max_tokens` 등 AI API 파라미터의 역할
- 정규표현식을 이용한 민감정보 마스킹
- AI 생성 결과에 대한 후처리 및 형식 검증
- Python 코드를 패키지 및 모듈 단위로 분리하는 방법