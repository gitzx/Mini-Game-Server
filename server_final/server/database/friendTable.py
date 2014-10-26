# -*- coding: utf-8 -*-

import database
import const

class friend_table(database.database):
	"""
	�洢������Ϣ�����ݿ�
	���ݿ�ṹ��
		username��	�û���
		friend:		�����û���
	"""
	def __init__(self):
		super(friend_table, self).__init__()
		#self.db = database.database(const_db.database)
		self.table = self.get_cursor()
		self.table_name = const.friend_table

	def add_friend(self, user1, user2):
		"""
		�û�user1 ����û�user2Ϊ����
		"""
		try:
			self.table = self.get_cursor()
			count = self.table.execute('select * from ' + self.table_name + ' where username = "' + user1 + '" and friend = "' + user2 + '"')
			if count > 0:
				print user1 + ' and ' + user2 + ' are already friends'
				return False
			count = self.table.execute('select * from ' + self.table_name + ' where username = "' + user2 + '" and friend = "' + user1 + '"')
			if count > 0:
				print user1 + ' and ' + user2 + ' are already friends'
				return False
			self.table.execute('insert into ' + self.table_name + ' values("%s", "%s")'%(user1, user2))
			self.commit()
			return True
		except:
			print 'Error in friend table. add_friend'
			raise Exception('unable to add friend')

	def remove_friend(self, user1, user2):
		"""
		�û�user1ɾ������user2
		"""
		try:
			count1 = self.table.execute('delete from ' + self.table_name + ' where username = "' + user1 + '" and friend = "' + user2 + '"')
			#count2 = self.table.execute('delete from ' + self.table_name + ' where username = "' + user2 + '" and friend = "' + user1 + '"')
			self.commit()
			return count1
		except:
			print 'Error in friend table . remove friend'
			raise Exception('unable to remove friend')

	def get_friend_list(self, username):
		"""
		��ȡ�û�username�ĺ����б�
		"""
		try:
		#if True:
			command = 'select friend from ' + self.table_name + ' where username = "' + username + '"'
			count1 = self.table.execute(command)
			ret1 = [data[0] for data in self.table.fetchall()]
			#command = 'select username from ' + self.table_name + ' where friend = "' + username + '"'
			#count2 = self.table.execute(command)
			#ret2 = [data[0] for data in self.table.fetchall()]
			#ret1.extend(ret2)
			return ret1
		except:
			raise Exception('unable to get friend list')

