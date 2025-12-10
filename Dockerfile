FROM python:3.10-slim

RUN apt-get update && apt-get install -y cron bash curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY monitor.py autocare.py exporter.py alert_check.py action.py smartdoctor-cron config.json telegram_bot.py ./

COPY logs/ ./logs/
COPY templates/ ./templates/

RUN pip install --no-cache-dir psutil prometheus_client requests python-telegram-bot psycopg2-binary

COPY smartdoctor-cron /etc/cron.d/smartdoctor-cron
RUN chmod 0644 /etc/cron.d/smartdoctor-cron && crontab /etc/cron.d/smartdoctor-cron

RUN chmod +x *.py smartdoctor-cron

CMD ["/usr/sbin/cron", "-f"]
