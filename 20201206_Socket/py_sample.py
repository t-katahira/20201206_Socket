# coding: utf-8

import socket
import threading

class SocketServer():
	def __init__(self):
		print("IPアドレスをカンマ付きで入力してください")
		addr = input('ip>>')
		print("port番号を入力してください")
		port = input('port>>')
		port = int(port)
		self.host = addr
		self.port = port
		self.clients = []
		
	def socket_server_up(self):	
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.bind((self.host, self.port))
		sock.listen(5)
		print("接続待機中...")
		while True:
			try:
				# 接続要求を受信
				conn, addr = sock.accept()
			except KeyboardInterrupt:
				break
			# アドレス確認
			print("[接続]{}".format(addr))
			# クライアントを追加
			self.clients.append((conn, addr))
			# スレッド作成
			thread = threading.Thread(target=self.handler, args=(conn, addr), daemon=True)
			# スレッドスタート
			thread.start()
			
			print("STX, ETX, CR, LFを入力する場合は<STX>, <ETX>, <CR>, <LF>と入力してください")
			print("例 : <STX>LOAD000<CR><LF>")
			while True:
				sendMes = input("Server>")
				sendMes = sendMes
				sendMes = sendMes.replace("<STX>", "\x02")
				sendMes = sendMes.replace("<ETX>", "\x03")
				sendMes = sendMes.replace("<CR>", "\r")
				sendMes = sendMes.replace("<LF>", "\n")
				conn.send(sendMes.encode('utf-8'))
			
		
	def close_connection(self, conn, addr):
		print('[切断]{}'.format(addr))
		# 通信を遮断する
		conn.close()
		# クライアントを除外する
		self.clients.remove((conn, addr))
		
	def handler(self, conn, addr):
		while True:
			try:
				# クライアントから送信されたメッセージを 1024 バイトずつ受信
				data = conn.recv(1024)
			except ConnectionResetError:
				# クライアント側でソケットを強制終了(Ctrl + c)すると
				# ソケットサーバが処理落ちするので、コネクションを切断する
				self.close_connection(conn, addr)
				break
				
			if not data:
				# データが無い場合、接続を切る
				self.close_connection(conn, addr)
				break
			else:
				print('data : {}, addr&port: {}'.format(data, addr))
				

if __name__ == "__main__":
	ss = SocketServer()
	ss.socket_server_up()
	