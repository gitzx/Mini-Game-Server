# -*- coding: utf-8 -*-

import const
import json
import time

class connection_pool(object):
	"""
	网络连接池，保存所有建立的连接
	"""
	def __init__(self):
		self.clients = []
		self.status = 0

	def add_connection(self, client):
		"""
		加入新连接到连接池
		"""
		self.clients.append(client)
		self.click()

	def remove_connection(self, index = 0):
		"""
		删除第index个网络连接
		"""
		if index < 0 or index > self.clients.__len__() - 1:
			return False
		try:
			self.clients[index].close()
			self.clients.pop(index)
			return True
		except:
			return False

	def click(self):
		"""
		删除所有过期的连接
		"""
		#print 'len = ' + str(self.clients.__len__())
		while self.clients.__len__() > 0 and self.clients[0].get_connect_time() > const.connection_keep_time:
			self.remove_connection(0)
		while self.clients.__len__() > const.client_num:
			self.remove_connection(0)

	def recv(self):
		"""
		遍历所有连接，取出下一条消息
		"""
		checked_client = 0
		while 1:
			if self.clients.__len__() < 1:
				time.sleep(0.5)
				yield (None, None)
			for client in self.clients:
				client.try_send()
				data = client.recv()
				if data:
					checked_client = 0
					#client.send(str(self.clients.__len__()))
					yield (client, data)
				else:
					checked_client = checked_client + 1
				if checked_client >= self.clients.__len__():
					time.sleep(0.5)
					checked_client = 0
					yield (None, None)

