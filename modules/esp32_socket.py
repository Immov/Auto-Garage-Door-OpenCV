import socket

HOST = "192.168.4.1"  # The IP address of the ESP32
PORT = 80  # The port that the ESP32 is listening on

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

while True:
    message = input("Enter a message to send: ")
    s.send(message.encode())
    data = s.recv(1024).decode()
    print(f"Received: {data}")

s.close()
