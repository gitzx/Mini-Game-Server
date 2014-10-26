# -*- coding: utf-8 -*-

import socket
import const

class net(object):
	"""
	网络基础类，用于监听端口，获取新的客户端连接
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
		获取新连接
		"""
		try:
			client, address = self.net.accept()
			client.setblocking(0)
			return client
		except:
			return None


