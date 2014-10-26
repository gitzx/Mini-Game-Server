#-*- coding: utf-8 -*-

import xlrd
from lib import hero
import const

class raw_hero(object):
	"""
	导入所有英雄卡牌的信息
	"""
	def __init__(self):
		self.hero_datas = {}

	def load(self, filename, table_id = 0):
		"""
		从文件filename中导入第table_id个表
		"""
		data = xlrd.open_workbook(filename)
		table = data.sheets()[table_id]
		self.load_heros(table)

	def get_name(self, table, row):
		name = table.cell(row, 2).value
		return str(int(name))

	def get_card_name(self, table, row):
		card_name = table.cell(row, 3).value
		return card_name

	def get_race(self, table, row):
		race = table.cell(row, 4).value
		return race

	def get_star(self, table, row):
		star = table.cell(row, 5).value
		return star

	def get_atk(self, table, row):
		atk_grow = table.cell(row, 6).value
		atk = table.cell(row, 8).value
		return (atk, atk_grow)

	def get_hp(self, table, row):
		hp_grow = table.cell(row, 7).value
		hp = table.cell(row, 9).value
		return (hp, hp_grow)

	def get_skills(self, table, row):
		ret = []
		for i in xrange(12, 17, 2):
			#print i
			name = table.cell(row, i).value
			level = table.cell(row, i + 1).value
			#print name
			#print level
			if not name:
				ret.append(None)
			else:
				ret.append((name, level))
		return ret

	def load_one_hero(self, table, row):
		"""
		从第row行导出一个英雄卡牌的信息
		"""
		name = self.get_name(table, row)
		race = self.get_race(table, row)
		star = self.get_star(table, row)
		atk = self.get_atk(table, row)
		hp = self.get_hp(table, row)
		skills = self.get_skills(table, row)
		card_name = self.get_card_name(table, row)
		self.hero_datas[name] = [race, star, atk, hp, skills, card_name]

	def load_heros(self, table):
		"""
		在table中导出所有卡牌的信息
		"""
		for i in xrange(1, table.nrows):
			self.load_one_hero(table, i)

	def get_hero_star(self, hero_name):
		"""
		获取卡牌的星级
		"""
		if hero_name in self.hero_datas:
			return self.hero_datas[hero_name][1]
		else:
			return None

	def get_hero_card_name(self, hero_name):
		"""
		获取卡牌名称
		"""
		if hero_name in self.hero_datas:
			return self.hero_datas[hero_name][5]
		else:
			return None

	def get_all_hero(self):
		"""
		获取所有卡牌
		"""
		ret = []
		for hero_name in self.hero_datas:
			ret.append(hero_name)
		return ret

	def get_hero_data(self, hero_name, level):
		"""
		获取卡牌的hp和atk
		"""
		if hero_name in self.hero_datas:
			hero_data = self.hero_datas[hero_name]
			hp = hero_data[3]
			atk = hero_data[2]
			return (hp[0] + hp[1] * level, atk[0] + atk[1] * level)
		else:
			return [0,0]

	def get_hero(self, hero_name, level):
		"""
		由卡牌名字和级别实例化出一个卡牌
		"""
		if hero_name in self.hero_datas:
			hero_data = self.hero_datas[hero_name]
			race = hero_data[0]
			star = hero_data[1]
			atk = hero_data[2]
			hp = hero_data[3]
			skills = hero_data[4]
			ret = hero.hero(hero_name, race, star, level, int(atk[0] + atk[1] * level), int(hp[0] + hp[1] * level))
			for i in xrange(3):
				if level > i * 5 - 1 and skills[i] != None:
					if skills[i][1] != None:
						ret.add_skill(skills[i][0], skills[i][1])
					else:
						ret.add_skill(skills[i][0])
			return ret
		else:
			print eval('u"' + hero_name + '"')
			raise Exception('unknow hero name: ' + hero_name)

if __name__ == '__main__':
	test = raw_hero()
	test.load(const.hero_filename)


