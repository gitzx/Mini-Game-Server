# -*- coding: utf-8 -*-

import random
import world

class hero_heap(object):
	"""
	战斗中的一个队列
	"""
	def __init__(self):
		self.heros = []

	def add_hero(self, hero):
		self.heros.append(hero)

	def get_hero(self):
		"""
		获取正在战斗的卡牌
		"""
		if self.heros.__len__() > 0:
			return self.heros[0]
		else:
			return None
	
	def remove_hero(self, po = 0):
		"""
		删除队列中的一个英雄
		"""
		if po < 0 or po > self.heros.__len__() - 1:
			raise Exception('No hero to remove')
		return self.heros.pop(po)

	def rand_hero(self):
		"""
		把堆中的卡牌随机打乱
		"""
		for (i, hero) in enumerate(self.heros):
			p = random.randint(0, i)
			self.heros[i], self.heros[p] = self.heros[p], self.heros[i]
		#for hero in self.heros:
		#	print '(' + str(hero.hp) + ',' + str(hero.atk) + ') ',
		#print ''
	
	def alive(self):
		"""
		判断堆中是否还有牌
		"""
		return self.heros.__len__() > 0

	def attack(self, team_self, team_target):
		if self.alive():
			return self.heros[0].step(team_self, team_target)
		else:
			return []

	def get_situation(self):
		ret = []
		for hero in self.heros:
			ret.append(hero.get_situation())
		return ret

	def output(self):
		f = file('log.txt', 'a')
		for hero in self.heros:
			print eval('u"' + hero.name + ', hp: "') + str(hero.hp) ,
			name = world.heros.get_hero_card_name(hero.name)
			f.write(name.encode('gbk'))
			f.write(': ' + str(hero.hp) + '\t')
		f.write('\n')
		f.close()
		print ''
