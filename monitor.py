import psutil
import csv
import datetime
import json
import os
import sys
import psycopg2

print("=== Avvio monitor.py ===")

DB_NAME = os.environ.get("POSTGRES_DB", "smartdoctor_db")
DB_USER = os.environ.get("POSTGRES_USER", "sd_user")
DB_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "sd_password")
DB_HOST = os.environ.get("DB_HOST", "postgres_db")

def create_table():
    """Tenta di creare la tabella system_metrics."""
    conn = None
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST
        )
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS system_metrics (
                id SERIAL PRIMARY KEY,
                timestamp TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
                cpu REAL,
                ram REAL,
                disk REAL,
                sent REAL,
                recv REAL
            );
        """)
        conn.commit()
    except Exception as e:
        print(f"Errore init DB (Ignorato se il DB si sta avviando): {e}")
    finally:
        if conn:
            conn.close()

def save_metrics_to_db(metrics):
    """Salva i dati nel DB PostgreSQL"""
    create_table()

    conn = None
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST
        )
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO system_metrics (cpu, ram, disk, sent, recv)
            VALUES (%s, %s, %s, %s, %s)
            """,
            [
                metrics['cpu'],
                metrics['mem_percent'],
                metrics['disk_percent'],
                metrics['sent'],
                metrics['recv']
            ]
        )
        conn.commit()
        print(f"Metriche salvate su PostgreSQL: CPU={metrics['cpu']}%")
    except Exception as e:
        print(f"ERRORE GRAVE DB: {e}")
    finally:
        if conn:
            conn.close()

def collect_metrics():
    """Raccoglie le metriche del sistema e le restituisce come dizionario."""
    timestamp = datetime.datetime.now().isoformat()
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    net = psutil.net_io_counters()

    row = {
        "time": timestamp,
        "cpu": cpu,
        "mem_percent": mem.percent,
        "disk_percent": disk.percent,
        "sent": net.bytes_sent,
        "recv": net.bytes_recv
    }
    return row

if __name__ == "__main__":
    try:
        metrics_data = collect_metrics()
        save_metrics_to_db(metrics_data)

        print("=== Metriche correnti ===")
        print(f"time: {metrics_data['time']}")
        print(f"cpu: {metrics_data['cpu']}")
        print(f"mem_percent: {metrics_data['mem_percent']}")
        print(f"disk_percent: {metrics_data['disk_percent']}")
        print(f"sent: {metrics_data['sent']}")
        print(f"recv: {metrics_data['recv']}")
        print("=== Fine monitor.py ===")

    except Exception as e:
        print(f"ERRORE FATALE NELLA RACCOLTA DATI: {e}")
