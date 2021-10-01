import bunny
import socket


def serve():
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

    s = socket.socket()
    s.bind(addr)
    s.listen(1)

    print('listening on', addr)

    while True:
        cl, addr = s.accept()
        print('client connected from', addr)
        cl_file = cl.makefile('rwb', 0)
        get = False
        post = False
        while True:
            line = cl_file.readline()
            if line.startswith('GET / '):
                get = True
            elif line.startswith('POST /'):
                line = line.decode('utf-8')
                r, g, b = line.split('/')[1:4]
                bunny.setColor((int(r), int(g), int(b)))
                bunny.draw()
                post = True
            if not line or line == b'\r\n':
                break
        if get:
            cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
            cl.sendall(open('index.html').read())
        if post:
            cl.send('HTTP/1.0 204 No Content')
        cl.close()
