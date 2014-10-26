# -*- coding: utf-8 -*-

import database
import const
from lib import legendData

class legend_table(database.database):
	"""
	存储传奇数据的数据库。
	数据库结构：
		legendId：	传奇编号
		legendName：	传奇名称
		owner：		拥有者用户名
		level：		等级
		exp：		经验
		position：	在卡牌中的位置0 不上场 1 上场
	"""
	def __init__(self):
		super(legend_table, self).__init__()
		#self.db = database.database(const_db.database)
		self.table = self.get_cursor()
		self.table_name = const.legend_table

	def add_legend(self, username, legend_name):
		"""
		向数据库中添加一个传奇的数据
		"""
		try:
			command = 'insert into ' + self.table_name + ' values(0, "' + legend_name + '", "' + username + '", default, default, default)'
			if isinstance(command, unicode):
				command = command.encode('utf-8')
			self.table = self.get_cursor()
			self.table.execute(command)
			self.table.execute('select last_insert_id()')
			_id = self.table.fetchone()
			ret = legendData.legend_data(_id[0], legend_name, 0, 0, 0)
			self.commit()
			return ret
		except:
			raise Exception('Error when insert new legend into legendTable')

	def update_legend(self, legend_id, level, exp, position):
		"""
		更新编号为legend_id的legend数据
		"""
		try:
			command = 'update ' + self.table_name + ' set level = ' + str(level) + ', exp = ' + str(exp) + ', position = ' + str(position) + ' where legendId = ' + str(legend_id)
			if isinstance(command, unicode):
				command = command.encode('utf-8')
			self.table = self.get_cursor()
			self.table.execute(command)
			self.commit()
		except:
			raise Exception('Error when update legendTable')

	def get_legend_list(self, username):
		"""
		获取用户username的所有传奇的列表
		"""
		try:
			command = 'select legendId, legendName, level, exp, position from ' + self.table_name + ' where owner = "' + username + '"'
			#print command
			self.table = self.get_cursor()
			self.table.execute(command)
			data = self.table.fetchall()
			ret = {}
			for i in data:
				name = i[1]
				if not isinstance(name, unicode):
					name = name.decode('utf-8')
				ret[i[0]] = legendData.legend_data(i[0], name, i[2], i[3], i[4])
			return ret
		except:
			raise Exception('Error when get legendList')

