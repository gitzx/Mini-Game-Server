# -*- coding: utf-8 -*-

"""
所有技能效果类
"""

import random
import const

class skill_effect(object):
	def __init__(self):
		pass

	def effect(self, caster, target, harm = 0):
		pass

class add_hp(skill_effect):
	def __init__(self, hp = 0, hp_type = const.add_hp_type_const_hp):
		self.hp = hp
		self.hp_type = hp_type

	def effect(self, caster, target, harm = 0):
		if self.hp_type == const.add_hp_type_const_hp:
			return target.add_hp(self.hp)
		elif self.hp_type == const.add_hp_type_percentage_hp:
			return target.add_hp(self.hp * target.hp_max)
		elif self.hp_type == const.add_hp_type_harm_percentage_hp:
			return target.add_hp(harm * self.hp)
		elif self.hp_type == const.add_hp_type_add_hp_and_harm_const:
			hp, ret = target.damage(caster, self.hp)
			hp, ret1 = caster.add_hp(hp)
			ret.extend(ret1)
			return hp, ret
		else:
			raise Exception('in skill_effect: unknow type in add_hp')

class add_atk(skill_effect):
	def __init__(self, atk = 0, atk_type = const.add_atk_type_const_atk):
		self.atk = atk
		self.atk_type = atk_type

	def effect(self, caster, target, harm = 0):
		if self.atk_type == const.add_atk_type_const_atk:
			#return harm + self.atk, [{'to':target.get_id(), 'type': 'atk', 'atk':int(self.atk)}]
			return harm + self.atk, []
		elif self.atk_type == const.add_atk_type_percentage_atk:
			#return harm * (1 + self.atk), [{'to':target.get_id(), 'type':'atk', 'atk':int(harm * self.atk)}]
			return harm * (1 + self.atk), []
		elif self.atk_type == const.add_atk_type_const_atk_forever:
			return target.add_atk(self.atk)
		elif self.atk_type == const.add_atk_type_percentage_atk_forever:
			return target.add_atk(self.atk * target.get_atk())
		else:
			raise Exception('in skill_effect: unknow type in add_atk')

class add_attack_num(skill_effect):
	def __init__(self):
		pass

	def effect(self, caster, target, harm = 0):
		target.add_attack_num()
		return harm, [{'to': target.get_id(), 'type': 'addattacknum'}]

# TODO 以下三个类实现的目的不同，只是伤害值传递的通道不同，如何复用呢？

class damage(skill_effect):
	def __init__(self, harm = 0, harm_type = const.damage_type_const):
		self.harm = harm
		self.harm_type = harm_type

	def effect(self, caster, target, harm = 0):
		if self.harm_type == const.damage_type_const:
			return target.damage(caster, self.harm)
		elif self.harm_type == const.damage_type_random:
			l = int(self.harm[0])
			r = int(self.harm[1])
			harm = random.randint(l, r)
			return target.damage(caster, harm)
		elif self.harm_type == const.damage_type_percentage_hp_max:
			harm = self.harm * target.hp_max
			return target.damage(caster, harm)
		elif self.harm_type == const.damage_type_percentage_harm:
			harm1 = self.harm * harm
			harm1, process = target.damage(caster, harm1)
			return harm, process
		else:
			raise Exception('in skill_effect: unknow type in damage')

class damage_magic(skill_effect):
	def __init__(self, harm = 0, harm_type = const.damage_type_const):
		self.harm = harm
		self.harm_type = harm_type

	def effect(self, caster, target, harm = 0):
		if self.harm_type == const.damage_type_const:
			return target.damage_magic(caster, self.harm)
		elif self.harm_type == const.damage_type_random:
			l = int(self.harm[0])
			r = int(self.harm[1])
			harm = random.randint(l, r)
			return target.damage_magic(caster, harm)
		elif self.harm_type == const.damage_type_percentage_hp_max:
			harm = self.harm * target.hp_max
			return target.damage_magic(caster, harm)
		elif self.harm_type == const.damage_type_percentage_harm:
			harm = self.harm * harm
			return target.damage_magic(caster, harm)
		else:
			raise Exception('in skill_effect: unknow type in damage_magic')

class damage_element(skill_effect):
	def __init__(self, harm = 0, harm_type = const.damage_type_const):
		self.harm = harm
		self.harm_type = harm_type

	def effect(self, caster, target, harm = 0):
		if self.harm_type == const.damage_type_const:
			return target.damage_element(caster, self.harm)
		elif self.harm_type == const.damage_type_random:
			l = int(self.harm[0])
			r = int(self.harm[1])
			harm = random.randint(l, r)
			return target.damage_element(caster, harm)
		elif self.harm_type == const.damage_type_percentage_hp_max:
			harm = self.harm * target.hp_max
			return target.damage_element(caster, harm)
		elif self.harm_type == const.damage_type_percentage_harm:
			harm = self.harm * harm
			return target.damage_element(caster, harm)
		else:
			raise Exception('in skill_effect: unknow type in damage_element')

class add_status(skill_effect):
	def __init__(self, status, percentage = 1):
		self.status = status
		self.percentage = percentage

	def effect(self, caster, target, harm = 0):
		ret = []
		if random.random() < self.percentage:
			process = target.add_status(caster, self.status)
			ret.extend(process)
		return harm, ret

class set_death(skill_effect):
	def __init__(self, parameter = 0, set_death_type = const.set_death_type_add_atk_forever):
		self.parameter = parameter
		self.set_death_type = set_death_type

	def effect(self, caster, target, harm = 0):
		if self.set_death_type == const.set_death_type_only:
			harm, process = target.damage(caster, target.hp_max)
		elif self.set_death_type == const.set_death_type_add_atk_forever:
			harm, process = target.damage(caster.get_id(), target.hp_max)
			atk, process1 = caster.add_atk(self.parameter)
			process.extend(process1)
		else:
			raise Exception('in skill_effect: unknow type in set_death')
		return harm, process	

class block(skill_effect):
	def __init__(self, block_harm = 0, block_type = const.block_type_block_const):
		self.block_type = block_type
		self.block_harm = block_harm

	def effect(self, caster, target, harm = 0):
		if self.block_type == const.block_type_block_const:
			harm = harm - self.block_harm
			if harm < 0:
				harm = 0
			return harm, []
		elif self.block_type == const.block_type_block_all:
			return 0, []
		elif self.block_type == const.block_type_block_most_harm:
			if harm > self.block_harm:
				harm = self.block_harm
			return harm, []
		else:
			raise Exception('in skill_effect, block')

class block_legend(skill_effect):
	def __init__(self, percentage):
		self.percentage = percentage

	def effect(self, caster, target, harm = 0):
		target.add_block_hero(caster, self.percentage)
		return 0, []

class reflect(skill_effect):
	def __init__(self, reflect_harm):
		self.reflect_harm = reflect_harm

	def effect(self, caster, target, harm = 0):
		harm1, process = target.damage(caster, self.reflect_harm)
		return harm, process

class reborn(skill_effect):
	def __init__(self):
		pass

	def effect(self, caster, target, harm = 0):
		caster.reborn()

