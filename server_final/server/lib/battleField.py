# -*- coding: utf-8 -*-

import xlrd

import battle
import world
import const

class battle_field(object):
	"""
	ս���ࣺ���ڼ�¼�����û���ս��
	"""
	def __init__(self):
		self.battles = {}
		self.hero_table =  world.db_hero

	def add_battle(self, uid, level = [1,1,1]):
		"""
		���һ��ս��
		idΪuid���û���ս�ؿ�level
		level�ṹ��[����,�ؿ�,�Ǽ�]
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
		ս������֮���ս����ɾ��
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
		��ȡ�û����ڲ����ս��
		"""
		return self.battles.get(uid)

