# -*- coding: utf-8 -*-

import xlrd

import battle
import world
import const

class battle_field(object):
	"""
	战场类：用于记录所有用户的战斗
	"""
	def __init__(self):
		self.battles = {}
		self.hero_table =  world.db_hero

	def add_battle(self, uid, level = [1,1,1]):
		"""
		添加一场战斗
		id为uid的用户挑战关卡level
		level结构：[场景,关卡,星级]
		"""
		if uid in self.battles:
			print 'user ' + uid + ' already in a battle, have no time to attend another'
			return None
		player_data = world.onlineUsers.get_user(uid)
		if not player_data.test_battle_level(level):
			print 'level not allowed'
			return None
		if not player_data.cost_power(const.power_cost_per_fight):
			return None
		player = player_data.get_battle_user()
		if level[0] < 0:
			return None
		else:
			computer = world.all_fences.get_guard(level[0], level[1], level[2])
		if not player:
			return None
		if not computer:
			return None

		battle1 = battle.battle(player, computer)
		self.battles[uid] = battle1
		battle1.set_level(level)
		return battle1

	def remove_battle(self, uid):
		"""
		战斗结束之后从战场中删除
		"""
		try:
			if uid in self.battles:
				self.battles.pop(uid)
				return True
			else:
				return False
		except:
			return False

	def get_battle(self, uid):
		"""
		获取用户正在参与的战斗
		"""
		return self.battles.get(uid)

