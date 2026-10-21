# AI Git Commit / PR Generator

Git 변경 사항을 수집하여 AI API에 전달하고, 변경 내용을 기반으로 **커밋 메시지와 Pull Request 초안**을 자동 생성하는 Python CLI 도구입니다.

`git status`, `git diff` 결과를 AI의 입력 컨텍스트로 사용하며, 사용자는 터미널에서 `commit` 또는 `pr` 명령을 실행하여 결과를 확인할 수 있습니다.

---

## 1. 주요 기능

- `git status`를 이용한 변경 파일 확인
- `git diff`를 이용한 코드 변경 내용 수집
- AI API를 이용한 커밋 메시지 자동 생성
- AI API를 이용한 PR 제목/본문 자동 생성
- 모델, temperature, max tokens CLI 옵션 지원
- API Key 환경변수 관리
- API 요청 실패 및 네트워크 오류 처리
- 변경 사항이 없는 경우 AI API를 호출하지 않고 종료
- Safe Mode를 통한 AI 전송 데이터 제한
- PR 템플릿 자동 생성
  - Why
  - What
  - How to Test

---

## 2. 프로젝트 구조

```text
B3-2/
├── main.py
├── README.md
│
└── ai_git/
    ├── __init__.py
    ├── run.py
    ├── cli.py
    ├── api_client.py
    ├── git_utils.py
    └── prompts.py
```

각 파일의 역할은 다음과 같습니다.

```text
main.py
└── 프로그램 실행 진입점

ai_git/run.py
└── Git 수집 → 프롬프트 생성 → AI 호출 → 결과 출력 흐름 관리

ai_git/cli.py
└── commit/pr 명령 및 CLI 옵션 처리

ai_git/api_client.py
└── AI REST API 요청 및 오류 처리

ai_git/git_utils.py
└── git status, git diff 실행 및 결과 수집

ai_git/prompts.py
└── Commit / PR 생성용 프롬프트 관리
```

---

## 3. 개발 환경

- Python 3.12 이상
- Git
- Terminal CLI 환경

웹 화면 없이 터미널에서 실행됩니다.

---

## 4. API Key 설정

API Key는 코드에 직접 작성하지 않고 환경변수로 관리합니다.

macOS / Linux:

```bash
export AI_API_KEY="YOUR_API_KEY"
```

설정 여부 확인:

```bash
echo $AI_API_KEY
```

API Key가 설정되지 않은 상태에서 프로그램을 실행하면 다음과 같이 종료됩니다.

```text
[ERROR] AI_API_KEY 환경변수가 설정되지 않았습니다.
```

API Key를 소스 코드, Git 커밋 또는 GitHub 저장소에 직접 포함하지 않도록 주의해야 합니다.

---

## 5. REST API

REST API는 HTTP를 이용하여 프로그램이 외부 서버의 기능을 요청하고 응답을 받는 방식입니다.

이 프로젝트에서는 Python 프로그램이 AI 서버에 Git 변경사항과 프롬프트를 전달하고, AI 서버가 생성한 커밋 메시지 또는 PR 초안을 응답으로 반환합니다.

전체 흐름은 다음과 같습니다.

```text
Python 프로그램
    ↓
Git status / Git diff 수집
    ↓
AI 서버에 HTTP POST 요청
    ↓
AI 서버가 입력 내용 분석
    ↓
JSON 형태로 결과 반환
    ↓
Python에서 생성된 텍스트 추출
    ↓
터미널에 Commit / PR 초안 출력
```

HTTP 요청에는 여러 방식이 있으며 대표적으로 다음과 같습니다.

- `GET` : 데이터 조회
- `POST` : 데이터 전송 및 생성 요청
- `PUT` : 데이터 수정
- `DELETE` : 데이터 삭제

이 프로젝트에서는 AI에게 프롬프트를 전달하고 새로운 텍스트 생성을 요청하기 때문에 `POST` 방식을 사용합니다.

예를 들어 API 요청은 다음과 같은 구조로 이루어집니다.

```python
response = requests.post(
    url,
    headers=headers,
    json=data,
    timeout=30
)
```

