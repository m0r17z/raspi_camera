
"""Usage: pic_client.py <address>

"""

import socket
import subprocess
import docopt


def run_client(args):
    try:
        client_socket = socket.socket()
        client_socket.connect((args['<address>'], 8000))
    except Exception, e:
        print 'failed to connect.'
        print e.message
        return -1
    print 'successfully connected.'

    connection = client_socket.makefile('wb')

    try:
        print 'starting vlc player.'
        cmdline = ['vlc', '--demux', 'h264', '-']
        player = subprocess.Popen(cmdline, stdin=subprocess.PIPE)

        print 'reading data.'
        while True:
            data = connection.read(1024)
            if not data:
	            print 'data stopped coming in.'
            break
            try:
	            player.stdin.write(data)
            except Exception, e:
	            print 'player is broken.'

    finally:
        connection.close()
        client_socket.close()
        player.terminate()
        print 'closed the connection.'


if __name__ == '__main__':
    args = docopt.docopt(__doc__)
    print args
    run_client(args)