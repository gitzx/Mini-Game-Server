# -*- coding: utf-8 -*-
"""
���ڼ�¼������ҵ��û����ݣ�
gold��diamondÿ��XXʱ��д�����ݿ�һ��
scene����ʱд�����ݿ�
heros��legendÿ��XXʱ��д�����ݿ�һ��
friend_list�ڸ���ʱд�����ݿ�
powerΪ��ҵ�����ֵ��ÿ��6min����һ�㣬ÿ��ս������5�㣬������const.power_max + ��������
power���¼�ϴμ�����ֵ��ʱ��
"""

import battleUser
import world
import const
import time

import xlrd

class new_user(object):
	"""
	��ʼ��һ�����û����洢�����ݿ���
	"""
	def __init__(self):
		self.legend_table = world.db_legend
		self.hero_table = world.db_hero
		self.user_data = world.db_user_data
		self.pvp_table = world.db_pvp

	def create(self, username):
		"""
		�����û�
		"""
		self.user_data.add_user(username)
		data = xlrd.open_workbook(const.test_war_filename)
		table = data.sheets()[0]

		name = str(int(table.cell(0, 0).value))
		level = int(table.cell(0, 1).value)

		legend = self.legend_table.add_legend(username, name)
		self.legend_table.update_legend(legend.legendId, level, 0, 1)

		hero_datas = []
		for i in range(1, table.nrows):
			name = str(int(table.cell(i, 0).value))
			level = int(table.cell(i, 1).value)
			heap = int(table.cell(i, 2).value)
			hero_datas.append((name, username, level, 0, heap))
		self.hero_table.add_heros(hero_datas)
		self.pvp_table.add_hero(username)

create_new_user = new_user()

