from flask import Flask, request
import subprocess

app = Flask(__name__)

DEST = "projectwork12111@gmail.com"  # metti qui l'email dove vuoi ricevere i messaggi

@app.route("/send", methods=["POST"])
def send():
    name = request.form.get("name", "")
    email = request.form.get("email", "")
    message = request.form.get("message", "")

    body = f"Da: {name} <{email}>\n\n{message}\n"

    # usa il comando 'mail' della VM (deve essere configurato e funzionante)
    subprocess.run(
        ["mail", "-s", "Messaggio da form SmartDoctor", DEST],
        input=body,
        text=True,
        check=False,
    )

    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)