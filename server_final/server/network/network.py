# -*- coding: utf-8 -*-

import socket
import const

class net(object):
	"""
	��������࣬���ڼ����˿ڣ���ȡ�µĿͻ�������
	"""
	def __init__(self, host = None, port = None):
		if host == None:
			host = const.host
		if port == None:
			port = const.port
		self.net = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.net.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.net.bind((host, port))
		self.net.listen(const.client_num)
		self.net.setblocking(0)

	def get_new_connect(self):
		"""
		��ȡ������
		"""
		try:
			client, address = self.net.accept()
			client.setblocking(0)
			return client
		except:
			return None


