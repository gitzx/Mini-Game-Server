# -*- coding: utf-8 -*-
from lib.heroStatus import hero_status
from lib.baseCard import base_card
from skill import getTarget
import world
import const

class hero(base_card):
	"""
	战斗中的英雄卡牌
	"""
	def __init__(self, name, race, stars, level, atk, hp):
		super(hero, self).__init__(name, race, level, atk, hp)
		self.stars = stars
		self.attack_num = 1
		self.status = hero_status()

		#技能列表，按触发时间不同定义了几个数组
		self.skill_enter = []
		self.skill_magic = []
		self.skill_befor_atk = []
		self.skill_after_atk = []
		self.skill_block_phy = [] 
		self.skill_block_magic = []
		self.skill_block_element = [] 
		self.skill_die = []
		self.skill_block_status = []

		self.hero_id = 0

	def reborn(self):
		# TODO write the reborn
		pass

	def get_stars(self):
		return self.stars

	def add_atk(self, atk):
		atk = int(atk)
		if atk + self.atk < 0:
			atk = -1 * self.atk
		ret = [{'to':self.get_id(), 'type': 'atk', 'atk':int(atk)}]
		self.atk = self.atk + atk
		return self.atk, ret

	def add_attack_num(self, num = 1):
		self.attack_num = self.attack_num + num

	def damage(self, _from, harm):
		"""
		绝对伤害
		"""
		#print str(_from.get_id()) + ' harm ' + str(self.get_id()) + ':' + str(harm)
		#print _from.name + '\t' + self.name
		harm = super(hero, self).damage(harm)
		return harm

	def damage_phy(self, _from, harm):
		"""
		物理伤害
		"""
		ret = []
		for skill in self.skill_block_phy:
			harm, process = skill.effect(self, _from, harm)
			ret.extend(process)
		harm, process = self.damage(_from, harm)
		ret.extend(process)
		
		harm1, process = self.status.get_harm_when_attacked(self.get_id(), harm)
		ret.extend(process)
		harm = harm + harm1

		return harm, ret

	def damage_magic(self, _from, harm):
		"""
		法术伤害
		"""
		ret = []
		for skill in self.skill_block_magic:
			harm, process = skill.effect(self, _from, harm)
			ret.extend(process)
		harm, process = self.damage(_from, harm)
		ret.extend(process)
		return harm, ret

	def damage_element(self, _from, harm):
		"""
		元素法术伤害
		"""
		ret = []
		for skill in self.skill_block_element:
			harm, process = skill.effect(self, _from, harm)
			ret.extend(process)
		harm, process = self.damage(_from, harm)
		ret.extend(process)
		return harm, ret

	def add_status(self, _from, status_name):
		"""
		添加状态，如中毒等
		"""
		if self.skill_block_status.__len__() > 0:
			return []
		return self.status.add_status(status_name, self.get_id())

	def add_hp(self, hp):
		if not self.status.can_add_hp():
			hp = 0
		return super(hero, self).add_hp(hp)

	def add_skill(self, skill_name, skill_level = 1):
		"""
		初始化用户时，添加技能
		"""
		skill = world.skills.get_skill(skill_name, skill_level)
		if skill.trigger_time == 1:
			self.skill_enter.append(skill)
		elif skill.trigger_time == 2:
			self.skill_magic.append(skill)
		elif skill.trigger_time == 3:
			self.skill_befor_atk.append(skill)
		elif skill.trigger_time == 4:
			self.skill_after_atk.append(skill)
		elif skill.trigger_time == 5:
			self.skill_block_phy.append(skill)
		elif skill.trigger_time == 6:
			self.skill_block_magic.append(skill)
			self.skill_block_element.append(skill)
		elif skill.trigger_time == 7:
			self.skill_block_element.append(skill)
		elif skill.trigger_time == 8:
			self.skill_die.append(skill)
		elif skill.trigger_time == 9:
			self.skill_block_status.append(skill)
			self.skill_block_magic.append(skill)
			self.skill_block_element.append(skill)
		else:
			raise Exception('unknow trigger time')

	def set_heap(self, heap):
		"""
		设置在队列中的位置
		"""
		self.heap = heap

	def get_heap(self):
		return self.heap

	def enter(self, team_self, team_target):
		"""
		入场时
		"""
		ret = []
		for skill in self.skill_enter:
			if not self.alive():
				return ret
			harm, process = skill.effect(team_self, self.get_heap(), team_target)
			ret.extend(process)
		return ret

	def magic(self, team_self, team_target):
		"""
		法术阶段
		"""
		ret = []
		skill_to_remove = None
		for i, skill in enumerate(self.skill_magic):
			if not self.alive():
				return ret
			harm, process = skill.effect(team_self, self.get_heap(), team_target)
			if skill.only_once:
				skill_to_remove = i
			ret.extend(process)
		if skill_to_remove:
			self.skill_magic.pop(skill_to_remove)
		return ret

	def die(self):
		"""
		死亡
		"""
		# TODO 重生和自爆自己没有实现
		ret = []
		#for skill in self.skill_die:
		#	harm, process = skill.effect(team_self, self.get_heap(), team_target)
		#	ret.extend(process)
		#print eval('u"' + self.get_name() + str(self.get_id()) + '"'),
		#print str(self.get_name()) + str(self.get_id())
		#print ' died'
		return ret

	def attack(self, team_self, team_target, target = None):
		"""
		物理攻击过程
		"""
		if target == None:
			target = getTarget.target_target(team_self, self.get_heap(), team_target)[0]
		ret = []
		if not self.alive():
			return  ret
		harm = self.get_atk()
		skillToRemove = None
		for i, skill in enumerate(self.skill_befor_atk):
			harm, process = skill.effect(team_self, target.get_heap(), team_target, harm)
			ret.extend(process)
			if skill.only_once:
				skillToRemove = i
		if skillToRemove != None:
			self.skill_befor_atk.pop(skillToRemove)
		if not self.alive():
			return ret
		ret.append({'from': self.get_id(), 'to': target.get_id(), 'type': 'attack'})
		harm, process = target.damage_phy(self, harm)
		ret.extend(process)
		if not self.alive():
			return ret
		death = not target.alive()
		for skill in self.skill_after_atk:
			#print skill.name
			harm, process = skill.effect(team_self, self.get_heap(), team_target, harm, death)
			ret.extend(process)
		return ret

	def step(self, team_self, team_target):
		"""
		行动阶段
		"""
		ret = []
		if not self.alive():
			return ret
		harm, process = self.status.get_harm_before_move(self.get_id(), self.hp_max)
		harm, process = super(hero, self).damage(harm)
		ret.extend(process)
		harm, process = super(hero, self).damage(harm)
		ret.extend(process)
		if not self.alive():
			return ret
		if self.status.can_move():
			if self.status.can_magic():
				process = self.magic(team_self, team_target)
				ret.extend(process)
			if self.status.can_attack():
				tar = getTarget.target_target(team_self, self.get_heap(), team_target)[0]
				if tar.race == const.legend_race:
					ret.append({'type': 'attack', 'from': self.get_id(), 'to': tar.get_id()})
					harm, process = tar.damage_phy(self, self.get_atk())
					ret.extend(process)
				else:
					if self.attack_num == 1:
						self.attack_num = 0
						process = self.attack(team_self, team_target)
						ret.extend(process)
					elif self.attack_num == 2:
						self.attack_num = 0
						process = self.attack(team_self, team_target)
						ret.extend(process)
						target = team_target.get_hero(self.get_heap())
						if self.alive() and target and target.alive():
							process = self.attack(team_self, team_target)
							ret.extend(process)
					else:
						raise Exception('number of attacks is ' + str(self.attack_num))
					if self.alive() and self.attack_num > 0:
						ta = getTarget.target_target_random1(team_self, self.get_heap(), team_target)
						if ta.__len__() > 0:
							process = self.attack(team_self, team_target, ta[0])
							ret.extend(process)
			self.attack_num = 1
		if not self.alive():
			return ret
		harm, process = self.status.get_harm_after_move(self.get_id(), self.hp_max)
		harm, process = super(hero, self).damage(harm)
		ret.extend(process)
		process = self.status.step(self.get_id())
		ret.extend(process)
		return ret

	def get_situation(self):
		"""
		获取状态
		"""
		#ret = {'name': self.name, 'level': self.level, 'hp': self.hp, 'atk': self.atk, 'id': self.hero_id}
		ret = {'id': int(float(self.name)), 'level': self.level, 'hp': self.hp, 'atk': self.atk}
		return ret

	def set_hero_id(self, hero_id):
		"""
		设置卡牌在数据库中的ID
		"""
		self.hero_id = hero_id

