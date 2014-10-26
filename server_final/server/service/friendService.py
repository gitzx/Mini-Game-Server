# -*- coding: utf-8 -*-

import json
import world
import const
import service

class friend_service(service.service):
	"""
	处理用户关于好友的请求
	"""
	def __init__(self):
		super(friend_service, self).__init__(const.friend_service_id)
		commands = {
				const.friend_add: self.handle_add_friend,
				const.friend_remove: self.handle_remove_friend,
				const.friend_get: self.handle_get_friend,
				const.friend_get_random: self.handle_get_random_user,
				}
		self.registers(commands)

		friend_db = world.db_friend

	def handle_add_friend(self, msg, sender):
		"""
		添加好友
		"""
		identification = msg.get(const.identification_id)
		user = world.onlineUsers.get_user(identification, sender)
		if not user:
			return
		friend = msg.get(const.friend_data_id)
		result = user.add_friend(friend)
		if result:
			ret = {const.sid: const.friend_service_id, const.cid: const.friend_add, const.result_data_id: result}
			sender.send(json.dumps(ret))
			world.logger.append('friend+ ' + identification + ', ' + friend)
		else:
			print 'illegal add friend command'

	def handle_remove_friend(self, msg, sender):
		"""
		删除好友
		"""
		identification = msg.get(const.identification_id)
		user = world.onlineUsers.get_user(identification, sender)
		if not user:
			return
		friend = msg.get(const.friend_data_id)
		result = user.remove_friend(friend)
		if result:
			ret = {const.sid: const.friend_service_id, const.cid: const.friend_remove, const.result_data_id: result}
			sender.send(json.dumps(ret))
			world.logger.append('friend- ' + identification + ', ' + friend)
		else:
			print 'illegal remove friend command'

	def handle_get_friend(self, msg, sender):
		"""
		获取好友列表
		"""
		identification = msg.get(const.identification_id)
		user = world.onlineUsers.get_user(identification, sender)
		if not user:
			return
		users = user.get_friends()
		ret = {const.sid: const.friend_service_id, const.cid: const.friend_get, const.result_data_id: users}
		sender.send(json.dumps(ret))
		# TODO: return friend list

	def handle_get_random_user(self, msg, sender):
		"""
		随机选择一定量的非好友用户
		"""
		identification = msg.get(const.identification_id)
		user = world.onlineUsers.get_user(identification, sender)
		if not user:
			return
		users = user.get_random_user()
		ret = {const.sid: const.friend_service_id, const.cid: const.friend_get_random, const.result_data_id: users}
		sender.send(json.dumps(ret))

