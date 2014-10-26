# -*- coding: utf-8 -*-
import database
import const

import time

class passwd_table(database.database):
	"""
	用于保存用户密码的数据库
	数据结构：
		username：	用户名
		passwd：	密码
	"""
	def __init__(self):
		super(passwd_table, self).__init__()
		#self.db = database.database(const_db.database)
		self.table = self.get_cursor()
		self.table_name = const.passwd_table

	def insert(self, username, passwd):
		"""
		加入一个新的用户
		"""
		try:
			if username.__len__() < 6 or username.__len__() >= const.username_maxlen or passwd.__len__() < 6 or passwd.__len__() >= const.passwd_maxlen:
				return False
			self.table = self.get_cursor()
			self.table.execute('insert into ' + self.table_name + ' values("%s","%s")'%(username, passwd))
			self.commit()
			from lib import userData
			userData.create_new_user.create(username)
			return True
		except:
			raise Exception('Error when insert into ' + self.table_name)

	def get_passwd(self, username):
		"""
		获取用户username的密码
		"""
		try:
			self.table = self.get_cursor()
			count = self.table.execute('select passwd from ' + self.table_name + ' where username = "' + username + '"')
			if count < 1:
				return None
			elif count == 1:
				ret = self.table.fetchone()
				return ret[0]
			else:
				print 'Error in ' + self.table_name + ': more the one user with same username'
				return False
		except:
			raise Exception('Error when get passwd in '+ self.table_name)

