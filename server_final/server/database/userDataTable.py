# -*- coding: utf-8 -*-
# �洢�û���������͹ؿ����� ����Ϣ

import database
import const
import const

import time

class user_data_table(database.database):
	"""
	�洢�û����ݵ����ݿ�
	���ݿ�ṹ��
		username��	�û���
		gold��		Ǯ
		diamond��	
		scene��		�ؿ�����
		power��		����ֵ
		updateTime��	����ֵ����ʱ��(δ����)
	"""
	def __init__(self):
		super(user_data_table, self).__init__()
		#self.db = database.database(const_db.database)
		self.table = self.get_cursor()
		self.table_name = const.user_data_table

	def add_user(self, username):
		"""
		���û�ע�ᣬ��ʼ����Ϣ
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
		��ĳ��ʱ��㣬ˢ�»���ֵ
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
		�����û���Ϣ
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
		��ȡ�û�����
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
		�����ݿ������ѡ���һЩ�û����ṩ���û����Ա����������Ӻ���
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

