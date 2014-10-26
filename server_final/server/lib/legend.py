# -*- coding: utf-8 -*-

import const
from baseCard import base_card

class legend(base_card):
	"""
	传奇对象
	"""
	def __init__(self, name, level, hp, speed):
		# 传奇的攻击力为0，且不同的传奇速度不同
		super(legend, self).__init__(name, const.legend_race, level, 0, hp)
		self.speed = speed
		self.block_hero = []
		# block_hero 存储了所有可以为传奇抵挡伤害的英雄，当英雄技能触发时被添加到列表中

	def add_block_hero(self, hero, harm_percentage):
		self.block_hero.append((hero, harm_percentage))
	
	def damage(self, _from, harm):
		"""
		英雄受到绝对伤害
		"""
		#print str(_from.get_id()) + ' harm ' + str(self.get_id()) + ':' + str(harm)
		#print _from.name + '\t' + self.name
		while self.block_hero.__len__() > 0:
			if self.block_hero[0][0].alive():
				break
			else:
				self.block_hero.pop(0)
		if self.block_hero.__len__() > 0:
			ret = [{'type': 'skill', 'from': self.block_hero[0][0].get_id(), 'to':[], 'name': 'block for legend'}]
			harm, process = self.block_hero[0][0].damage(None, harm * self.block_hero[0][1])
			ret.extend(process)
			return harm, ret
		else:
			return super(legend, self).damage(harm)

	def damage_phy(self, _from, harm):
		"""
		物理伤害
		"""
		return self.damage(_from, harm)

	def damage_magic(self, _from, harm):
		"""
		魔法伤害
		"""
		return self.damage(_from, harm)

	def damage_element(self, _from, harm):
		"""
		元素法术伤害
		"""
		return self.damage(_from, harm)

	def set_speed(self, speed):
		"""
		设置速度
		"""
		self.speed = speed

	def get_speed(self):
		"""
		速度
		"""
		return self.speed

	def die(self):
		"""
		死亡处理
		"""
		#print 'legend ' + str(self.get_id()) + ' died'
		pass

	def get_situation(self):
		"""
		状态信息
		"""
		return {'hp': self.hp, 'speed': self.speed, 'level': self.level, 'name': self.name}

