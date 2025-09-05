import socket

class Board:
    def __init__(self, n):
        self.n = n
        self.board=[]
        x = 1
        for i in range(n):
            row=[]
            for j in range(n):
                row.append(str(x))
                x+=1
            self.board.append(row)
        self.currentturn = "X" 

    def printboard(self):
        print(f"\nPlayer {self.currentturn}'s turn - Enter a value between 1 and {n*n}:")
        for i in range(self.n):
            print(" " + " | ".join(self.board[i]))
            if i < self.n - 1:
                print("---+" * (self.n - 1) + "---")

    def strconverter(self):
        boardstr= [",".join(i) for i in self.board]
        boardstr.append(self.currentturn)
        return "\n".join(boardstr)

    def listconverter(self, data):
        rows = data.strip().split("\n")
        self.board = [r.split(",") for r in rows[:-1]]
        self.currentturn = rows[-1]

    def move(self, value):
        m=value-1
        a, b = divmod(m,self.n)
        if self.board[a][b].isdigit():
            self.board[a][b] = self.currentturn
            return True
        else:
            print("Cell already taken!")
            return False

    def winner(self):
        n = self.n
        symbol = self.currentturn

        for r in self.board:
            if all(i == symbol for i in r):
                return True

        for c in range(n):
            if all(self.board[i][c] == symbol for i in range(n)):
                return True

        if all(self.board[i][i] == symbol for i in range(n)) or all(self.board[i][n - 1 - i] == symbol for i in range(n)):
            return True

        return False

    def draw(self):
        return all(not cell.isdigit() for row in self.board for cell in row)

    def turnshifter(self):
        self.currentturn = "O" if self.currentturn == "X" else "X"


host,port = "localhost",2870
n = int(input("Enter number of rows and columns: "))
board = Board(n)

server= socket.socket()
server.bind((host,port))
server.listen()
conn, addr = server.accept()

while True:

    conn.send(board.strconverter().encode())

    if board.currentturn == "O":
        data = conn.recv(4096).decode()
        if not data:
            break
        board.listconverter(data)
        board.printboard()

        if board.winner():
            print("Player O Wins!")
            break
        if board.draw():
            print("Draw!")
            break

        board.turnshifter()

    if board.currentturn == "X":
        board.printboard()
        while True:
            try:
                val = int(input(f"Your move (X) - Enter a value between 1 and {n*n}: "))
                if board.move(val):
                    break
            except:
                pass
            print("Invalid or Taken!")

        if board.winner():
            board.printboard()
            print("Player X Wins!")
            conn.send(board.strconverter().encode())
            break
        if board.draw():
            board.printboard()
            print("Draw!")
            conn.send(board.strconverter().encode())
            break

        board.turnshifter()

conn.close()
server.close()
