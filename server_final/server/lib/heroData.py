# -*- coding: utf-8 -*-

import world

class hero_data(object):
	"""
	用于存储英雄卡牌的数据，以便在战斗时能快速实例化
	"""
	def __init__(self, heroId, name, level, exp, position):
		self.heroId = heroId
		self.name = name
		self.level = level
		self.exp = exp
		self.position = position

	def set_position(self, position):
		"""
		设置在队列中的位置
		"""
		if position < 0 or position > 2:
			return False
		self.position = position
		return True

	def get_hero(self, baseID = 0):
		"""
		由数据实例化为实际战斗对象
		"""
		if self.position < 0:
			return None
		hero = world.heros.get_hero(self.name, self.level)
		hero.set_id(baseID + 1 + self.position)
		return hero, self.position

	def idle_hero(self):
		"""
		将hero移出卡组，使其不参与战斗
		"""
		if self.position > -1:
			self.position = -1
			return True
		else:
			return False

	def set_level(self, level):
		"""
		设置卡牌级别
		"""
		self.level = level

	def set_exp(self, exp):
		"""
		设置卡牌经验
		"""
		self.exp = exp

	#def add_exp(self, exp):
	#	self.exp = self.exp + exp
	#	# TODO test level up

