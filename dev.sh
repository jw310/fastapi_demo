PORT="${PORT:-8000}"
uvicorn llm.main:app --port $PORT --host 0.0.0.0 --forwarded-allow-ips '*' --reload