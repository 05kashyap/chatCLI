import threading
import socket

# choosing nickname
nickname = input("Choose your nickname: ")

if nickname == 'admin':
    password = input("Enter password for admin:")

# connecting to server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('192.168.56.1', 55555))

stop_thread = True

# listening to Server and Sending Nickname
def receive():
    global stop_thread
    while not stop_thread:
        try:
            # Receive Message From Server
            # If 'NICK' Send Nickname
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
                next_message = client.recv(1024).decode('ascii')
                if next_message == 'PASS':
                    client.send(password.encode('ascii'))
                    if(client.recv(1024).decode('ascii') == 'REFUSE'):
                        print("Wrong password, connection refused.")
                        stop_thread = True
                elif next_message == 'BAN':
                    print("Connection refused because of ban from chat.")
                    client.close()
                    stop_thread = True
            else:
                print(message)
        except:
            # Close Connection When Error
            print("An error occured!")
            client.close()
            connected = False
            break

def write():
    global stop_thread
    while not stop_thread:
        message = '{}: {}'.format(nickname, input(''))
        if message[len(nickname)+2:].startswith('/'):
            if nickname == 'admin':
                if message[len(nickname)+2:].startswith('/kick'):
                    client.send(f'KICK {message[len(nickname)+8:]}'.encode('ascii'))
                elif message[len(nickname)+2:].startswith('/ban'):
                    client.send(f'BAN {message[len(nickname)+7:]}'.encode('ascii'))
            else:
                print("Commands can only be executed by the admin.")
        else:
            client.send(message.encode('ascii'))

# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()