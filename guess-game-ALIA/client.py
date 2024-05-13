import socket

HOST = "localhost"
PORT = 12345

def connect_to_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((HOST, PORT))
        return s
    except ConnectionRefusedError:
        print("Connection refused. Make sure the server is running.")
        return None

def play_game(s):
    try:
        data = s.recv(1024)
        print(data.decode().strip())
        difficulty_choice = input("").strip()
        s.sendall(difficulty_choice.encode())

        while True:
            user_input = input("").strip()
            s.sendall(user_input.encode())
            reply = s.recv(1024).decode().strip()
            if "Correct" in reply:
                print(reply)
                name = input("Enter your name: ")
                s.sendall(name.encode())
                s.sendall(difficulty_choice.encode())
                break
            print(reply)
    except Exception as e:
        print("An error occurred:", e)

def main():
    while True:
        s = connect_to_server()
        if s:
            play_game(s)
            s.close()

            play_again = input("Do you want to play again? (y/n): ")
            if play_again.lower() != 'y':
                break

if __name__ == "__main__":
    main()
