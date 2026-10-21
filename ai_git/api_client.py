import time
import requests

def call_ai(api_key, prompt, model):
    url = "https://copa.codyssey.kr/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    data = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    for attempt in range(2):
        try:
            response = requests.post(
                url,
                headers=headers,
                json=data,
                timeout=30
            )

            if response.status_code == 200:
                return response

            print(
                f"[WARN] AI API 호출 실패 "
                f"({response.status_code}), "
                f"시도 {attempt + 1}/2"
            )

        except requests.exceptions.RequestException as e:
            print(f"[WARN] 네트워크 오류: {e}")

        if attempt == 0:
            time.sleep(1)

    return response