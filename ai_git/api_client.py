import requests

def call_ai(api_key, prompt, model, temperature, max_tokens):
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
        ],
        "temperature": temperature,
        "max_tokens": max_tokens
    }

    try:
        return requests.post(url, headers=headers, json=data, timeout=30)
    except requests.exceptions.RequestException as e:
        print(f"[WARN] 네트워크 오류: {e}")
        return None