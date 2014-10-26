# -*- coding: utf-8 -*-

import database
import const
import const

class pvp_table(database.database):
	"""
	���ڴ洢pvp���������ݿ�
	���ݿ�ṹ��
		username��	�û�
		rank��		�û�������
	
	˵�����û�ע��ʱ��ʼ��������֮����֮ǰ���û�ս����ʤ���򽻻�������ʧ����������
	���Կ�����userdataTable�ϲ�
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
		# ���ѡ����ֵ�������[rank���ֵ��ѡ��Χ��ѡ�����]

	def add_hero(self, username):
		"""
		���û�ע��
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
		��ȡ�û�������
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
		�����û�����
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
		ս��ʤ������������
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
		ѡ���û�username����ս����
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

