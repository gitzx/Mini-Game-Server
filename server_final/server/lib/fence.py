# -*- coding: utf-8 -*-
# 用于记录一个关卡的信息并初始化关卡对战信息

import world
from lib import battleUser
from lib import legend

class fence(object):
	"""
	用于保存一个关卡的战斗信息
	现在主要包括敌人的传奇信息，英雄种类，级别和位置等
	"""
	def __init__(self, level):
		self.level = level
		
		self.legend_name = None
		self.legend = None

		self.heros = []

	def get_enemy(self, star):
		"""
		由之前保存的关卡信息实例化战斗用户信息
		"""
		ret = battleUser.battle_user()
		if star < 0 or star >= self.legend[2].__len__() or star >= self.legend[3].__len__(): # self.legend 的数据结构为[名字，级别，hp，speed]
			raise Exception('star is illegal')
		le = legend.legend(self.legend[0], self.legend[1][star], self.legend[2][star], self.legend[3][star])
		le.set_id(4)
		ret.set_legend(le)
		for hero in self.heros:
			if int(hero[2][star]) < 1: #位置为0，表示在当前星级，该卡片不参战
				continue
			if star < 0 or star >= hero[1].__len__() or star >= hero[2].__len__():
				raise Exception('star is illegal')
			n_hero = world.heros.get_hero(hero[0], hero[1][star])
			n_hero.set_id(4 + hero[2][star])
			ret.add_hero(n_hero, int(hero[2][star]) - 1)
		return ret

	def add_hero(self, hero):
		"""
		添加英雄
		结构：[名字，级别列表，位置列表]
		"""
		self.heros.append(hero)

	def set_legend_name(self, legend_name):
		"""
		设置传奇的显示名称
		"""
		self.legend_name = legend_name

	def set_legend(self, legend):
		"""
		设置实际传奇的数据
		结构：[名字，级别列表，hp列表，speed列表]
		"""
		self.legend = legend

