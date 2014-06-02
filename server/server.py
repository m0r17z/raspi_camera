
"""Usage: pic_server.py <address>

"""

import socket
import time
import picamera
import docopt


def run_server(args):
    server_socket = socket.socket()
    server_socket.bind((args['<address>'], 8000))
    server_socket.listen(0)

    connection = server_socket.accept()[0].makefile('rb')

    try:
        with picamera.PiCamera() as camera:
            camera.resolution = (640, 480)

            camera.start_preview()
            time.sleep(2)

            camera.start_recording(connection, format='h264')
            camera.wait_recording(60)
            camera.stop_recording()
    finally:
        connection.close()
        server_socket.close()

if __name__ == '__main__':
    args = docopt.docopt(__doc__)
    print args
    run_server(args)