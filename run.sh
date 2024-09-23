echo LINE_TOKEN=$LINE_TOKEN >> /etc/environment;
service cron start;uvicorn main:app --host 0.0.0.0 --port 8080 --reload
