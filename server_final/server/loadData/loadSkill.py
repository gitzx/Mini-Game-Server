# -*- coding:utf-8 -*-

import xlrd
import const
from skill import skill
from skill import blockSkill

from skill import getTarget
from skill import skillEffect
from skill import skillCondition

targets = { # 目标编号与目标函数的对应关系
		1: getTarget.target_self,
		2: getTarget.target_target,
		3: getTarget.target_self_legend,
		4: getTarget.target_target_legend,
		5: getTarget.target_self_all,
		6: getTarget.target_target_random1,
		7: getTarget.target_target_random2,
		8: getTarget.target_target_all,
		9: getTarget.target_self_max_lose_hp,
		10: getTarget.target_target_min_hp,
		11: getTarget.target_target_neighbour
		}

conditions = { # 条件编号与条件对象的对应关系
		1: skillCondition.probability,
		2: skillCondition.check_target_race,
		3: skillCondition.check_target_not_race,
		4: skillCondition.check_target_hp_less_then_x,
		5: skillCondition.check_death,
		6: skillCondition.check_hp_self_comp_target
		}

effects = { # 效果
		1: skillEffect.add_hp,
		2: skillEffect.add_atk,
		3: skillEffect.add_attack_num,
		4: skillEffect.block_legend,
		5: skillEffect.damage_magic,
		6: skillEffect.damage_element,
		7: skillEffect.damage,
		8: skillEffect.add_status,
		9: skillEffect.set_death,
		10:skillEffect.block,
		11:skillEffect.reflect,
		12:skillEffect.reborn
		}

class raw_skill(object):
	def __init__(self):
		self.skills = {}
		self.skill_pool = {}

	def get_name(self, table, row):
		name = table.cell(row, 1).value
		return name

	def get_type(self, table, row):
		ret = table.cell(row, 2).value
		return ret

	def get_effect(self, table, row):
		effect_id = table.cell(row, 9).value
		parameter1 = table.cell(row, 10).value
		parameter2 = table.cell(row, 11).value
		if effect_id == "":
			return None
		if parameter1 == "":
			return (int(effect_id), )
		else:
			if parameter2 == "":
				return  (int(effect_id), parameter1)
			else:
				if effect_id == 6 and parameter2 == 2:
					t = parameter1.split(' ')
					parameter1 = (int(t[0]), int(t[1]))
				return (int(effect_id), parameter1, parameter2)

	def get_target(self, table, row):
		ret = table.cell(row, 4).value
		if ret:
			return int(ret)
		else:
			return None

	def get_trigger_time(self, table, row):
		ret = int(table.cell(row, 3).value)
		return ret

	def get_condition(self, table, row):
		condition_id = table.cell(row, 7).value
		parameter = table.cell(row, 8).value
		if not condition_id:
			return None
		if parameter:
			return (condition_id, parameter)
		else:
			return (condition_id, )

	def get_only_once(self, table, row):
		"""
		获取是否只允许触发一次
		"""
		ret = table.cell(row, 5).value
		if ret:
			return True
		else:
			return False

	def get_grow(self, table, row):
		"""
		成长类型
		"""
		grow_type = table.cell(row, 12).value
		return grow_type

	def append_skill(self, skill_name, skill_type, trigger_time, skill_target, condition, only_once, effect, grow_type):
		if skill_name in self.skills:
			raise Exception('skill with name ' + skill_name + ' have inserted befor')
		self.skills[skill_name] = [skill_type, trigger_time, skill_target, condition, only_once, effect, grow_type]

	def load(self, filename, sheet_id):
		"""
		从文件filename的第sheet_id个表格中导出数据
		"""
		data = xlrd.open_workbook(filename)
		table = data.sheets()[sheet_id]

		skill_name = None
		effect = []
		condition = []
		for i in xrange(1, table.nrows):
			name_t = self.get_name(table, i)
			if name_t:
				if skill_name != None:
					self.append_skill(skill_name, skill_type, trigger_time, target, condition, only_once, effect, grow_type)
				skill_name = name_t
				effect = []
				condition = []
				skill_type = self.get_type(table, i)
				trigger_time = self.get_trigger_time(table, i)
				target = self.get_target(table, i)
				con = self.get_condition(table, i)
				if con:
					condition.append(con)
				only_once = self.get_only_once(table, i)
				eff = self.get_effect(table, i)
				if eff:
					effect.append(eff)
				grow_type = self.get_grow(table, i)
			else:
				con = self.get_condition(table, i)
				eff = self.get_effect(table, i)
				if con:
					condition.append(con)
				if eff:
					effect.append(eff)
		self.append_skill(skill_name, skill_type, trigger_time, target, condition, only_once, effect, grow_type)

	def get_skill(self, skill_name, level = 1):
		"""
		由技能名字和技能级别获取技能
		"""
		#print 'skill name is: ' + skill_name
		if (skill_name, level) in self.skill_pool:
			return self.skill_pool[(skill_name, level)]
		if skill_name in self.skills:
			skill_data = self.skills[skill_name]
			skill_type = skill_data[0]
			trigger_time = skill_data[1]
			skill_target = skill_data[2]
			skill_condition = skill_data[3]
			only_once = skill_data[4]
			skill_effect = skill_data[5]
			grow_type = skill_data[6]

			if trigger_time in [5, 6, 7, 9]:
				ret = blockSkill.block_skill(skill_name, level, skill_type, trigger_time)
			else:
				ret = skill.skill(skill_name, level, skill_type, trigger_time)
			if only_once:
				ret.set_only_once()
			if skill_target:
				ret.set_target(targets[skill_target])
			for condition in skill_condition:
				if condition.__len__() == 2:
					if grow_type == 1:
						condition_level = level
						ret.add_condition(conditions[condition[0]](condition_level * condition[1]))
						grow_type = None
					else:
						#print eval('u"' + skill_name + '"')
						ret.add_condition(conditions[condition[0]](condition[1]))
				elif condition.__len__() == 1:
					ret.add_condition(conditions[condition[0]]())
				else:
					raise Exception('unknow condition')
			for effect in skill_effect:
				if effect.__len__() == 3:
					if grow_type == 2:
						if type(effect[1]) == type((1, 2)):
							tmp_effect1 = (effect[1][0] * level, effect[1][1] * level)
							ret.add_effect(effects[effect[0]](tmp_effect1, effect[2]))
							# TODO not good
						else:
							ret.add_effect(effects[effect[0]](effect[1] * level, effect[2]))
						grow_type = None
					elif grow_type == 3:
						ret.add_effect(effects[effect[0]](effect[1] - 3 * (level - 1), effect[2]))
						grow_type = None
					else:
						ret.add_effect(effects[effect[0]](effect[1], effect[2]))
				elif effect.__len__() == 2:
					if grow_type == 2:
						ret.add_effect(effects[effect[0]](effect[1] * level))
						grow_type = None
					elif grow_type == 3:
						ret.add_effect(effects[effect[0]](effect[1] - 3 * (level-1)))
						grow_type = None
					else:
						ret.add_effect(effects[effect[0]](effect[1]))
				elif effect.__len__() == 1:
					ret.add_effect(effects[effect[0]]())
				else:
					raise Exception('unknow effect')
			self.skill_pool[(skill_name, level)] = ret
			return ret
		else:
			print 'skill name:',
			print eval('u"' + skill_name + '"')
			raise Exception('skill with name ' + skill_name + ' not defined yet')

