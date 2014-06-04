
"""Usage: pic_server.py <address>

"""

import socket
import time
import picamera
import docopt


def run_server(args):
    try:
        server_socket = socket.socket()
        server_socket.bind((args['<address>'], 8000))
        server_socket.listen(0)
    except BaseException:
        print 'failed to opene the socket.'
        print BaseException.message
        return -1
    print 'started up the socket.'

    while True:
        connection = server_socket.accept()[0].makefile('rb')
        print 'accepting a connection.'

        try:
            with picamera.PiCamera() as camera:
                camera.resolution = (640, 480)

                camera.start_preview()
                time.sleep(2)
                print 'starting to record.'
                camera.start_recording(connection, format='h264')
                camera.wait_recording(60)
                camera.stop_recording()
                print 'stopped recording.'
        finally:
            connection.close()
            print 'closed the connection.'

if __name__ == '__main__':
    args = docopt.docopt(__doc__)
    print args
    run_server(args)