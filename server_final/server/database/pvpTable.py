# -*- coding: utf-8 -*-

import database
import const
import const

class pvp_table(database.database):
	"""
	用于存储pvp排名的数据库
	数据库结构：
		username：	用户
		rank：		用户的排名
	
	说明：用户注册时初始化排名，之后与之前的用户战斗，胜利则交换排名，失败则不做操作
	可以考虑与userdataTable合并
	"""
	def __init__(self):
		super(pvp_table, self).__init__()
		#self.db = database.database(const_db.database)
		self.table = self.get_cursor()
		self.table_name = const.pvp_rank_table
		self.select_level = [
				[10, 10, 1],
				[50, 10, 0.6],
				[100, 20, 0.30],
				[300, 50, 0.12],
				[1000, 200, 0.03],
				[10000000, 500, 0.012],
				]
		# 随机选择对手的条件：[rank最大值，选择范围，选择概率]

	def add_hero(self, username):
		"""
		新用户注册
		"""
		try:
			command = 'insert into ' + self.table_name + ' values("' + username + '" , 0)'
			self.table = self.get_cursor()
			ret = self.table.execute(command)
			self.commit()
			return ret
		except:
			raise Exception('Error when add new user in pvp')

	def get_rank(self, username):
		"""
		获取用户的排名
		"""
		try:
			command = 'select rank from ' + self.table_name + ' where username = "' + username + '"'
			self.table = self.get_cursor()
			self.table.execute(command)
			data = self.table.fetchall()
			if data.__len__() == 1:
				return data[0][0]
			else:
				raise Exception('Error: ' + username + ' not found or found more then one')
		except:
			raise Exception('Error when get rank for user:' + username)

	def update_rank(self, username, rank):
		"""
		更新用户排名
		"""
		try:
			command = 'update ' + self.table_name + ' set username = "' + username + '" where rank = ' + str(rank)
			self.table = self.get_cursor()
			ret = self.table.execute(command)
			self.commit()
			return ret
		except:
			raise Exception('Error when update user pvp rank')

	def exchange(self, username1, username2, rank1 = None, rank2 = None):
		"""
		战斗胜利，交换排名
		"""
		try:
			if not rank1:
				rank1 = self.get_rank(username1)
			if not rank2:
				rank2 = self.get_rank(username2)
			self.update_rank(username2, rank1)
			self.update_rank(username1, rank2)
		except:
			raise Exception('Error when exchange rank')

	def get_pvp_list(self, username):
		"""
		选择用户username的挑战对象
		"""
		try:
			rank = self.get_rank(username)
			ret = [{'username':"", 'rank':rank}]
			for level in self.select_level:
				if rank < level[0]:
					command = 'select username, rank from ' + self.table_name + ' where rank < ' + str(rank) + ' and rank > ' + str(rank - level[1]) + ' and rand() < ' + str(level[2]) + ' limit ' + str(const.num_random_pvp)
					self.table = self.get_cursor()
					self.table.execute(command)
					data = self.table.fetchall()
					for item in data:
						ret.append({'username': item[0], 'rank': item[1]})
					return ret
					# rank - 1 ~ rank - level[1] pro(level[2], const)
		except:
			raise Exception('Error when get pvp list')

