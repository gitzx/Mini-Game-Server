# -*- coding: utf-8 -*-

class service(object):
	"""
	服务的基本类
	"""
	def __init__(self, sid = 0):
		self.service_id = sid
		self.command_map = {}

	def register(self, cid, function):
		"""
		注册命令
		"""
		if cid in self.command_map:
			raise Exception('command id ' + cid + 'already registered')
		else:
			self.command_map[cid] = function

	def registers(self, commandDict):
		"""
		注册多条命令
		"""
		for cid in commandDict:
			self.register(cid, commandDict[cid])

	def handle(self, msg, sender):
		"""
		处理消息
		"""
		cid = msg['cid']

		if not cid in self.command_map:
			print 'unknow command id:' + cid
			return None
		f = self.command_map[cid]
		return f(msg, sender)

