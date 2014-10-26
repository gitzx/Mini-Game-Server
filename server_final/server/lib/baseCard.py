# -*- coding: utf-8 -*-

class base_card(object):
	"""
	���п��ƵĻ�����
	���ڼ�¼���ƵĻ�����Ϣ
	"""
	def __init__(self, name, race, level, atk, hp):
		self.name = name
		self.race = race # ������Ϣ��Ϊ���㴦�����д������������Ϊlegend
		self.level = level
		self.atk = atk
		self.hp_max = hp
		self.hp = hp

	def set_id(self, _id):
		"""
		���ÿ�����ս���е�λ��
		λ��˵�����������棺0 �Է�����4 �������зֱ�Ϊ1 2 3 ��֮��Եĵط����зֱ�Ϊ 5 6 7
		"""
		self._id = _id

	def get_id(self):
		"""
		��ȡλ��
		"""
		return self._id

	def get_race(self):
		"""
		��ȡ����
		"""
		return self.race

	def get_name(self):
		"""
		��ȡ���֣���������ʹ�õ��ǿ��Ʊ��
		"""
		return self.name

	def get_level(self):
		"""
		����
		"""
		return self.level

	def get_atk(self):
		return self.atk

	def damage(self, harm):
		"""
		�����ܵ�ֵΪharm���˺�
		�˺�ֵΪ����ʱ�׳��쳣
		"""
		if harm < 0:
			raise Exception('in base_card: damage velue cannot be negative')
		if self.hp < 1:
			# Ŀ���������������˺�
			return 0, []
		hpb = self.hp
		self.hp = self.hp - int(harm)
		if self.hp < 0:
			self.hp = 0
		if self.hp < 1:
			self.die() # card killed
		if hpb != self.hp:
			return hpb - self.hp, [{'to': self.get_id(), 'type': 'harm', 'harm':hpb - self.hp}]
		else:
			# ֻ���ܵ��˺�ʱ�Ż������˶���
			return 0, []

	def add_hp(self, hp):
		"""
		��Ѫ
		"""
		if hp < 0:
			raise Exception('in base_card: cure velue cannot be negative, please call damage instead')
		if not self.alive():
			return 0, []
		hpb = self.hp
		self.hp = self.hp + int(hp)
		if self.hp > self.hp_max:
			self.hp = self.hp_max
		if self.hp != hpb:
			ret = [{'to': self.get_id(), 'type': 'cure', 'cure':self.hp - hpb}]
		else:
			ret = []
		return self.hp - hpb, ret

	def alive(self):
		"""
		�жϿ����Ƿ񻹴��
		"""
		return self.hp > 0

	def get_hp_max(self):
		return self.hp_max

	def get_hp(self):
		return self.hp

	def get_lose_hp(self):
		"""
		ʧѪ��
		"""
		return self.hp_max - self.hp

