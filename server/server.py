
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
	except Exception, e:
		print 'failed to open the socket.'
		print e.message
		return -1
	print 'started up the socket.'
	print 'waiting for a new connection.'

	while True:
		connection = server_socket.accept()[0].makefile('rb')
		print 'accepting a connection.'

		try:
			with picamera.PiCamera() as camera:
				camera.resolution = (1024, 768)
				# automatic mode
				camera.ISO = 0

				print 'showing preview.'
				camera.start_preview()
				time.sleep(2)
				print 'starting to record.'
				try:
					camera.start_recording(connection, format='h264')
					camera.wait_recording(60)
					camera.stop_recording()
				except Exception, e:
					print 'can\'t record properly. maybe the pipe is broken.'
				print 'stopped recording.'
		finally:
			try:
				connection.close()
			except Exception, e:
				print 'can\'t close the connection properly. maybe the pipe is broken.'

		print 'closed the connection.\nwaiting for a new connection.'

if __name__ == '__main__':
	args = docopt.docopt(__doc__)
	print args
	run_server(args)