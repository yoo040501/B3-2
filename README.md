# AI Git Commit / PR Generator

Git 변경 사항을 수집하여 AI API에 전달하고, 변경 내용을 기반으로 **커밋 메시지와 Pull Request 초안**을 자동 생성하는 Python CLI 프로그램입니다.

`git status`와 `git diff` 결과를 AI 입력 데이터로 사용하며, 프롬프트를 통해 커밋 및 PR 형식을 제어합니다.

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
- API 요청 실패 시 재시도
- Safe Mode를 통한 전송 데이터 보호
- AI 생성 결과 형식 검증
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
| `ai_git/run.py` | Git 수집 → 프롬프트 생성 → API 호출 → 검증 → 출력 흐름 관리 |
| `ai_git/cli.py` | `commit`, `pr` 명령 및 CLI 옵션 처리 |
| `ai_git/api_client.py` | AI REST API 호출, timeout 및 오류/재시도 처리 |
| `ai_git/git_utils.py` | `git status`, `git diff` 실행 및 결과 수집 |
| `ai_git/prompts.py` | Commit / PR용 프롬프트 생성 |
| `ai_git/sanitizer.py` | Safe Mode에서 AI에 전달할 diff 전처리 |
| `ai_git/validator.py` | 생성된 Commit / PR의 길이 및 형식 검증 |
| `ai_git/__init__.py` | `ai_git` 패키지 정의 |

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
Git status / Git diff 수집
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

요청에는 다음과 같은 정보가 포함됩니다.

```text
URL
→ API 요청 주소

Headers
→ API Key 등 인증 정보

JSON Body
→ model, messages, temperature, max_tokens 등

Response
→ 서버가 반환한 HTTP 응답
```

AI 응답은 JSON 형태로 받은 뒤 생성된 텍스트를 추출하여 사용합니다.

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

기본 모델을 사용하지 않고 직접 모델을 지정할 수 있습니다.

```bash
python3 main.py commit --model gpt-5.4-mini
```

### Temperature

```bash
python3 main.py commit --temperature 0.3
```

`temperature`는 생성 결과의 다양성을 조절합니다.

- 낮은 값: 비교적 일관되고 정형화된 결과
- 높은 값: 표현이 다양해질 수 있음

커밋 메시지와 PR처럼 일정한 형식이 필요한 경우 낮은 값을 사용하는 것이 적합합니다.

### Max Tokens

```bash
python3 main.py pr --max-tokens 500
```

`max_tokens`는 AI가 한 번의 요청에서 생성할 수 있는 최대 출력량을 제한합니다.

### 옵션 조합

```bash
python3 main.py pr \
    --model gpt-5.4-mini \
    --temperature 0.3 \
    --max-tokens 500
```

---

## 8. Safe Mode

`git diff`에는 API Key, 이메일, Token 등의 민감정보가 포함될 수 있습니다.

Safe Mode를 활성화하려면 다음과 같이 실행합니다.

```bash
python3 main.py commit --safe-mode
```

또는:

```bash
python3 main.py pr --safe-mode
```

Safe Mode에서는 `sanitizer.py`를 통해 AI API에 전달하기 전 diff를 전처리하여 민감정보 노출 가능성을 줄입니다.

```text
git diff
   ↓
Safe Mode
   ↓
민감정보 마스킹 / 전송 데이터 제한
   ↓
AI API
```

Safe Mode가 모든 민감정보를 완벽하게 탐지하는 것은 아니므로 실제 전송 전 Git 변경 내용을 확인해야 합니다.

---

## 9. Commit 생성 규칙

Commit 프롬프트에는 다음 규칙을 적용합니다.

- 첫 줄은 커밋 제목
- Conventional Commit 형식 사용
- 제목은 50자 이내 권장
- 최대 72자
- 본문에는 핵심 변경 내용을 bullet 형태로 작성
- 불필요한 추가 설명은 생성하지 않도록 요청

예:

```text
Feat: AI API 연동 기능 추가

- Git diff 기반 프롬프트 생성
- AI 응답 처리 기능 추가
```

---

## 10. PR 생성 규칙

PR 제목은 최대 80자로 생성하도록 합니다.

