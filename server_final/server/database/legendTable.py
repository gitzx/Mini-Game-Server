# -*- coding: utf-8 -*-

import database
import const
from lib import legendData

class legend_table(database.database):
	"""
	�洢�������ݵ����ݿ⡣
	���ݿ�ṹ��
		legendId��	������
		legendName��	��������
		owner��		ӵ�����û���
		level��		�ȼ�
		exp��		����
		position��	�ڿ����е�λ��0 ���ϳ� 1 �ϳ�
	"""
	def __init__(self):
		super(legend_table, self).__init__()
		#self.db = database.database(const_db.database)
		self.table = self.get_cursor()
		self.table_name = const.legend_table

	def add_legend(self, username, legend_name):
		"""
		�����ݿ������һ�����������
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
		���±��Ϊlegend_id��legend����
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
		��ȡ�û�username�����д�����б�
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

