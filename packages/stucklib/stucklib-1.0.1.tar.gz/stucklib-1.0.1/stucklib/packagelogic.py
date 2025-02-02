import requests

def ask(task: str):

    api_key = "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"
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    data = {
        "messages": [
            {"role": "system", "content": "You are a programming assistant. Your task is to write maximally optimized and working code for a programming olympiad."},
            {"role": "user", "content": task}
        ],
        "model": "deepseek-r1-distill-llama-70b",
        "temperature": 0.6,
        "max_completion_tokens": 100000,
        "top_p": 0.95,
        "stream": False
    }

    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        response_json = response.json()
        return response_json["choices"][0]["message"]["content"]
    else:
        return f"Error {response.status_code}: {response.text}"