각 항목의 역할은 다음과 같습니다.

```text
url
→ API 요청을 보낼 서버 주소

headers
→ API Key 등 인증 정보

json=data
→ 모델, 프롬프트 등 AI 서버에 전달할 데이터

response
→ 서버가 반환한 HTTP 응답
```

AI 서버에는 다음과 같은 JSON 데이터를 전달합니다.

```python
data = {
    "model": "gpt-5.4-mini",
    "messages": [
        {
            "role": "user",
            "content": prompt
        }
    ]
}
```

서버가 반환한 JSON 응답에서는 생성된 텍스트를 추출하여 사용합니다.

```python
content = response.json()["choices"][0]["message"]["content"]
```

즉 이 프로젝트에서는 다음과 같은 REST API 연동 과정을 사용합니다.

```text
요청 데이터 구성
→ HTTP POST 요청
→ API 인증
→ 서버 응답 수신
→ 상태 코드 확인
→ JSON 응답 처리
→ 생성된 텍스트 출력
```

---

## 6. 사용 방법

프로그램은 **Git 저장소의 루트 디렉토리에서 실행**합니다.

### 커밋 메시지 생성

```bash
python3 main.py commit
```

현재 Git 변경사항을 분석하여 커밋 제목과 변경 내용 요약을 생성합니다.

예시:

```text
--- Commit Message ---
Feat: AI 기반 커밋/PR 생성 기능 추가

- AI API 호출 기능 추가
- Git 변경사항 기반 프롬프트 생성 기능 구현
- Commit/PR 명령에 따른 출력 처리 추가
----------------------
```

### PR 초안 생성

```bash
python3 main.py pr
```

PR 제목과 함께 다음 템플릿 구조의 본문을 생성합니다.

```text
--- PR Draft ---
AI 기반 커밋/PR 자동 생성 기능 추가

## Why
- Git 변경사항을 기반으로 커밋 메시지와 PR 작성 과정을 자동화하기 위해 기능을 추가했습니다.

## What
- git status 및 git diff 결과 수집
- AI API 호출 기능 구현
- commit / pr 명령별 프롬프트 생성 기능 추가

## How to Test
- AI_API_KEY 환경변수를 설정합니다.
- python3 main.py commit 명령을 실행합니다.
- python3 main.py pr 명령을 실행합니다.
- 생성 결과가 지정된 형식을 만족하는지 확인합니다.
----------------
```

---

## 7. CLI 옵션

### 모델 변경

기본 모델:

```text
gpt-5.4-mini
```

다른 모델을 지정하려면:

```bash
python3 main.py commit --model gpt-5.4-mini
```

### Temperature

```bash
python3 main.py commit --temperature 0.3
```

기본값:

```text
0.3
```

`temperature`는 AI가 생성하는 결과의 다양성을 조절합니다.

- 낮은 값: 비교적 일관되고 정형화된 결과
- 높은 값: 다양한 표현의 결과

커밋 메시지와 PR처럼 일정한 형식이 필요한 작업에서는 비교적 낮은 값을 사용하는 것이 적합합니다.

### Max Tokens

```bash
python3 main.py pr --max-tokens 500
```

기본값:

```text
500
```

`max_tokens`는 AI가 생성할 수 있는 최대 출력 토큰 수를 제한합니다.

### 옵션 조합

```bash
python3 main.py pr \
    --model gpt-5.4-mini \
    --temperature 0.3 \
    --max-tokens 500
```

---

## 8. Safe Mode

Git diff에는 API Key, 이메일, 개인정보 등 외부 AI API로 보내고 싶지 않은 정보가 포함될 수 있습니다.

Safe Mode를 활성화하려면:

```bash
python3 main.py commit --safe-mode
```

또는:

```bash
python3 main.py pr --safe-mode
```

Safe Mode에서는 AI API로 전달되는 diff 범위를 제한하여 불필요한 코드와 정보가 전송되는 것을 줄입니다.

예:

```text
최대 200줄까지 AI API에 전달
```

