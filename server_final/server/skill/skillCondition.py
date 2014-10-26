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
	一定概率触发
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
	对方种族类型不是XXX
	"""
	def __init__(self, card_race):
		self.check_race = card_race

	def test(self, _from, _to, harm = 0, death = 0):
		return _to.get_race() != self.check_race

class check_self_not_race(skill_condition):
	"""
	己方种族类型不是XXX
	"""
	def __init__(self, card_race):
		self.check_race = card_race
	
	def test(self, _from, _to, harm = 0, death = 0):
		return _from.get_race() != self.check_race

class check_target_hp_less_then_x(skill_condition):
	"""
	检查目标血量是否小于某个值
	"""
	def __init__(self, hp_min):
		self.hp_min = hp_min

	def test(self, _from, _to, harm = 0, death = 0):
		return _to.get_hp() <= self.hp_min

class check_death(skill_condition):
	"""
	检查是否使对方死亡
	"""
	def __init__(self):
		pass

	def test(self, _from, _to, harm, death):
		return harm > 0 and death

class check_damage(skill_condition):
	"""
	判断是否造成伤害
	"""
	def __init__(self):
		pass

	def test(self, _from, _to, harm, death = 0):
		return harm > 0

class check_hp_self_comp_target(skill_condition):
	"""
	判断攻击者血量和被攻击者血量间的关系
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

