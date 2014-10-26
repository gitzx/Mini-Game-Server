# -*- coding: utf-8 -*-

class skill(object):
	"""
	�����ࣺͨ����Ӳ�ͬ��Ŀ���ͬ�������Լ���ͬ��Ч������ʵ�ֶ���(����)����
	"""
	def __init__(self, name, level, skill_type, trigger_time):
		self.name = name
		self.level = level
		self.skill_type = skill_type
		self.trigger_time = trigger_time

		self.target = None
		self.conditions = []
		self.effects = []
		self.only_once = False

	def set_only_once(self):
		"""
		���ü���ֻ�ܴ���һ��
		"""
		self.only_once = True

	def set_target(self, func):
		"""
		���ü���Ŀ��
		"""
		self.target = func

	def add_condition(self, condition):
		"""
		���Ӽ��ܴ�������
		"""
		self.conditions.append(condition)

	def add_effect(self, effect):
		"""
		���Ӽ���Ч��
		"""
		self.effects.append(effect)

	def effect(self, caster_team, caster_id, target_team, harm = 0, death = 0):
		"""
		�жϼ����Ƿ񴥷������ǣ������Ч��
		"""
		ret = []
		targets = self.target(caster_team, caster_id, target_team)
		caster = caster_team.get_hero(caster_id)
		#if caster == None or not caster.alive():
		#	return 0, ret
		skill_t = []
		for target in targets:
			can_effect = True
			for condition in self.conditions:
				if not condition.test(caster, target, harm, death):
					can_effect = False
					break
			if can_effect:
				#skill_t.append(target.get_id())
				#print str(caster.get_id()) + 'skill:' + self.name + str(target.get_id())
				#ret.append({'from': caster.get_id(), 'to': target.get_id(), 'type': 'skill', 'name': self.name})
				effected = False
				for effect in self.effects:
					try:
						harm, process = effect.effect(caster, target, harm)
					except:
						print 'Error in skill: ',
						print eval('u"' + self.name + '"')
					if process.__len__() > 0:
						effected = True
					ret.extend(process)
					if not target.alive():
						break
				if effected:
					skill_t.append(target.get_id())
		if skill_t.__len__() > 0:
			ret1 = [{'from': caster.get_id(), 'to': skill_t, 'type': 'skill', 'name': self.name}]
			ret1.extend(ret)
			ret = ret1
		else:
			ret = []
		return harm, ret

