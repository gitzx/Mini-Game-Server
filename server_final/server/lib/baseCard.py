# -*- coding: utf-8 -*-

class base_card(object):
	"""
	所有卡牌的基础类
	用于记录卡牌的基本信息
	"""
	def __init__(self, name, race, level, atk, hp):
		self.name = name
		self.race = race # 种族信息，为方便处理，所有传奇的种族设置为legend
		self.level = level
		self.atk = atk
		self.hp_max = hp
		self.hp = hp

	def set_id(self, _id):
		"""
		设置卡牌在战斗中的位置
		位置说明：己方传奇：0 对方传奇4 己方三列分别为1 2 3 与之相对的地方三列分别为 5 6 7
		"""
		self._id = _id

	def get_id(self):
		"""
		获取位置
		"""
		return self._id

	def get_race(self):
		"""
		获取种族
		"""
		return self.race

	def get_name(self):
		"""
		获取名字，现在名字使用的是卡牌编号
		"""
		return self.name

	def get_level(self):
		"""
		级别
		"""
		return self.level

	def get_atk(self):
		return self.atk

	def damage(self, harm):
		"""
		卡牌受到值为harm的伤害
		伤害值为负数时抛出异常
		"""
		if harm < 0:
			raise Exception('in base_card: damage velue cannot be negative')
		if self.hp < 1:
			# 目标已阵亡，不受伤害
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
			# 只有受到伤害时才会有受伤动作
			return 0, []

	def add_hp(self, hp):
		"""
		回血
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
		判断卡牌是否还存活
		"""
		return self.hp > 0

	def get_hp_max(self):
		return self.hp_max

	def get_hp(self):
		return self.hp

	def get_lose_hp(self):
		"""
		失血量
		"""
		return self.hp_max - self.hp

