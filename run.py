from hashids import Hashids
import socket
import sqlite3
from cache import Cache_URL


def connect_db():
    global connection, cursor
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS "Url_and_key" ("url"	TEXT UNIQUE)'''
        )
    connection.commit()


def start_server(host='127.0.0.1', port=8080):
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


def add_url(url):
    try:
        cursor.execute(f'''INSERT INTO Url_and_key ('url') VALUES ('{url}');''')
        id = cursor.lastrowid
        connection.commit()
    except sqlite3.IntegrityError:
        cursor.execute(f'''SELECT rowid FROM Url_and_key WHERE url LIKE '{url}';''')
        id = cursor.fetchone()[0]
    key = hashid.encode(id)
    return key


def get_url(key):
    url = cache.get_url(key)
    if url is not None:
        return url
    id = hashid.decode(key)
    if id == ():
        return None
    else:
        id = id[0]
    print('req')
    cursor.execute(f"SELECT url FROM Url_and_key WHERE rowid = {id};")
    url = cursor.fetchone()
    cache.save(key=key, url=url)
    return url


def parse_request(request_data):
    try:
        data = request_data.split(' ')[1]
    except Exception:
        return '', 404
    if data[1] == 'a':
        url = data.split('/a/?url=')[1]
        key = add_url(url)
        return key, 200
    elif data[1] == 's':
        key = data.split('/s/')[1]
        url = get_url(key)
        if url is not None:
            return url[0], 302
    return '', 404


def handl():
    client_socket, address = server.accept()
    data = client_socket.recv(1024).decode('utf-8')
    content, status = parse_request(data)
    client_socket.send(response_text(content=content, status=status))


def main():
    global cache, hashid
    hashid = Hashids(salt="this is my salt", min_length=8)
    cache = Cache_URL(max_lenght=50)
    connect_db()
    start_server()
    while(True):
        handl()


if __name__=='__main__':
    try:
        main()
    except KeyboardInterrupt:
        connection.close()
