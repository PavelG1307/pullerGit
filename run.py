import socket
import time
import os

proccess = 0
pullServer = f'git -C ../fifth_floor_server pull && cd ../fifth_floor_server && pm2 restart {proccess} && cd ../pullerGit'
pullSite = f'git -C ../fifth_floor pull'
last_update = 0

def start_server(host='127.0.0.1', port=8000):
  global server
  server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server.bind((host, port))
  server.listen(4)
  print('Working...')


def response_text(content='', status=200):
  if status == 200:
    return f'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n{content}'.encode('utf-8')
  elif status == 302:
    return f'HTTP/1.1 302 Found\r\nLocation: {content}'.encode('utf-8')
  elif status == 404:
    return f'HTTP/1.1 404 Not Found'.encode('utf-8')

def pull(server):
  global last_update
  last_update = time.time()
  command = pullServer if server else pullSite
  return os.system(command)

def getpull():
  return last_update

def parse_request(request_data, domain = "127.0.0.1:8080"):
  try:
    method = request_data.split(' ')[0]
    if method == 'GET':
      return getpull(), 200
    elif method == 'POST':
      return pull(True), 200
    elif method == 'PUT':
      return pull(False), 200
  except Exception:
    return '', 404

  return '', 404


def handl():
  client_socket, address = server.accept()
  print(address)
  data = client_socket.recv(1024).decode('utf-8')
  content, status = parse_request(data)
  client_socket.send(response_text(content=content, status=status))


def main():
  start_server()
  while(True):
    handl()


if __name__=='__main__':
  try:
    main()
  except KeyboardInterrupt:
    server.close()