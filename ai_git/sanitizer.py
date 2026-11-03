import re


def mask_sensitive_info(text):
    # 이메일 주소
    text = re.sub(
        r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}',
        '[REDACTED_EMAIL]',
        text
    )

    # API Key처럼 보이는 값
    text = re.sub(
        r'''(?i)(\b(?:ai[_-])?api[_-]?key\b["']?\s*[=:]\s*)(?:"(?:\\.|[^"\\\r\n])*"|'(?:\\.|[^'\\\r\n])*'|[^\s,;#}\]]+)''',
        r'\1[REDACTED_API_KEY]',
        text,
    )

    # Bearer Token
    text = re.sub(
        r'(?i)(Authorization:\s*Bearer\s+)[^\s"\']+',
        r'\1[REDACTED_TOKEN]',
        text
    )

    return text