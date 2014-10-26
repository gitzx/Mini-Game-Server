# -*- coding: utf-8 -*-

import getTarget
from skill import skill

class block_skill(skill):
	"""
	������������
	"""
	def __init__(self, name, level, skill_type, trigger_time):
		super(block_skill, self).__init__(name, level, skill_type, trigger_time)

	def effect(self, caster, target, harm):
		"""
		�ж��Ƿ�ﵽ���ܴ������������ǣ��������ӦЧ��
		"""
		if target == getTarget.target_self:
			caster, target = target, caster
		ret = []
		can_effect = True
		for condition in self.conditions:
			if not condition.test(caster, target, harm):
				can_effect = False
				break
		if can_effect:
			ret.append({'from':caster.get_id(), 'to':[], 'type': 'skill', 'name': self.name})
			for effect in self.effects:
				harm, process = effect.effect(caster, target, harm)
				ret.extend(process)
		return harm, ret

