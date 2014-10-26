# -*- coding: utf-8 -*-

import const
import world

class hero_status(object):
	"""
	һ������������״̬�Ĺ�����
	"""
	def __init__(self):
		self.status_one = []
		self.status_all = []

	def add_status(self, status_name, target_id = 0):
		"""
		���״̬
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
		ȥ��һ����״̬
		"""
		ret = []
		for st in self.status_one:
			ret.append({'type': 'removeStatus', 'name': st.name, 'to': hero_id})
		self.status_one = []
		return ret

	def can_move(self):
		"""
		�ж��ڵ�ǰ״̬���Ƿ�����ƶ�
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
		�ж��ڵ�ǰ״̬���Ƿ����ʩ��
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
		�ж��ڵ�ǰ״̬���Ƿ���Թ���
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
		�ж��ڵ�ǰ״̬���Ƿ���Լ�Ѫ
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
		����ǰ״̬�˺�����
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
		������״̬�˺�����
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
		����ʱ״̬�˺�����
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

