# -*- coding: utf-8 -*-

import xlrd
import const
import world

class hero_upgrade(object):
	"""
	卡牌升级
	"""
	def __init__(self):
		"""
		初始化吃其他卡牌可以获得的经验和升级所需的经验
		"""
		data = xlrd.open_workbook(const.hero_upgrade_filename)
		table = data.sheets()[0]
		self.exp_needed = []
		for i in xrange(1, table.nrows):
			exp = table.cell(i, 2).value
			if exp != "":
				self.exp_needed.append(int(exp))
		table = data.sheets()[1]
		self.exp_earn = []
		for i in xrange(5):
			tmp_exp_earn = []
			for j in xrange(5):
				exp = int(table.cell(2 + i, 1 + j).value)
				tmp_exp_earn.append(exp)
			self.exp_earn.append(tmp_exp_earn)

		self.exp_append = []
		for i in xrange(5):
			exp = int(table.cell(9 + i, 1).value)
			self.exp_append.append(exp)

	def get_exp(self, upgrade_hero, food_hero):
		"""
		计算吃牌获得的经验
		"""
		name1 = upgrade_hero.name
		name2 = food_hero.name

		star1 = world.heros.get_hero_star(name1)
		star2 = world.heros.get_hero_star(name2)

		star1 = int(float(star1)) - 1
		star2 = int(float(star2)) - 1

		ret = 0
		ret = ret + self.exp_earn[star1][star2]

		if name1 == name2:
			ret = ret + self.exp_append[star1]
		return ret

	def get_exps(self, upgrade_hero, food_heros):
		"""
		计算吃多张卡牌获得的经验
		"""
		ret = 0
		for hero in food_heros:
			ret = ret + self.get_exp(upgrade_hero, hero)
		return ret

	def upgrade(self, user_data, upgrade_hero, food_heros):
		"""
		user_data的upgrade_hero卡牌吃掉food_heros中所有卡牌的升级情况
		"""
		exp = self.get_exps(upgrade_hero, food_heros)
		for hero in food_heros:
			user_data.remove_hero(hero.heroId)

		exp = exp + upgrade_hero.exp
		level = upgrade_hero.level

		while level < self.exp_needed.__len__() and exp >= self.exp_needed[level]:
			exp = exp - self.exp_needed[level]
			level = level + 1

		upgrade_hero.set_level(level)
		upgrade_hero.set_exp(exp)

