# -*- coding:utf-8 -*-

import world
import const
from accountService import account_service
from battleService import battle_service
from friendService import friend_service
from pvpService import pvp_service
from heroService import hero_service
from chatService import chat_service

class main_service(object):
	"""
	将消息分发给不同的Service
	"""
	def __init__(self):
		self.account = account_service()
		self.battle = battle_service()
		self.friend = friend_service()
		self.pvp = pvp_service()
		self.hero = hero_service()
		self.chat = chat_service()

	def handle(self, msg, sender):
		try:
			identification = msg.get(const.identification_id)
			if identification != None:
				user = world.onlineUsers.get_user(identification)
				if user != None:
					# 包验证通过
					if msg.get(const.sid) == const.battle_service_id:
						print 'battle'
						#msg[const.username_data_id] = username
						self.battle.handle(msg, sender)
					if msg.get(const.sid) == const.friend_service_id:
						print 'friend'
						self.friend.handle(msg, sender)
					if msg.get(const.sid) == const.pvp_service_id:
						print 'pvp'
						self.pvp.handle(msg, sender)
					if msg.get(const.sid) == const.update_service_id:
						print 'update'
						self.hero.handle(msg, sender)
					if msg.get(const.sid) == const.chat_service_id:
						print 'chat'
						self.chat.handle(msg, sender)
			elif msg.get(const.sid) == const.account_service_id:
				self.account.handle(msg, sender)
			else:
				# 不合法数据
				pass
		except:
			pass


