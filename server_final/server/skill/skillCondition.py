# -*- coding: utf-8 -*-

import random
import const

class skill_condition(object):
	def __init__(self):
		pass

	def test(self, _from, _to, harm, death):
		pass

class probability(skill_condition):
	"""
	һ�����ʴ���
	"""
	def __init__(self, pro):
		self.pro = pro

	def test(self, _from, _to, harm = 0, death = 0):
		return random.random() < self.pro

class check_target_race(skill_condition):
	def __init__(self, card_race):
		self.check_race = card_race

	def test(self, _from, _to, harm = 0, death = 0):
		return _to.get_race() == self.check_race

class check_self_race(skill_condition):
	def __init__(self, card_race):
		self.check_race = card_race
	
	def test(self, _from, _to, harm = 0, death = 0):
		return _from.get_race() == self.check_race

class check_target_not_race(skill_condition):
	"""
	�Է��������Ͳ���XXX
	"""
	def __init__(self, card_race):
		self.check_race = card_race

	def test(self, _from, _to, harm = 0, death = 0):
		return _to.get_race() != self.check_race

class check_self_not_race(skill_condition):
	"""
	�����������Ͳ���XXX
	"""
	def __init__(self, card_race):
		self.check_race = card_race
	
	def test(self, _from, _to, harm = 0, death = 0):
		return _from.get_race() != self.check_race

class check_target_hp_less_then_x(skill_condition):
	"""
	���Ŀ��Ѫ���Ƿ�С��ĳ��ֵ
	"""
	def __init__(self, hp_min):
		self.hp_min = hp_min

	def test(self, _from, _to, harm = 0, death = 0):
		return _to.get_hp() <= self.hp_min

class check_death(skill_condition):
	"""
	����Ƿ�ʹ�Է�����
	"""
	def __init__(self):
		pass

	def test(self, _from, _to, harm, death):
		return harm > 0 and death

class check_damage(skill_condition):
	"""
	�ж��Ƿ�����˺�
	"""
	def __init__(self):
		pass

	def test(self, _from, _to, harm, death = 0):
		return harm > 0

class check_hp_self_comp_target(skill_condition):
	"""
	�жϹ�����Ѫ���ͱ�������Ѫ����Ĺ�ϵ
	"""
	def __init__(self, comp):
		self.comp = comp

	def test(self, _from, _to, harm = 0, death = 0):
		if self.comp == const.check_hp_comp_type_self_less:
			return _from.get_hp() < _to.get_hp()
		elif self.comp == const.check_hp_comp_type_self_more:
			return _from.get_hp() > _to.get_hp()
		else:
			raise Exception('unknow type in skill_condition.check_hp_self_comp_target')

