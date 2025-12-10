import json, os, csv, smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime

CFG_PATH = "/app/config.json" if os.path.exists("/app/config.json") else "./config.json"
cfg = {}
if os.path.exists(CFG_PATH):
    try:
        with open(CFG_PATH) as f:
            cfg = json.load(f)
    except json.JSONDecodeError:
        cfg = {}

def invia_email(subject, body, to_emails):
    email_cfg = cfg.get("email", {})
    smtp_server = email_cfg.get("smtp_server")
    smtp_port = email_cfg.get("smtp_port")
    from_email = email_cfg.get("from")
    username = email_cfg.get("username")
    password = email_cfg.get("password_env")

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = ", ".join(to_emails)
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(username, password)
        server.sendmail(from_email, to_emails, msg.as_string())
        server.quit()
        print(f"[EMAIL] Alert inviato a {to_emails}")
    except Exception as e:
        print(f"[EMAIL] Errore invio email: {e}")

csvfile = "logs/metrics.csv"
if not os.path.exists(csvfile):
    print("[Autocare] Nessun file di metriche trovato")
    exit()

with open(csvfile) as f:
    last_line = list(csv.DictReader(f))[-1]

alerts = []
if float(last_line["cpu"]) > cfg.get("cpu_alert_pct", 85):
    alerts.append(f"CPU alta: {last_line['cpu']}%")
if float(last_line["mem_percent"]) > cfg.get("ram_alert_pct", 85):
    alerts.append(f"RAM alta: {last_line['mem_percent']}%")
if float(last_line["disk_percent"]) > cfg.get("disk_alert_pct", 90):
    alerts.append(f"DISK alta: {last_line['disk_percent']}%")

if alerts:
    subject = "[SmartDoctor ALERT] Soglie superate"
    body = f"Data: {last_line['time']}\n" + "\n".join(alerts)
    to_emails = cfg.get("email", {}).get("to", [])
    if to_emails:
        invia_email(subject, body, to_emails)
    print("[Autocare] Alert generati:", alerts)
else:
    print("[Autocare] Nessuna soglia superata")
