# -*- coding: utf-8 -*-

class service(object):
	"""
	����Ļ�����
	"""
	def __init__(self, sid = 0):
		self.service_id = sid
		self.command_map = {}

	def register(self, cid, function):
		"""
		ע������
		"""
		if cid in self.command_map:
			raise Exception('command id ' + cid + 'already registered')
		else:
			self.command_map[cid] = function

	def registers(self, commandDict):
		"""
		ע���������
		"""
		for cid in commandDict:
			self.register(cid, commandDict[cid])

	def handle(self, msg, sender):
		"""
		������Ϣ
		"""
		cid = msg['cid']

		if not cid in self.command_map:
			print 'unknow command id:' + cid
			return None
		f = self.command_map[cid]
		return f(msg, sender)

