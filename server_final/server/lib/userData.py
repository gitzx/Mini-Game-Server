# -*- coding: utf-8 -*-
"""
用于记录在线玩家的用户数据：
gold和diamond每隔XX时间写入数据库一次
scene更新时写入数据库
heros和legend每隔XX时间写入数据库一次
friend_list在更新时写入数据库
power为玩家的体力值，每隔6min增长一点，每次战斗消耗5点，上限是const.power_max + 好友数量
power需记录上次加体力值的时间
"""

import battleUser
import world
import const
import time

import xlrd

class new_user(object):
	"""
	初始化一个新用户并存储到数据库中
	"""
	def __init__(self):
		self.legend_table = world.db_legend
		self.hero_table = world.db_hero
		self.user_data = world.db_user_data
		self.pvp_table = world.db_pvp

	def create(self, username):
		"""
		创建用户
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
	记录用户所需的数据
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
		刷新用户的活力值
		"""
		self.power = const.power_max

	def cost_power(self, power):
		"""
		战斗，消耗活力值
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
		将用户数据存储到数据库中
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
		添加好友
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
		删除好友
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
		获取好友列表
		"""
		return self.friend_list

	def get_random_user(self):
		"""
		随机选择用户用作好友候选
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
		获取用户通关情况，返回给用户
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
		添加奖励到用户数据中
		"""
		self.gold = self.gold + gold
		if hero_card:
			self.add_hero(str(hero_card))
		self.legend.add_exp(exp)

	def get_battle_user(self, baseID = 0):
		"""
		由用户数据生成战斗的一方
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
		检查用户是否可以挑战关卡level
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
		用户通关，更新通关纪录
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
		用户买商品消耗金钱
		"""
		if self.gold < delta_gold[0] or self.diamond < delta_gold[1]:
			return False
		self.gold = self.gold - delta_gold[0]
		self.diamond = self.diamond = delta_gold[1]
		return True

	def earn(self, delta_money):
		"""
		用户金钱增加
		"""
		self.gold = self.gold + delta_gold[0]
		self.diamond = self.diamond + delta_gold[1]
		return True

	def add_hero(self, hero_name):
		"""
		用户获得新的卡牌
		"""
		hero = self.heros_table.add_hero(self.username, hero_name)
		self.heros[hero.heroId] = hero
		return hero

	def remove_hero(self, heroId):
		"""
		用户卡牌被删除(强化时)
		"""
		self.heros_table.remove_hero(heroId)
		self.heros.pop(heroId)

	def set_hero_position(self, heap1, heap2, heap3):
		"""
		编队
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
		获取一张新的传奇卡
		"""
		legend = self.legend_table.add_legend(self.username, legend_name)
		self.legends[legend.legendId] = legend
		return legend

	def set_legend(self, legend_id):
		"""
		设置参战传奇
		"""
		for leid in self.legends:
			self.legends[leid].position = 0
		self.legends[legend_id].position = 1
		self.legend = self.legends[legend_id]

	def get_heros(self):
		"""
		获取用户所有英雄卡牌
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
		卡牌强化
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

