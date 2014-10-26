# -*- coding: utf-8 -*-

import const
import world

class hero_status(object):
	"""
	一个卡牌所包含状态的管理器
	"""
	def __init__(self):
		self.status_one = []
		self.status_all = []

	def add_status(self, status_name, target_id = 0):
		"""
		添加状态
		"""
		ret = []
		status = world.all_status.get_status(status_name)
		if status.last_time == const.status_last_time_one_step:
			insert_array = self.status_one
		elif status.last_time == const.status_last_time_always:
			insert_array = self.status_all
		else:
			raise Exception('in hero_status: unknow status')
		
		exist = False
		for st in insert_array:
			if st.name == status_name:
				exist = True
				break
		if not exist:
			insert_array.append(status)
			ret.append({'type': 'addStatus', 'name': status.name, 'to': target_id})
		return ret

	def step(self, hero_id):
		"""
		去除一次性状态
		"""
		ret = []
		for st in self.status_one:
			ret.append({'type': 'removeStatus', 'name': st.name, 'to': hero_id})
		self.status_one = []
		return ret

	def can_move(self):
		"""
		判断在当前状态下是否可以移动
		"""
		for status in self.status_one:
			if not status.can_move:
				return False
		for status in self.status_all:
			if not status.can_move:
				return False
		return True

	def can_magic(self):
		"""
		判断在当前状态下是否可以施法
		"""
		for status in self.status_one:
			if not status.can_magic:
				return False
		for status in self.status_all:
			if not status.can_magic:
				return False
		return True

	def can_attack(self):
		"""
		判断在当前状态下是否可以攻击
		"""
		for status in self.status_one:
			if not status.can_attack:
				return False
		for status in self.status_all:
			if not status.can_attack:
				return False
		return True

	def can_add_hp(self):
		"""
		判断在当前状态下是否可以加血
		"""
		for status in self.status_one:
			if not status.can_add_hp:
				return False
		for status in self.status_all:
			if not status.can_add_hp:
				return False
		return True

	def get_harm_before_move(self, hero_id, hp):
		"""
		攻击前状态伤害计算
		"""
		process = []
		ret = 0
		for status in self.status_one:
			harm = int(status.get_harm_before_move(hp))
			ret = ret + harm
			#if harm > 0:
			#	process.append({'type': 'status', 'harm': harm, 'to': hero_id, 'statusName': status.name})
		for status in self.status_all:
			harm = int(status.get_harm_before_move(hp))
			ret = ret + harm
			#if harm > 0:
			#	process.append({'type': 'status', 'harm': harm, 'to': hero_id, 'name': status.name})
		return ret, process

	def get_harm_after_move(self, hero_id, hp):
		"""
		攻击后状态伤害计算
		"""
		process = []
		ret = 0
		for status in self.status_one:
			harm = int(status.get_harm_after_move(hp))
			ret = ret + harm
			#if harm > 0:
			#	process.append({'type': 'status', 'harm': harm, 'to': hero_id, 'name': status.name})
		for status in self.status_all:
			harm = int(status.get_harm_after_move(hp))
			ret = ret + harm
			#if harm > 0:
			#	process.append({'type': 'status', 'harm': harm, 'to': hero_id, 'name': status.name})
		return ret, process

	def get_harm_when_attacked(self, hero_id, harm):
		"""
		攻击时状态伤害计算
		"""
		process = []
		ret = 0
		for status in self.status_one:
			harm = int(status.get_harm_when_attacked(harm))
			ret = ret + harm
			#if harm > 0:
			#	process.append({'type': 'status', 'harm': harm, 'to': hero_id, 'name': status.name})
		for status in self.status_all:
			harm = int(status.get_harm_when_attacked(harm))
			ret = ret + harm
			#if harm > 0:
			#	process.append({'type': 'status', 'harm': harm, 'to': hero_id, 'name': status.name})
		return ret, process

