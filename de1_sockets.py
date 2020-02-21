from socket import *
import _thread
import os

host = '192.168.0.200'
port = 8080
server_addr = (host, port)

def send_image_data(img_path, palette_path):
    global server_addr
    
    img = open(img_path, "rb").read()
    img_header = (str(len(img)).zfill(10)).encode()

    palette = open(palette_path, "rb").read()
    palette_header = (str(len(palette)).zfill(10)).encode()
    
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    
    server_socket.bind(server_addr)
    server_socket.listen(1)
     
    print("The server socket is now listening")
    
    connection, addr = server_socket.accept()
    
    connection.send(img_header)
    connection.send(img)
    
    connection.send(palette_header)
    connection.send(palette)
     
    server_socket.close()

    print("Finished sending image data, the server socket is now closed")
    
    _thread.exit()