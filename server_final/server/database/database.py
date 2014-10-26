# -*- coding: utf-8 -*-

import const
import MySQLdb

class database(object):
	"""
	所有数据库的基类，用于数据库的连接
	"""
	def __init__(self, db = None, host = None, user = None, passwd = None, port = None):
		if db == None:
			db = const.database
		if host == None:
			host = const.host
		if user == None:
			user = const.username
		if passwd == None:
			passwd = const.password
		if port == None:
			port = const.port
		try:
			self.conn = MySQLdb.connect(host = host, user = user, passwd = passwd, db = db, port = port)
		except:
			raise Exception('Error when connect database')

	def commit(self):
		self.conn.commit()

	def close(self):
		self.conn.close()

	def get_cursor(self):
		return self.conn.cursor()


if __name__ == '__main__':
	db = database(const.database)

