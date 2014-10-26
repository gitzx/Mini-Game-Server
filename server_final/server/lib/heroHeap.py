# -*- coding: utf-8 -*-

import random
import world

class hero_heap(object):
	"""
	ս���е�һ������
	"""
	def __init__(self):
		self.heros = []

	def add_hero(self, hero):
		self.heros.append(hero)

	def get_hero(self):
		"""
		��ȡ����ս���Ŀ���
		"""
		if self.heros.__len__() > 0:
			return self.heros[0]
		else:
			return None
	
	def remove_hero(self, po = 0):
		"""
		ɾ�������е�һ��Ӣ��
		"""
		if po < 0 or po > self.heros.__len__() - 1:
			raise Exception('No hero to remove')
		return self.heros.pop(po)

	def rand_hero(self):
		"""
		�Ѷ��еĿ����������
		"""
		for (i, hero) in enumerate(self.heros):
			p = random.randint(0, i)
			self.heros[i], self.heros[p] = self.heros[p], self.heros[i]
		#for hero in self.heros:
		#	print '(' + str(hero.hp) + ',' + str(hero.atk) + ') ',
		#print ''
	
	def alive(self):
		"""
		�ж϶����Ƿ�����
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
