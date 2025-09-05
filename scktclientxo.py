import socket

host=input("Server IP: ")
port=2870

client= socket.socket()
client.connect((host,port))

while True:

    str = client.recv(4096).decode()
    
    row= str.strip().split("\n")
    board= row[:-1]  
    designboard=[i.split(",") for i in row[:-1]]  
    current = row[-1]      
    n = len(board)

    print(f"\nPlayer {current}'s turn:")
    for i in range(n):
            print(" " + " | ".join(designboard[i]))
            if i < n - 1:
                print("---+" * (n - 1) + "---")

    if current== "O":
        while True:
            try:
                value = int(input(f"Enter your move (O) - Enter a value between 1 and {n*n}:"))
                m=value-1
                a, b = divmod(m,n)
                rlist = board[a].split(",")
                if rlist[b].isdigit():
                    rlist[b] = "O"
                    board[a] = ",".join(rlist)
                    break
            except :
                pass
            print("Enter a valid number.")

        clientboard=clientboard = "\n".join(board) + f"\n{current}"
        client.send(clientboard.encode())

client.close()
