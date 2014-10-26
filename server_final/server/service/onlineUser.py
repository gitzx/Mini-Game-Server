# -*- coding:utf-8 -*-

import json
import const
import world
import hashlib

class online_user(object):
	"""
	记录所有在线用户的用户数据
	"""
	def __init__(self):
		self.users = {}
		self.clients = {}

	def refresh_power(self):
		"""
		刷新所有在线用户的活力值
		"""
		for user in self.users:
			user_data = self.users[user]
			user_data.refresh_power()

	def _add(self, identification, username, client):
		"""
		新用户登陆，加入在线用户中
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
		获取identification
		"""
		identification = hashlib.md5(username).hexdigest().upper()
		identification = identification + username
		return identification

	def add_user(self, username, client):
		# 新用户登陆
		# TODO 判断用户是否重复登陆
		identification = self._get_identification(username)
		self._add(identification, username, client)
		return identification

	def store(self):
		"""
		存储所有在线用户的数据
		"""
		for uid in self.users:
			user = self.users[uid]
			user.store()

	def remove_user(self, identification):
		"""
		用户退出登陆，从在线用户中删除
		"""
		if identification in self.users:
			user = self.users[identification]
			user.store()
			self.users.pop(identification)
		else:
			raise Exception('No user logined with id: ' + identification)

	def get_user(self, identification, sender = None):
		"""
		由identification获取用户数据
		"""
		if (identification in self.users):# and (sender == None or sender == self.clients[identification] ):
			return self.users[identification]
		else:
			return None

	def send_data_one(self, identification, data):
		"""
		聊天时向一个在线用户发消息
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
		聊天中广播消息
		"""
		for cliendID in self.clients:
			self.send_data_one(cliendID, data)

	def get_user_with_name(self, username):
		"""
		由用户的用户名获取用户信息
		"""
		identification = self._get_identification(username)
		return self.get_user(identification)

