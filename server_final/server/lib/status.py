# -*- coding: utf-8 -*-

import const

class status(object):
	"""
	×´Ì¬Àà
	"""
	def __init__(self, name, can_move, can_magic, can_attack, harm_type, harm_before_move, harm_after_move, harm_when_attacked, last_time, can_add_hp):
		self.name = name
		self.can_move = can_move
		self.can_magic = can_magic
		self.can_attack = can_attack
		self.harm_type = harm_type
		self.harm_before_move = harm_before_move
		self.harm_after_move = harm_after_move
		self.harm_when_attacked = harm_when_attacked
		self.last_time = last_time
		self.can_add_hp = can_add_hp

	def get_harm_before_move(self, hp_max):
		if self.harm_type == const.status_harm_type_const:
			return self.harm_before_move
		elif self.harm_type == const.status_harm_type_ratio:
			return self.harm_before_move * hp_max
		else:
			raise Exception('in status: unknow type of harm for status')

	def get_harm_after_move(self, hp_max):
		if self.harm_type == const.status_harm_type_const:
			return self.harm_after_move
		elif self.harm_type == const.status_harm_type_ratio:
			return self.harm_after_move * hp_max
		else:
			raise Exception('in status: unknow type of harm for status')

	def get_harm_when_attacked(self, harm):
		if self.harm_type == const.status_harm_type_const:
			return self.harm_when_attacked
		elif self.harm_type == const.status_harm_type_ratio:
			return harm * self.harm_when_attacked
		else:
			raise Exception('in status: unknow type of harm for status')

