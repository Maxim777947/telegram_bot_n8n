pip freeze > requirements.txt
alembic upgrade head



ssh -R 80:localhost:8443 nokey@localhost.run

Копируем вебхук вставляем в данные переменные в таком формате

N8N_HOST=1a8d2d4475b4c1.lhr.life
N8N_EDITOR_BASE_URL=https://1a8d2d4475b4c1.lhr.life
WEBHOOK_URL=https://1a8d2d4475b4c1.lhr.life

docker-compose up -d


uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 

