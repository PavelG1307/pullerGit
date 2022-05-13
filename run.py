import random
import socket
import sqlite3
import string

def connect_db():
    global connection, cursor
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

def start_server():
    global server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 8080))
    server.listen(4)
    print('Working...')
    
    
def response_text(content ='', status = 200):
    if status == 200:
        return f'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n{content}'.encode('utf-8')
    elif status == 302:
        return f'HTTP/1.1 302 Found\r\nLocation: {content}'.encode('utf-8')
    elif status == 404:
        return f'HTTP/1.1 404 Not Found'.encode('utf-8')
    
def check_url(url):
    cursor.execute(f"SELECT key FROM Url_and_key WHERE url LIKE '{url}';")
    result = cursor.fetchall()
    if result == []:
        return None
    return result[0][0]

def check_key(key):
    cursor.execute(f"SELECT COUNT(*) FROM Url_and_key WHERE key LIKE '{key}';")
    if cursor.fetchall()[0][0] == 0:
        return True
    return False

def add_url(url):
    key = check_url(url)
    if key is None:
        key = generate_key()
        cursor.execute(f"INSERT INTO Url_and_key ('key', 'url') VALUES ('{key}', '{url}');")
        connection.commit()
    return key

def get_url(key):
    cursor.execute(f"SELECT url FROM Url_and_key WHERE key LIKE '{key}';")
    url = cursor.fetchall()
    if url != []:
        return url[0][0]
    return None

def generate_key():
    dictionary = list(string.ascii_lowercase + string.ascii_uppercase) + ['0','1','2','3','4','5','6','7','8','9']
    key = ''
    for i in range(8):
        key+=random.choice(dictionary)
    if check_key(key):
        return(key)
    else:
        generate_key()
        # По хорошему надо сделать ограничение от случая, когда будут заняты все ключи
        # Но вероятность такой ситуации в наших масштабах около нуля
    
def parse_request(request_data):
    data = request_data.split(' ')[1]
    if data[1] == 'a':
        url = data.split('/a/?url=')[1]
        key = add_url(url)
        return key, 200
    elif data[1] == 's':
        key = data.split('/s/')[1]
        url = get_url(key)
        return url, 302
    return '', 200

def handl():
    client_socket, address = server.accept()
    data = client_socket.recv(1024).decode('utf-8')
    content, status = parse_request(data)
    client_socket.send(response_text(content = content, status = status))



def main():
    connect_db()
    start_server()
    while(True):
        handl()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    