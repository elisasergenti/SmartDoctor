import os

import subprocess

import time

def clean_temp_files():

    """Esegue la pulizia dei file temporanei e delle vecchie cartelle di log."""

    print("--- Avvio Azione Correttiva: Pulizia File Temporanei ---")

    try:

        command = "find /tmp/ -type f -mtime +3 -delete"

        subprocess.run(command, shell=True, check=True)

        print("Pulizia /tmp completata per i file più vecchi di 3 giorni.")

    except subprocess.CalledProcessError as e:

        print(f"ERRORE durante la pulizia dei file temporanei: {e}")

    except Exception as e:

        print(f"Errore generico in clean_temp_files: {e}")

if __name__ == "__main__":

    clean_temp_files()

    print("--- Fine actions.py ---")
