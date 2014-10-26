# -*- coding: utf-8 -*-

import world

class hero_data(object):
	"""
	���ڴ洢Ӣ�ۿ��Ƶ����ݣ��Ա���ս��ʱ�ܿ���ʵ����
	"""
	def __init__(self, heroId, name, level, exp, position):
		self.heroId = heroId
		self.name = name
		self.level = level
		self.exp = exp
		self.position = position

	def set_position(self, position):
		"""
		�����ڶ����е�λ��
		"""
		if position < 0 or position > 2:
			return False
		self.position = position
		return True

	def get_hero(self, baseID = 0):
		"""
		������ʵ����Ϊʵ��ս������
		"""
		if self.position < 0:
			return None
		hero = world.heros.get_hero(self.name, self.level)
		hero.set_id(baseID + 1 + self.position)
		return hero, self.position

	def idle_hero(self):
		"""
		��hero�Ƴ����飬ʹ�䲻����ս��
		"""
		if self.position > -1:
			self.position = -1
			return True
		else:
			return False

	def set_level(self, level):
		"""
		���ÿ��Ƽ���
		"""
		self.level = level

	def set_exp(self, exp):
		"""
		���ÿ��ƾ���
		"""
		self.exp = exp

	#def add_exp(self, exp):
	#	self.exp = self.exp + exp
	#	# TODO test level up

