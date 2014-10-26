# -*- coding: utf-8 -*-
# 存储用户金币数量和关卡进度 等信息

import database
import const
import const

import time

class user_data_table(database.database):
	"""
	存储用户数据的数据库
	数据库结构：
		username：	用户名
		gold：		钱
		diamond：	
		scene：		关卡进度
		power：		活力值
		updateTime：	活力值更新时间(未启用)
	"""
	def __init__(self):
		super(user_data_table, self).__init__()
		#self.db = database.database(const_db.database)
		self.table = self.get_cursor()
		self.table_name = const.user_data_table

	def add_user(self, username):
		"""
		新用户注册，初始化信息
		"""
		try:
			command = ('insert into ' + self.table_name + ' values("%s", default, default, "0", default,' +str(int(time.time())) + ')')%(username)
			#command = ('insert into ' + self.table_name + ' values("%s", default, default, "000000000000000000000000000000000000000000000000000000000000000000000000000", default,' +str(int(time.time())) + ')')%(username)
			self.table = self.get_cursor()
			self.table.execute(command)
			self.commit()
		except:
			raise Exception('Error when add user data')

	def refresh_power(self):
		"""
		在某个时间点，刷新活力值
		"""
		try:
			command = 'update ' + self.table_name + ' set power = ' + str(const.power_max)
			self.table = self.get_cursor()
			self.table.execute(command)
			self.commit()
		except:
			raise Exception('Error when refresh power')

	def update(self, username, gold, diamond, scene, power, update_time):
		"""
		更新用户信息
		"""
		try:
			command = 'update ' + self.table_name + ' set gold = ' + str(gold) + ', diamond = ' + str(diamond) + ', scene = "' + scene + '", power = ' + str(power) + ', updateTime = ' + str(update_time) + ' where username = "' + username + '"'
			self.table = self.get_cursor()
			self.table.execute(command)
			self.commit()
		except:
			raise Exception('Error when update user data')

	def get_user_data(self, username):
		"""
		获取用户数据
		"""
		try:
			command = 'select username, gold, diamond, scene, power, updateTime from ' + self.table_name + ' where username = "' + username + '"'
			self.table = self.get_cursor()
			self.table.execute(command)
			ret = self.table.fetchall()
			if ret.__len__() < 1:
				raise Exception('no data available with name: ' + username)
			if ret.__len__() > 1:
				raise Exception('in userDataTable, username is primary key, should be unique')
			from lib import userData
			ret =  userData.user_data(ret[0])
			return ret
		except:
			return None
			#raise Exception('Error when get user data')

	def get_random_user(self, num):
		"""
		从数据库中随机选择出一些用户名提供给用户，以便其更容易添加好友
		"""
		try:
			command = 'select username from ' + self.table_name + ' order by rand() limit ' + str(num)
			self.table = self.get_cursor()
			self.table.execute(command)
			allData = self.table.fetchall()
			ret = []
			for data in allData:
				ret.append(data[0])
			return ret
		except:
			raise Exception('Error when get random user')

