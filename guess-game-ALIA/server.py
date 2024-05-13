import socket
import random
import json

HOST = '127.0.0.1'
PORT = 12345
BANNER = """
== Guessing Game v1.0 ==
Choose difficulty level:
a - Easy (1-50)
b - Medium (1-100)
c - Hard (1-500)
Enter the letter then press 'enter' two times:"""

DIFFICULTY_RANGES = {
    'a': (1, 50),
    'b': (1, 100),
    'c': (1, 500)
}

def generate_random_int(difficulty):
    return random.randint(*DIFFICULTY_RANGES.get(difficulty, (1, 50)))

def update_leaderboard(name, score, difficulty, leaderboard):
    leaderboard.append({"name": name, "score": score, "difficulty": difficulty})
    leaderboard.sort(key=lambda x: x["score"])
    return leaderboard[:10]

def save_leaderboard(leaderboard):
    with open("leaderboard.json", "w") as f:
        json.dump(leaderboard, f)

def load_leaderboard():
    try:
        with open("leaderboard.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def start_server(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(5)
    print(f"Server is listening on port {port}")

    while True:
        conn, addr = s.accept()
        print(f"New connection from {addr}")

        leaderboard = load_leaderboard()
        conn.sendall(BANNER.encode())

        difficulty = None
        guessme = 0
        tries = 0

        while True:
            client_input = conn.recv(1024).decode().strip()

            if client_input in DIFFICULTY_RANGES:
                difficulty = client_input
                guessme = generate_random_int(difficulty)
                conn.sendall(b"Enter your guess:")
                tries = 0
            elif client_input.isdigit():
                guess = int(client_input)
                tries += 1

                if guess == guessme:
                    conn.sendall(b"Correct Answer!")
                    name = conn.recv(1024).decode().strip()
                    score = tries
                    leaderboard = update_leaderboard(name, score, difficulty, leaderboard)
                    save_leaderboard(leaderboard)
                    conn.sendall(b"\nLeaderboard:\n" + json.dumps(leaderboard).encode())
                    break
                elif guess > guessme:
                    conn.sendall(b"Guess Lower!\nEnter guess: ")
                elif guess < guessme:
                    conn.sendall(b"Guess Higher!\nEnter guess:")
            else:
                conn.sendall(b"Invalid input!\nEnter guess or choose difficulty level:")

        conn.close()

if __name__ == "__main__":
    start_server(HOST, PORT)
