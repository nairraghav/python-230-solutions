import socket
import sys
import traceback


def server(log_buffer=sys.stderr):
    # set an address for our server
    address = ('127.0.0.1', 10000)
    sock = get_socket(address, log_buffer)

    try:
        # the outer loop controls the creation of new connection sockets. The
        # server will handle each incoming connection one at a time.
        while True:
            # we will be waiting until we get a connection
            print('waiting for a connection', file=log_buffer)

            # accept the connection
            conn, addr = sock.accept()

            try:
                print('connection - {0}:{1}'.format(*addr), file=log_buffer)

                # the inner loop will receive messages sent by the client in
                # buffers.  When a complete message has been received, the
                # loop will exit
                while True:
                    data = conn.recv(16)

                    print('received "{0}"'.format(data.decode('utf8')))
                    conn.sendall(data)
                    print('sent "{0}"'.format(data.decode('utf8')))

                    # check to see if we have less than 16 bytes
                    # this implies the stream is over
                    if len(data) < 16:
                        break
            except Exception as e:
                traceback.print_exc()
                sys.exit(1)
            finally:
                sock.close()
                print(
                    'echo complete, client connection closed', file=log_buffer
                )
                sock = get_socket(address, log_buffer)

    except KeyboardInterrupt:
        sock.close()
        print('quitting echo server', file=log_buffer)


def get_socket(address, log_buffer):
    # we need to re-open the socket so we can accept more connections
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP)

    # this will restart the tcp server if the socket was left open
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # log that we are building a server
    print("making a server on {0}:{1}".format(*address), file=log_buffer)

    # we bind the socket to the address tuple and listen
    sock.bind(address)
    sock.listen(1)
    return sock


if __name__ == '__main__':
    server()
    sys.exit(0)
