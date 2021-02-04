# coding: utf-8

import socket
import threading

class SocketServer():
	def __init__(self):
		print("IP�A�h���X���J���}�t���œ��͂��Ă�������")
		addr = input('ip>>')
		print("port�ԍ�����͂��Ă�������")
		port = input('port>>')
		port = int(port)
		self.host = addr
		self.port = port
		self.clients = []
		
	def socket_server_up(self):	
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.bind((self.host, self.port))
		sock.listen(5)
		print("�ڑ��ҋ@��...")
		while True:
			try:
				# �ڑ��v������M
				conn, addr = sock.accept()
			except KeyboardInterrupt:
				break
			# �A�h���X�m�F
			print("[�ڑ�]{}".format(addr))
			# �N���C�A���g��ǉ�
			self.clients.append((conn, addr))
			# �X���b�h�쐬
			thread = threading.Thread(target=self.handler, args=(conn, addr), daemon=True)
			# �X���b�h�X�^�[�g
			thread.start()
			
			print("STX, ETX, CR, LF����͂���ꍇ��<STX>, <ETX>, <CR>, <LF>�Ɠ��͂��Ă�������")
			print("�� : <STX>LOAD000<CR><LF>")
			while True:
				sendMes = input("Server>")
				sendMes = sendMes
				sendMes = sendMes.replace("<STX>", "\x02")
				sendMes = sendMes.replace("<ETX>", "\x03")
				sendMes = sendMes.replace("<CR>", "\r")
				sendMes = sendMes.replace("<LF>", "\n")
				conn.send(sendMes.encode('utf-8'))
			
		
	def close_connection(self, conn, addr):
		print('[�ؒf]{}'.format(addr))
		# �ʐM���Ւf����
		conn.close()
		# �N���C�A���g�����O����
		self.clients.remove((conn, addr))
		
	def handler(self, conn, addr):
		while True:
			try:
				# �N���C�A���g���瑗�M���ꂽ���b�Z�[�W�� 1024 �o�C�g����M
				data = conn.recv(1024)
			except ConnectionResetError:
				# �N���C�A���g���Ń\�P�b�g�������I��(Ctrl + c)�����
				# �\�P�b�g�T�[�o��������������̂ŁA�R�l�N�V������ؒf����
				self.close_connection(conn, addr)
				break
				
			if not data:
				# �f�[�^�������ꍇ�A�ڑ���؂�
				self.close_connection(conn, addr)
				break
			else:
				print('data : {}, addr&port: {}'.format(data, addr))
				

if __name__ == "__main__":
	ss = SocketServer()
	ss.socket_server_up()
	