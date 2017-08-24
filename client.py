import socket

__author__ = 'johng'


def main():
    host = "192.168.0.4"
    port = 5050

    s = socket.socket()

    try:
        s.connect((host, port))
    except ConnectionRefusedError:
        print("Connection refused by server.")
        return

    if str(s.recv(1024).decode()).strip() == '110':
        print("Connection established.")
    else:
        print("Something went wrong...")
        return

    message = input("-> ")
    while message != "q":
        response = None
        if message == "sendgroup":
            try:
                send_group(s)
            except ConnectionResetError:
                print("Connection lost")
                return
        else:
            try:
                s.send(bytes(message, "UTF-8"))

                response = str(s.recv(1024).decode()).strip()
            except ConnectionResetError:
                print("Connection to server lost.")
                break

        if not response:
            print("Nothing to see here...")
            break

        if response[0] == "0" and len(response) > 1:
            print("--> " + response[1:])
        elif response[0] == "1":
            print("Error: " + response[1:])
        elif response[0] == "2":
            print("Server ended connection.")
            break

        message = input("-> ")

    s.close()


def send_group(conn):
    conn.send(b"VDOWN\N")

if __name__ == "__main__":
    main()
