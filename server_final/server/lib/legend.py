# -*- coding: utf-8 -*-

import const
from baseCard import base_card

class legend(base_card):
	"""
	�������
	"""
	def __init__(self, name, level, hp, speed):
		# ����Ĺ�����Ϊ0���Ҳ�ͬ�Ĵ����ٶȲ�ͬ
		super(legend, self).__init__(name, const.legend_race, level, 0, hp)
		self.speed = speed
		self.block_hero = []
		# block_hero �洢�����п���Ϊ����ֵ��˺���Ӣ�ۣ���Ӣ�ۼ��ܴ���ʱ����ӵ��б���

	def add_block_hero(self, hero, harm_percentage):
		self.block_hero.append((hero, harm_percentage))
	
	def damage(self, _from, harm):
		"""
		Ӣ���ܵ������˺�
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
		�����˺�
		"""
		return self.damage(_from, harm)

	def damage_magic(self, _from, harm):
		"""
		ħ���˺�
		"""
		return self.damage(_from, harm)

	def damage_element(self, _from, harm):
		"""
		Ԫ�ط����˺�
		"""
		return self.damage(_from, harm)

	def set_speed(self, speed):
		"""
		�����ٶ�
		"""
		self.speed = speed

	def get_speed(self):
		"""
		�ٶ�
		"""
		return self.speed

	def die(self):
		"""
		��������
		"""
		#print 'legend ' + str(self.get_id()) + ' died'
		pass

	def get_situation(self):
		"""
		״̬��Ϣ
		"""
		return {'hp': self.hp, 'speed': self.speed, 'level': self.level, 'name': self.name}