class user_data(object):
	"""
	��¼�û����������
	"""
	def __init__(self, data):
		self.username = data[0]
		self.user_data_table = world.db_user_data
		self.heros_table = world.db_hero
		self.legend_table = world.db_legend
		self.friend_table = world.db_friend

		#data = self.user_data_table.get_user_data(username)
		self.gold = data[1]
		self.diamond = data[2]
		self.scene = [int(i) for i in data[3]]
		self.power = data[4]
		self.update_time_power = data[5]

		self.heros = self.heros_table.get_hero_list(self.username)
		self.legends = self.legend_table.get_legend_list(self.username)
		self.friend_list = self.friend_table.get_friend_list(self.username)

	def refresh_power(self):
		"""
		ˢ���û��Ļ���ֵ
		"""
		self.power = const.power_max

	def cost_power(self, power):
		"""
		ս�������Ļ���ֵ
		"""
		if self.power < power:
			return False
		else:
			self.power = self.power - power
			print 'cost power: ' + str(power)
			print 'left power: ' + str(self.power)
			return True

	def store(self):
		"""
		���û����ݴ洢�����ݿ���
		"""
		self.user_data_table.update(self.username, self.gold, self.diamond, "".join([str(i) for i in self.scene]), self.power, self.update_time_power)
		for hero in self.heros:
			hero_data = self.heros[hero]
			self.heros_table.update_hero(hero_data.heroId, hero_data.level, hero_data.exp, hero_data.position)
		for legend in self.legends:
			legend_data = self.legends[legend]
			self.legend_table.update_legend(legend_data.legendId, legend_data.level, legend_data.exp, legend_data.position)

	def add_friend(self, friend_name, store = True):
		"""
		��Ӻ���
		"""
		if store:
			result = self.friend_table.add_friend(self.username, friend_name)
		else:
			result = True
		if result:
			self.friend_list.append(friend_name)
			if store:
				friend = world.onlineUsers.get_user_with_name(friend_name)
				if friend:
					friend.add_friend(self.username, False)
		if result:
			return friend_name
		else:
			return False

	def remove_friend(self, friend_name, store = True):
		"""
		ɾ������
		"""
		if store:
			result = self.friend_table.remove_friend(self.username, friend_name)
		else:
			result = True
		if result:
			for i, friend in enumerate(self.friend_list):
				if friend == friend_name:
					self.friend_list.pop(i)
					break
			if store:
				friend = world.onlineUsers.get_user_with_name(friend_name)
				if friend:
					friend.remove_friend(self.username, False)
		if result:
			return friend_name
		else:
			return False

	def get_friends(self):
		"""
		��ȡ�����б�
		"""
		return self.friend_list

	def get_random_user(self):
		"""
		���ѡ���û��������Ѻ�ѡ
		"""
		rand_user = self.user_data_table.get_random_user(const.num_random_friend * 2)
		ret = []
		for user in rand_user:
			notFriend = True
			if user == self.username:
				continue
			for friend in self.friend_list:
				if user == friend:
					notFriend = False
					break
			if notFriend:
				ret.append(user)
				if ret.__len__() >= const.num_random_friend:
					break
		return ret

	def get_fences_msg(self):
		"""
		��ȡ�û�ͨ����������ظ��û�
		"""
		ret = []
		level_list = world.all_fences.level_list
		for i in xrange(self.scene.__len__()):
			if i >= level_list.__len__():
				continue
			level = level_list[i]
			ret.append({'mapID': int(level[0]), 'levelID': int(level[1]), 'stars':self.scene[i]})
		i = i + 1
		while i  < level_list.__len__():
			level = level_list[i]
			ret.append({'mapID': int(level[0]), 'levelID': int(level[1]), 'stars':-1})
			i = i + 1
		return ret

	def get_money(self):
		return (self.gold, self.diamond)

	def add_reward(self, exp = 0, gold = 0, hero_card = None):
		"""
		��ӽ������û�������
		"""
		self.gold = self.gold + gold
		if hero_card:
			self.add_hero(str(hero_card))
		self.legend.add_exp(exp)

	def get_battle_user(self, baseID = 0):
		"""
		���û���������ս����һ��
		"""
		ret = battleUser.battle_user()
		legend = None
		for le in self.legends:
			if self.legends[le].position == 1:
				self.legend = self.legends[le]
				user_legend = self.legends[le].get_legend()
				user_legend.set_id(baseID)
				ret.set_legend(user_legend)
		for hero_id in self.heros:
			hero_data = self.heros[hero_id]
			if hero_data.position > -1:
				hero, heap = hero_data.get_hero(baseID)
				ret.add_hero(hero, heap)
		return ret

	def test_battle_level(self, level):
		"""
		����û��Ƿ������ս�ؿ�level
		"""
		if level[0] < 0:
			# TODO player can pvp only after passed level???
			return True
		#print level
		level_id = world.all_fences.get_level_id(level)
		#print level_id
		#print self.scene
		if level_id < self.scene.__len__() and self.scene[level_id] >= level[2]:
			return True
		else:
			return False

	def pass_scene(self, level):
		"""
		�û�ͨ�أ�����ͨ�ؼ�¼
		"""
		ret = []
		level_id = world.all_fences.get_level_id(level)
		if level_id + 1 == self.scene.__len__():
			self.scene.append(0)
			l = world.all_fences.level_list[level_id + 1]
			ret.append({'mapID': int(l[0]), 'levelID': int(l[1]), 'stars':0})
		if level[2] == self.scene[level_id]:
			self.scene[level_id] = self.scene[level_id] + 1
			l = world.all_fences.level_list[level_id]
			ret.append({'mapID': int(l[0]), 'levelID': int(l[1]), 'stars':int(self.scene[level_id])})
		return ret

	def pay(self, delta_money):
		"""
		�û�����Ʒ���Ľ�Ǯ
		"""
		if self.gold < delta_gold[0] or self.diamond < delta_gold[1]:
			return False
		self.gold = self.gold - delta_gold[0]
		self.diamond = self.diamond = delta_gold[1]
		return True

	def earn(self, delta_money):
		"""
		�û���Ǯ����
		"""
		self.gold = self.gold + delta_gold[0]
		self.diamond = self.diamond + delta_gold[1]
		return True

	def add_hero(self, hero_name):
		"""
		�û�����µĿ���
		"""
		hero = self.heros_table.add_hero(self.username, hero_name)
		self.heros[hero.heroId] = hero
		return hero

	def remove_hero(self, heroId):
		"""
		�û����Ʊ�ɾ��(ǿ��ʱ)
		"""
		self.heros_table.remove_hero(heroId)
		self.heros.pop(heroId)

	def set_hero_position(self, heap1, heap2, heap3):
		"""
		���
		"""
		for heroid in self.heros:
			self.heros[heroid].position = -1
		for heroid in heap1:
			self.heros[heroid].position = 0
		for heroid in heap2:
			self.heros[heroid].position = 1
		for heroid in heap3:
			self.heros[heroid].position = 2

	def add_legend(self, legend_name):
		"""
		��ȡһ���µĴ��濨
		"""
		legend = self.legend_table.add_legend(self.username, legend_name)
		self.legends[legend.legendId] = legend
		return legend

	def set_legend(self, legend_id):
		"""
		���ò�ս����
		"""
		for leid in self.legends:
			self.legends[leid].position = 0
		self.legends[legend_id].position = 1
		self.legend = self.legends[legend_id]

	def get_heros(self):
		"""
		��ȡ�û�����Ӣ�ۿ���
		"""
		ret = []
		for hero_id in self.heros:
			hero_data = self.heros[hero_id]
			hero_id = hero_data.heroId
			hero_name = hero_data.name
			hero_level = hero_data.level
			position = hero_data.position
			(hp, atk) = world.heros.get_hero_data(hero_data.name, hero_data.level)
			ret.append({'pos': position, 'uuid': hero_id, 'id': int(float(hero_name)), 'hp': int(hp), 'atk': int(atk), 'level': hero_level})
		return ret

	def upgrade_card(self, upgrade_hero_id, food_heros_id):
		"""
		����ǿ��
		"""
		if upgrade_hero_id in self.heros:
			legal = True
			for food in food_heros_id:
				if not(food in self.heros):
					legal = False
			if legal:
				upgrade_hero = self.heros[upgrade_hero_id]
				food_heros = [self.heros[food_id] for food_id in food_heros_id]
				world.upgrade_hero.upgrade(self, upgrade_hero, food_heros)
				return upgrade_hero
			else:
				return None
		else:
			return None

import xlrd

if __name__ == '__main__':
	create_new_user.create('test_user')
	data = user_data('test_user')
	print data.username
	print data.heros

