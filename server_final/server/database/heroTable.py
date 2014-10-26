# -*- coding: utf-8 -*-

import database
import const
from lib import heroData

class hero_table(database.database):
	"""
	 存储英雄卡牌的数据库
	 用户出现的每张卡牌都存储在数据库中
	 数据库结构：
	 	heroId: 	英雄卡牌的唯一编号
	 	heroName:	英雄名称
	 	owner:		拥有人用户名
	 	level:		卡牌强化级别
	 	exp:		卡牌强化剩余经验
	 	position:	卡牌在牌组中的位置 -1 不上场， 012分别表示在三列中
	"""
	def __init__(self):
		super(hero_table, self).__init__()
		#self.db = database.database(const.database)
		self.table = self.get_cursor()
		self.table_name = const.hero_table

	def add_hero(self, username, hero_name, level = 0, exp = 0, position = -1):
		"""
		添加一个英雄到数据库中
		"""
		try:
			# value格式：id, heroName, userName, level, exp, position
			command = 'insert into ' + self.table_name + ' values(0, "' + hero_name + '", "' + username + '", ' + str(level) + ', ' + str(exp) + ', ' + str(position) + ')'
			if isinstance(command, unicode):
				command = command.encode('utf-8')
			self.table = self.get_cursor()
			self.table.execute(command)
			self.table.execute('select last_insert_id()')
			_id = self.table.fetchone()
			ret = heroData.hero_data(_id[0], hero_name, 0, 0, -1)
			self.commit()
			return ret
		except:
			raise Exception('Error when insert new hero into heroTable')

	def add_heros(self, hero_datas):
		"""
		添加多个英雄
		"""
		try:
		#if True:
			if hero_datas.__len__() < 1:
				return
			command = 'insert into ' + self.table_name + ' values'
			first_data = True
			for data in hero_datas:
				if not first_data:
					command = command + ', '
				command = command + '(0, "' + data[0] + '", "' + data[1] + '", ' + str(data[2]) + ', ' + str(data[3]) + ', ' + str(data[4]) + ')'
				first_data = False
			if isinstance(command, unicode):
				command = command.encode('utf-8')
			#print command
			self.table = self.get_cursor()
			ret = self.table.execute(command)
			#print ret
			self.commit()
			return ret
		except:
			raise Exception('Error when insert new hero into heroTable')

	def remove_hero(self, heroId):
		"""
		删除一个英雄数据
		用于强化时使用
		"""
		# TODO 是否有多个同时删除的方法，减少数据库负载
		try:
			command = 'delete from ' + self.table_name + ' where heroId = ' + str(heroId)
			self.table = self.get_cursor()
			self.table.execute(command)
			self.commit()
		except:
			raise Exception('Error when delete hero')

	def remove_heros(self, heroIds):
		"""
		删除多个英雄卡数据
		"""
		try:
			command = 'delete from ' + self.table_name + ' where heroId in (' + str(heroId)
			for id in heroIds:
				if command[-1] != ',':
					command = command + ','
				command = command + str(id)
			command = command + ')'
			self.table = self.get_cursor()
			self.table.execute(command)
			self.commit()
		except:
			raise Exception('Error when delete hero')

	def update_hero(self, hero_id, level, exp, position):
		try:
			command = 'update ' + self.table_name + ' set level = ' + str(level) + ', exp = ' + str(exp) + ', position = ' + str(position) + ' where heroId = ' + str(hero_id)
			if isinstance(command, unicode):
				command = command.encode('utf-8')
			self.table = self.get_cursor()
			self.table.execute(command)
			self.commit()
		except:
			raise Exception('Error when update heroTable')

	def get_hero_list(self, username):
		"""
		获取一个用户所有英雄的列表
		"""
		try:
			command = 'select heroId, heroName, level, exp, position from ' + self.table_name + ' where owner = "' + username + '"'
			self.table = self.get_cursor()
			self.table.execute(command)
			data = self.table.fetchall()
			ret = {}
			for i in data:
				name = i[1]
				if not isinstance(name, unicode):
					name = name.decode('utf-8')
				ret[i[0]] = heroData.hero_data(i[0],name,i[2],i[3],i[4])
			return ret
		except:
			raise Exception('Error when get heroList')

