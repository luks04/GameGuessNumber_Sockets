import socket
import random

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_adress = ('localhost', 3000)
sock.bind(server_adress)

def generateNum():
    return random.randint(0, 1000)

sock.listen(1)
while True:
    print("Waiting players ...")
    (conexion, cliente) = sock.accept()

    msg = conexion.recv(1)
    print(msg)
    if msg.decode() == "*":

        """Start Game"""

        # Generate winning number
        winnerNum = generateNum()
        # Reset number of attempts
        maxIntentos = 10

        print("---------- WINNER NUM & ATTEMPTS ----------", winnerNum, "----------", maxIntentos)

        # Ready to play
        conexion.sendall(str(maxIntentos).encode())

        numIntentos = 1
        while numIntentos <= 10:
            num = conexion.recv(5)
            print("---------- CLIENT NUM & ATTEMPTS ----------", int(num), "----------", numIntentos)

            if int(num) < winnerNum:
                conexion.sendall(("<" + str(numIntentos)).encode())
            elif int(num) > winnerNum:
                conexion.sendall((">" + str(numIntentos)).encode())
            else:
                conexion.sendall(("=" + str(numIntentos)).encode())
                break

            # Decrease number of current attempts
            numIntentos += 1

        # Attempts are over
        conexion.close()
