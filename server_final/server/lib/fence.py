# -*- coding: utf-8 -*-
# ���ڼ�¼һ���ؿ�����Ϣ����ʼ���ؿ���ս��Ϣ

import world
from lib import battleUser
from lib import legend

class fence(object):
	"""
	���ڱ���һ���ؿ���ս����Ϣ
	������Ҫ�������˵Ĵ�����Ϣ��Ӣ�����࣬�����λ�õ�
	"""
	def __init__(self, level):
		self.level = level
		
		self.legend_name = None
		self.legend = None

		self.heros = []

	def get_enemy(self, star):
		"""
		��֮ǰ����Ĺؿ���Ϣʵ����ս���û���Ϣ
		"""
		ret = battleUser.battle_user()
		if star < 0 or star >= self.legend[2].__len__() or star >= self.legend[3].__len__(): # self.legend �����ݽṹΪ[���֣�����hp��speed]
			raise Exception('star is illegal')
		le = legend.legend(self.legend[0], self.legend[1][star], self.legend[2][star], self.legend[3][star])
		le.set_id(4)
		ret.set_legend(le)
		for hero in self.heros:
			if int(hero[2][star]) < 1: #λ��Ϊ0����ʾ�ڵ�ǰ�Ǽ����ÿ�Ƭ����ս
				continue
			if star < 0 or star >= hero[1].__len__() or star >= hero[2].__len__():
				raise Exception('star is illegal')
			n_hero = world.heros.get_hero(hero[0], hero[1][star])
			n_hero.set_id(4 + hero[2][star])
			ret.add_hero(n_hero, int(hero[2][star]) - 1)
		return ret

	def add_hero(self, hero):
		"""
		���Ӣ��
		�ṹ��[���֣������б�λ���б�]
		"""
		self.heros.append(hero)

	def set_legend_name(self, legend_name):
		"""
		���ô������ʾ����
		"""
		self.legend_name = legend_name

	def set_legend(self, legend):
		"""
		����ʵ�ʴ��������
		�ṹ��[���֣������б�hp�б�speed�б�]
		"""
		self.legend = legend

