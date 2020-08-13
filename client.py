import socket

dir_server = ('localhost', 3000)

"""""
Iniciar una partida: para indicarle al servidor que vamos a comenzar a jugar y que
reinicie el número a adivinar, así como el número de intentos del jugador.
 Intentar un número: ya iniciada la partida, en esta opción se le pregunta al usuario
un número entre 0 y 1000, que deberá ser enviado al servidor. Este le responderá
con una pista (algo así como “más” o “menos”) o le indicará que ganó y el número
de intentos que realizó o le indicará que perdió (no adivinó en 10 intentos). En estos
dos últimos momentos, la partida se finalizará y el usuario no deberá poder enviar
nuevos números a menos que inicie una nueva partida.
 Saber cuántos intentos lleva en la partida actual (si la partida no ha sido iniciada,
deberá mostrarse un mensaje al respecto).
 Finalizar el programa
"""

print("-------------------------------------------------------------------------------------------------")
print("--------------------------------------BIENVENIDO-------------------------------------------------")
print("-------------------------------------------------------------------------------------------------\n")

while True:

    print("\n\n1. Start Game\n2. Exit")
    start = input("Enter the corresponding number: ")
    if int(start) == 2:
        print("Come back soon")
        break
    else:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(dir_server)

        # * es Quiero jugar
        sock.sendall("*".encode())
        rta = sock.recv(5)

        if rta > b'0':
            print("\n-------------------------------------------------------------------------------------------------\n")
            print("Game rules:")
            print(">>> You have ", int(rta), "  attempts to guess a number from 0 to 1000")
            print(">>> The system will give you clues for each failed attempt to help you guess the number")

            maxIntentos = int(rta)
            numIntentos = 1
            rtaCmp = ""
            nintentos = ""
            while numIntentos <= maxIntentos:
                num = input("Enter a number: ")
                # Send the number
                sock.sendall(num.encode())

                # Receive reply
                rtaCmp = sock.recv(10)
                if rtaCmp.decode()[0] == "<":
                    nintentos = rtaCmp.decode()[1:]
                    print("Too small, it takes ", nintentos, "attempts")
                    numIntentos += 1
                elif rtaCmp.decode()[0] == ">":
                    nintentos = rtaCmp.decode()[1:]
                    print("Too big, it takes ", nintentos, "attempts")
                    numIntentos += 1
                elif rtaCmp.decode()[0] == "=":
                    nintentos = rtaCmp.decode()[1:]
                    print("\n¡CONGRATULATIONS! You did it in ", nintentos, "attempts")
                    break
                else:
                    print(">>> Error, unexpected response: ", rtaCmp.decode())

            if rtaCmp.decode()[0] != "=":
                print("\n¡YOU LOST! You have made ", nintentos, "attempts")

        sock.close()
