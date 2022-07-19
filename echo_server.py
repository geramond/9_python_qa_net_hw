import socket
import sys

from config import LOCALHOST, random_port

my_socket = socket.socket()

address_and_port = (LOCALHOST, random_port())
# address_and_port = (LOCALHOST, int(sys.argv[1]))
my_socket.bind(address_and_port)
print("Started socket on", address_and_port)

my_socket.listen(10)

conn, addr = my_socket.accept()
print("Got connection", conn, addr)

# Получаем данные из соединения
data = conn.recv(1024)
print("Got data\n", data.decode("utf-8"))
# print(data)


data_list_encoded = []
for i in data.splitlines():
    data_list_encoded.append(i.decode("utf-8"))

method = data_list_encoded.pop(0)
if 'status' in method:
    status = method[method.find('=')+len("="):method.rfind(' HTTP')]
     # method = data_list_encoded.pop(0).split('/')[0].strip()
is_status_invalid = True
if status.isnumeric(): is_status_invalid = False


string_to_send = '\n '.join(data_list_encoded)
if 'status' not in method or is_status_invalid:
    string_to_send+="status: 200\n"
else:
    string_to_send+=f"status: {status}\n"

bytes_string = bytes(string_to_send, 'utf-8')
bytes_method = bytes(method, 'utf-8')

data_amount = my_socket.sendto(bytes_string, addr)
print("Send", data_amount, "bytes")
data_amount = my_socket.sendto(bytes_method, addr)
print("Send", data_amount, "bytes")

my_socket.close()
