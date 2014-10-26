# -*- coding: utf-8 -*-

import xlrd
import random
import world
import const

class reward(object):
	"""
	从excel文件中导出通关奖励信息
	"""
	def __init__(self):
		self.raw_reward = {}
		self.hero_set_star = [[], [], [], [], []]
		all_hero = world.heros.get_all_hero()
		for hero in all_hero:
			self.hero_set_star[int(world.heros.get_hero_star(hero)) - 1].append(hero)

	def get_level(self, table, row):
		"""
		关卡
		"""
		scene = int(table.cell(row, 0).value)
		level = int(table.cell(row, 1).value)
		return (scene, level)

	def get_exp(self, table, row):
		exp1 = table.cell(row, 2).value
		exp2 = table.cell(row, 3).value
		exp3 = table.cell(row, 4).value
		return (exp1, exp2, exp3)

	def get_gold(self, table, row):
		gold1 = table.cell(row, 5).value
		gold2 = table.cell(row, 6).value
		gold3 = table.cell(row, 7).value
		return (gold1, gold2, gold3)

	def get_hero(self, table, row):
		"""
		获取奖励的卡牌
		"""
		hero_name1 = table.cell(row, 8).value
		if not hero_name1:
			hero_name1 = None
		else:
			hero_name1 = str(int(hero_name1))
		hero_name2 = table.cell(row, 9).value
		if not hero_name2:
			hero_name2 = None
		else:
			hero_name2 = str(int(hero_name2))
		hero_name3 = table.cell(row, 10).value
		if not hero_name3:
			hero_name3 = None
		else:
			hero_name3 = str(int(hero_name3))
		return (hero_name1, hero_name2, hero_name3)

	def get_star_ratio(self, table, row):
		"""
		奖励卡牌的星级分布
		"""
		ratio1 = table.cell(row, 11).value
		ratio2 = table.cell(row, 12).value
		ratio3 = table.cell(row, 13).value
		return (ratio1, ratio2, ratio3)

	def load(self, filename, sheet_id):
		"""
		从文件filename中的sheet_id表中导出数据
		"""
		data = xlrd.open_workbook(filename)
		table = data.sheets()[sheet_id]

		for i in xrange(2, table.nrows):
			level = self.get_level(table, i)
			#print level
			exp = self.get_exp(table, i)
			#print exp
			gold = self.get_gold(table, i)
			#print gold
			star_ratio = self.get_star_ratio(table, i)
			#print star_ratio
			hero = self.get_hero(table, i)
			#print hero
			self.raw_reward[level] = [exp, gold, hero, star_ratio]
	
	def get_reward(self, scene, level, star, firstTime, win):
		"""
		计算战斗后的奖励
		"""
		#return (0, 0, None)
		exp = self.raw_reward[(scene, level)][0][star]
		r = random.random()
		r = (r-0.5)/5
		exp = int(exp * (1 + r))
		gold = self.raw_reward[(scene, level)][1][star]
		r = random.random()
		r = (r-0.5)/5
		gold = int(gold * (1 + r))
		if not win:
			return (exp/5, gold/5, None)
		hero = self.raw_reward[(scene, level)][2][star]
		if firstTime and hero:
			return (exp, gold, hero)
		if random.random() > const.probability_of_new_hero[star]:
			return (exp, gold, None)
		else:
			ratio = self.raw_reward[(scene, level)][3]
			p = random.random()
			for i in range(ratio.__len__()):
				if p < ratio[i]:
					hero = random.choice(self.hero_set_star[i])
					return (exp, gold, hero)
				else:
					p = p - ratio[i]
			raise Exception('ratio to get card Error')

if __name__ == '__main__':
	re = reward()
	re.load('reward.xlsx', 0)
	print 'reward = ',
	print re.get_reward(1, 2, 2, False)

