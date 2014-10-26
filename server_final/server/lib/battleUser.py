# -*- coding: utf-8 -*-

import const
from lib import heroHeap

class battle_user(object):
	"""
	战斗中的一方
	"""
	def __init__(self):
		self.heros = []
		self.legend = None
		self.heaps = []
		self.graveyard = heroHeap.hero_heap()

	def set_legend(self, legend):
		self.legend = legend
	
	def get_legend(self):
		return self.legend
	
	def add_hero(self, hero, heap):
		hero.set_heap(heap)
		self.heros.append(hero)

	def move(self, _from, _to):
		"""
		战斗中移动卡牌
		"""
		for test in (_from, _to):
			if self.heaps[test[0]].alive() and not self.heaps[test[0]].heros[0].alive():
				test[1] = test[1] + 1

			if test[0] < 0 or test[0] > 2:
				return 
			if test[1] < 0 or test[1] + 1 >= self.heaps[test[0]].heros.__len__():
				return
		tmp = self.heaps[_from[0]].heros.pop(_from[1] + 1)
		tmp.set_heap(_to[0])
		tmp.set_id(1 + _to[0])
		self.heaps[_to[0]].heros[_to[1]+1:_to[1]+1] = [tmp]

	def rand_hero(self):
		"""
		随机打乱牌堆
		"""
		for heap in self.heaps:
			heap.rand_hero()

	def init_heap(self):
		"""
		初始化牌堆
		"""
		for i in range(const.num_of_heap):
			self.heaps.append(heroHeap.hero_heap())
		for hero in self.heros:
			p = hero.get_heap()
			self.heaps[p].add_hero(hero)
		self.rand_hero()

	def attack(self, enemy, canAttack = True):
		"""
		己方攻击回合
		"""
		ret = []
		if not canAttack:
			if self.legend.get_id() < 1:
				ret.append([{'type': 'sideBegin', 'user' : 'player'}])
			else:
				ret.append([{'type': 'sideBegin', 'user' : 'enemy'}])
			return ret
		for (i, hero) in enumerate(self.heaps):
			attack_hero = self.heaps[i].get_hero()
			if attack_hero == None:
				continue
			elif not attack_hero.alive():
				self.heaps[i].remove_hero()
				attack_hero = self.heaps[i].get_hero()
				if attack_hero:
					process = attack_hero.enter(self, enemy)
					process1 = self.heaps[i].attack(self, enemy)
					process.extend(process1)
					if process.__len__() > 0:
						ret.append(process)
			else:
				process = self.heaps[i].attack(self, enemy)
				if process.__len__() > 0:
					ret.append(process)
		if self.legend.get_id() < 1:
			ret.append([{'type': 'sideBegin', 'user' : 'enemy'}])
		else:
			ret.append([{'type': 'sideBegin', 'user' : 'player'}])
		return ret

	def get_hero(self, po):
		"""
		获取第po列的战斗中卡牌
		"""
		return self.heaps[po].get_hero()

	def get_speed(self):
		return self.legend.get_speed()

	def alive(self):
		"""
		判断本方是否还存活
		"""
		if self.legend.alive():
			return True
		else:
			return False

	def get_situation(self):
		"""
		获取状态
		"""
		return {'legend': self.legend.get_situation(), '0': self.heaps[0].get_situation(), '1': self.heaps[1].get_situation(), '2': self.heaps[2].get_situation()}

	def output(self):
		f = file('log.txt', 'a')
		f.write('legend: ')
		f.write(str(self.legend.hp) + '\n')
		f.close()
		print 'legend: ',
		print self.legend.hp
		for heap in self.heaps:
			heap.output()

