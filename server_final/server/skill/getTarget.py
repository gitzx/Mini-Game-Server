# -*- coding: utf-8 -*-

"""
��ȡĿ��ĺ�������
"""

import random

def get_position(team, position):
	return [team.get_hero(position)]

def get_legend(team):
	return [team.get_legend()]

def get_random(team, num):
	tar = random.randint(0, 2)
	ret = []
	for hero_id in xrange(3):
		hero = team.get_hero((hero_id+tar) % 3)
		if hero and hero.alive():
			ret.append(hero)
			if ret.__len__() > num-1:
				break
	return ret

def target_self(attacker_team, attacker_id, injured_team): 
	# �Լ�
	return get_position(attacker_team, attacker_id)

def target_target(attacker_team, attacker_id, injured_team):
	#�������Ŀ�꣬�����򷵻ضԷ�����
	ret = get_position(injured_team, attacker_id)
	if not ret[0] or not ret[0].alive():
		ret = get_legend(injured_team)
	return ret

def target_self_legend(attacker_team, attacker_id, injured_team):
	# ��������
	return get_legend(attacker_team)

def target_target_legend(attacker_team, attacker_id, injured_team):
	# �Է�����
	return get_legend(injured_team)

def target_self_all(attacker_team, attacker_id, injured_team):
	# ����ȫ��
	return get_random(attacker_team, 3)

def target_target_random1(attacker_team, attacker_id, injured_team):
	# �Է����һ��
	return get_random(injured_team, 1)

def target_target_random2(attacker_team, attacker_id, injured_team):
	# �Է��������
	return get_random(injured_team, 2)

def target_target_all(attacker_team, attacker_id, injured_team):
	# �Է�ȫ��
	return get_random(injured_team, 3)

def get_max_lose_hp(team):
	ret = None
	for i in xrange(3):
		hero = team.get_hero(i)
		if hero == None:
			continue
		if ret == None:
			ret = hero
		elif hero.get_lose_hp() > ret.get_lose_hp():
			ret = hero
	if ret:
		return [ret]
	else:
		return []

def target_self_max_lose_hp(attacker_team, attacker_id, injured_team):
	# ����ʧѪ����Ӣ��
	return get_max_lose_hp(attacker_team)

def target_target_max_lose_hp(attacker_team, attacker_id, injured_team):
	# �Է�ʧѪ����Ӣ��
	return get_max_lose_hp(injured_team)

def get_min_hp(team):
	ret = None
	for i in xrange(3):
		hero = team.get_hero(i)
		if hero == None:
			continue
		if ret == None:
			ret = hero
		elif hero.get_hp() < ret.get_hp():
			ret = hero
	if ret:
		return [ret]
	else:
		return []

def target_self_min_hp(attacker_team, attacker_id, injured_team):
	# ����Ѫ������
	return get_min_hp(attacker_team)

def target_target_min_hp(attacker_team, attacker_id, injured_team):
	# �Է�Ѫ������
	return get_min_hp(injured_team)

def target_target_neighbour(attacker_team, attacker_id, injured_team):
	# �Է���ֱ�ӹ���Ŀ�������Ӣ�ۣ����ں�ɨ����
	ret = []
	hero = injured_team.get_hero((attacker_id + 2) % 3)
	if hero != None:
		ret.append(hero)
	hero = injured_team.get_hero((attacker_id + 1) % 3)
	if hero != None:
		ret.append(hero)
	return ret