본문은 다음 구조를 사용합니다.

```text
## Why
- 변경 배경

## What
- 핵심 변경 사항

## How to Test
- 테스트 방법
```

각 섹션에는 최소 하나 이상의 bullet 항목을 포함하도록 프롬프트를 구성합니다.

---

## 11. 출력 검증

AI가 프롬프트의 요구사항을 항상 정확하게 지킨다는 보장은 없기 때문에 생성 결과를 별도로 검증합니다.

`validator.py`에서 다음 항목을 검사합니다.

```text
Commit
- 제목 존재 여부
- 제목 최대 72자

PR
- 제목 존재 여부
- 제목 최대 80자
- ## Why 존재 여부
- ## What 존재 여부
- ## How to Test 존재 여부
- 필요한 출력 형식 만족 여부
```

프롬프트는 AI에게 원하는 결과를 요청하는 역할을 하고, validator는 실제 결과가 규칙을 만족하는지 확인하는 역할을 합니다.

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

AI 서버 오류 또는 네트워크 오류가 발생한 경우 오류 내용을 출력합니다.

예:

```text
[WARN] AI API 호출 실패 (502), 시도 1/2
```

일시적인 오류를 고려하여 제한된 횟수만 재시도하며, 과도한 API 호출은 수행하지 않습니다.

또한 API 요청에 timeout을 적용하여 서버 응답이 없는 경우 무한정 대기하지 않도록 처리합니다.

---

## 13. 다른 Git 프로젝트에서 사용

프로그램이 저장된 위치와 분석할 Git 프로젝트의 위치는 같을 필요가 없습니다.

예를 들어 프로그램이 다음 위치에 있고:

```text
/Users/user/B3-2
```

분석할 Git 프로젝트가 다음 위치에 있다면:

```text
/Users/user/eval1
```

먼저 분석할 프로젝트로 이동합니다.

```bash
cd /Users/user/eval1
```

그다음 프로그램을 실행합니다.

```bash
python3 /Users/user/B3-2/main.py commit
```

PR 초안 생성:

```bash
python3 /Users/user/B3-2/main.py pr
```

`git status`와 `git diff`는 프로그램 파일의 위치가 아니라 **현재 실행 중인 Git 프로젝트를 기준으로 수집**합니다.

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
     Safe Mode 처리
            ↓
   Commit / PR 프롬프트
            ↓
       AI REST API
            ↓
        응답 처리
            ↓
       출력 형식 검증
            ↓
   Commit / PR 초안 출력
```

---

## 15. 주의사항

- API Key는 환경변수로만 관리합니다.
- API Key를 GitHub 저장소에 업로드하지 않습니다.
- `git diff`에 민감정보가 포함되어 있는지 확인합니다.
- 필요한 경우 `--safe-mode`를 사용합니다.
- AI API 호출 횟수를 최소화합니다.
- AI가 생성한 결과는 최종 정답이 아닙니다.
- 생성된 Commit / PR 내용은 사용자가 검토한 후 실제 작업에 사용합니다.

---

## 16. 실행 예시

기본 Commit 생성:

```bash
python3 main.py commit
```

PR 생성:

```bash
python3 main.py pr
```

Safe Mode:

```bash
python3 main.py commit --safe-mode
```

옵션 적용:

```bash
python3 main.py pr \
    --model gpt-5.4-mini \
    --temperature 0.3 \
    --max-tokens 500 \
    --safe-mode
```

---

## 17. 학습 내용

이 프로젝트를 통해 다음 내용을 학습할 수 있습니다.

- REST API의 기본 구조
- HTTP POST 요청과 JSON 데이터 처리
- AI API 요청 및 응답 처리
- API Key 환경변수 관리
- 네트워크/API 오류 및 예외 처리
- Python `subprocess`를 이용한 Git 명령 실행
- `git status`, `git diff` 결과를 프로그램 입력으로 연결하는 방법
- CLI 프로그램 구성 방법
- AI 결과 품질을 조절하기 위한 프롬프트 설계
- `temperature`, `max_tokens` 등 AI API 파라미터의 역할
- AI 결과에 대한 후처리 및 형식 검증
- 여러 모듈을 Python 패키지 형태로 분리하는 방법