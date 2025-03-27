PORT="${PORT:-3001}"
uvicorn llm.main:app --port $PORT --host 0.0.0.0 --forwarded-allow-ips '*' --reload