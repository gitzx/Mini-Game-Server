# -*- coding:utf-8 -*-

import json
import const
import world
import hashlib

class online_user(object):
	"""
	��¼���������û����û�����
	"""
	def __init__(self):
		self.users = {}
		self.clients = {}

	def refresh_power(self):
		"""
		ˢ�����������û��Ļ���ֵ
		"""
		for user in self.users:
			user_data = self.users[user]
			user_data.refresh_power()

	def _add(self, identification, username, client):
		"""
		���û���½�����������û���
		"""
		if identification in self.users:
			world.battles.remove_battle(identification)
			# TODO remove connection before
			self.clients[identification] = client
		else:
			user = world.db_user_data.get_user_data(username)
			if user == None:
				print "why None?"
			self.users[identification] = user
			self.clients[identification] = client

	def _get_identification(self, username):
		"""
		��ȡidentification
		"""
		identification = hashlib.md5(username).hexdigest().upper()
		identification = identification + username
		return identification

	def add_user(self, username, client):
		# ���û���½
		# TODO �ж��û��Ƿ��ظ���½
		identification = self._get_identification(username)
		self._add(identification, username, client)
		return identification

	def store(self):
		"""
		�洢���������û�������
		"""
		for uid in self.users:
			user = self.users[uid]
			user.store()

	def remove_user(self, identification):
		"""
		�û��˳���½���������û���ɾ��
		"""
		if identification in self.users:
			user = self.users[identification]
			user.store()
			self.users.pop(identification)
		else:
			raise Exception('No user logined with id: ' + identification)

	def get_user(self, identification, sender = None):
		"""
		��identification��ȡ�û�����
		"""
		if (identification in self.users):# and (sender == None or sender == self.clients[identification] ):
			return self.users[identification]
		else:
			return None

	def send_data_one(self, identification, data):
		"""
		����ʱ��һ�������û�����Ϣ
		"""
		try:
			if identification in self.clients:
				client = self.clients[identification]
			else:
				return;
			ret = {const.sid: const.chat_service_id, const.cid: const.chat_command_id, const.result_data_id: data}
			client.send(json.dumps(ret))
		except:
			pass

	def send_data_all(self, data):
		"""
		�����й㲥��Ϣ
		"""
		for cliendID in self.clients:
			self.send_data_one(cliendID, data)

	def get_user_with_name(self, username):
		"""
		���û����û�����ȡ�û���Ϣ
		"""
		identification = self._get_identification(username)
		return self.get_user(identification)

