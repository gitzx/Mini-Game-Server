# -*- coding: utf-8 -*-

import time
import sys

class netstream(object):
	"""
	网络传输类：用于发送和接收消息
	"""
	def __init__(self, client):
		self.client = client
		self.recvbuf = ""
		self.sendbuf = ""
		self.head_len = 4
		self.recv_len = 1024
		self.start_time = time.clock()

	def get_connect_time(self):
		"""
		计算连接时间：
		"""
		return time.clock() - self.start_time

	def try_recv(self):
		try:
			#print 'client = '
			#print self.client
			data = self.client.recv(self.recv_len)
			if not data:
				return None
			else:
				return data
		except:
			#print 'Error when try to recv'
			return None
	
	def get_msg_len(self, msg):
		"""
		分析包的内容，获取包长度
		"""
		ret = 0
		for i in range(self.head_len - 1, -1, -1):
			ret = ret * 256 + ord(msg[i])
		return ret

	def set_msg_len(self, msg_len):
		"""
		在待发送包的开头部分加入包长度
		"""
		ret = []
		for i in range(self.head_len):
			ret.append(chr(msg_len % 256))
			msg_len = msg_len / 256
		#for i in range(self.head_len / 2):
		#	ret[i], ret[self.head_len - i - 1] = ret[self.head_len - i - 1], ret[i]
		return ''.join(ret)

	def recv(self):
		"""
		接收消息
		"""
		try:
			while 1:
				data = self.try_recv()
				if data != None:
					self.recvbuf = self.recvbuf + data
				else:
					break
			if self.recvbuf.__len__() < self.head_len:
				return None
			msg_len = self.get_msg_len(self.recvbuf)
			if msg_len != None and self.recvbuf.__len__() > msg_len + 3:
				ret = self.recvbuf[self.head_len:msg_len + self.head_len]
				self.recvbuf = self.recvbuf[msg_len + self.head_len:]
				print 'recvdata:' + ret
				#print 'recvdata'
				return ret
			else:
				return None
		except:
			print 'Error when recv'
			return None

	def try_send(self):
		if self.sendbuf.__len__() < 1:
			return None
		try:
		#if True:
			#print 'test_begin'
			size = self.client.send(self.sendbuf)
			#print size
			#print self.client
			self.sendbuf = self.sendbuf[size:]
			#print 'test_end'
			return size
		except:
			print 'Error when try to send'
			return 0

	def send(self, msg):
		"""
		发送消息
		"""
		msg_len = msg.__len__()
		print 'senddata:' + msg
		#print 'senddata'
		self.sendbuf = self.sendbuf + self.set_msg_len(msg_len) + msg
		while 1:
			size = self.try_send()
			if not size or size < 1:
				break

	def close(self):
		"""
		关闭连接
		"""
		self.client.close()