Safe Mode를 사용하더라도 모든 민감정보를 완전히 탐지하거나 제거할 수 있는 것은 아니므로, AI에 전달하기 전에 변경 내용을 확인해야 합니다.

---

## 9. 프로그램 동작 흐름

```text
CLI 실행
   ↓
명령어 / 옵션 분석
   ↓
AI_API_KEY 확인
   ↓
git status 실행
   ↓
변경사항 존재 여부 확인
   ↓
git diff 수집
   ↓
Safe Mode 적용
   ↓
Commit / PR 프롬프트 생성
   ↓
AI REST API 호출
   ↓
응답 처리
   ↓
Commit / PR 초안 출력
```

---

## 10. Git 변경 사항이 없는 경우

Git 변경사항이 없으면 AI API를 호출하지 않고 종료합니다.

```text
[INFO] 변경 사항이 없습니다.
```

불필요한 API 요청을 방지할 수 있습니다.

---

## 11. API 오류 처리

API 요청 중 인증 실패, 서버 오류 또는 네트워크 오류가 발생할 수 있습니다.

예:

```text
[WARN] AI API 호출 실패 (502), 시도 1/2
```

재시도 후에도 실패하면 오류 정보를 출력하고 프로그램을 종료합니다.

```text
[ERROR] AI API 호출 실패
{"error": {...}}
```

API 요청에는 timeout을 적용하여 서버 응답이 없는 경우 프로그램이 무한정 대기하지 않도록 처리합니다.

---

## 12. Commit 생성 규칙

AI 프롬프트에는 다음 규칙을 전달합니다.

- 첫 줄은 커밋 제목
- Conventional Commit 형식 사용
- 제목은 가능하면 50자 이내
- 제목은 최대 72자
- 필요한 경우 변경 내용을 bullet 형태로 요약
- 불필요한 설명은 출력하지 않음

예:

```text
Feat: AI 기반 커밋 메시지 생성 기능 추가

- Git 변경사항 수집 기능 추가
- AI API 호출 및 결과 출력 기능 구현
```

---

## 13. PR 생성 규칙

PR 제목은 최대 80자로 생성하도록 요청합니다.

PR 본문은 다음 세 개의 섹션으로 구성됩니다.

```text
## Why
- 변경 배경

## What
- 핵심 변경 사항

## How to Test
- 테스트 방법
```

각 섹션에는 최소 하나 이상의 bullet 항목이 포함되도록 프롬프트를 구성합니다.

---

## 14. 다른 Git 프로젝트에서 사용

이 프로그램이 저장된 디렉토리와 분석하려는 Git 프로젝트의 위치가 같을 필요는 없습니다.

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

이 경우 `git status`와 `git diff`는 현재 작업 디렉토리인 `eval1`을 기준으로 실행됩니다.

PR 생성도 동일합니다.

```bash
python3 /Users/user/B3-2/main.py pr
```

---

## 15. 주의사항

- API Key는 반드시 환경변수로 관리합니다.
- API Key를 GitHub에 업로드하지 않습니다.
- Git diff에 민감정보가 포함되어 있는지 확인합니다.
- 필요하면 `--safe-mode`를 사용합니다.
- AI API의 불필요한 호출을 피합니다.
- 한 번의 `commit` 또는 `pr` 실행에서 API 요청 횟수를 최소화합니다.
- AI가 생성한 커밋 메시지와 PR 본문은 최종 결과가 아닙니다.
- 생성 결과는 반드시 사용자가 확인한 후 실제 커밋 또는 PR에 사용합니다.

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

옵션 지정:

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

- REST API의 기본 구조와 HTTP 요청 방식
- Python에서 AI API를 호출하는 방법
- API 요청/응답 및 예외 처리
- JSON 요청 데이터 구성 및 응답 처리
- 환경변수를 이용한 API Key 관리
- Python `subprocess`를 이용한 Git 명령 실행
- `git status`, `git diff`를 프로그램 입력으로 사용하는 방법
- AI 결과 품질을 조절하기 위한 프롬프트 설계
- `temperature`, `max_tokens` 등 AI API 파라미터의 역할
- Git 변경사항부터 AI 결과 생성까지의 자동화 흐름