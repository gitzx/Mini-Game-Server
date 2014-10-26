# -*- coding: utf-8 -*-

import const
import MySQLdb

if __name__ == '__main__':
	host = const.host
	port = const.port
	user = const.username
	passwd = const.password

	#if True:
	try:
		conn = MySQLdb.connect(host = host, port = port, user = user, passwd = passwd)
		cur = conn.cursor()
		cur.execute("create database if not exists " + const.database) # create database
		conn.select_db(const.database)

		command = 'create table ' + const.passwd_table + '(username char(' + str(const.username_maxlen) + '), passwd char(' + str(const.passwd_maxlen) + '), primary key(username))'
		cur.execute(command) # create passwd_table

		command = 'create table ' + const.friend_table + '(username char(' + str(const.username_maxlen) + '), friend char(' + str(const.username_maxlen) + '))'

		cur.execute(command) # friend_table

		command = 'create table ' + const.hero_table + '(heroId int unsigned not null auto_increment, heroName char(' + str(const.hero_name_maxlen) + ') not null,  owner char(' + str(const.username_maxlen) + '), level tinyint default 0, exp int default 0, position tinyint default -1, primary key(heroId))'
		cur.execute(command) # hero_table

		command = 'create table ' + const.legend_table + '(legendId int unsigned not null auto_increment, legendName char(' + str(const.legend_name_maxlen) + ') not null, owner char(' + str(const.username_maxlen) + '), level tinyint default 0, exp int default 0, position tinyint default 0, primary key(legendId))'
		cur.execute(command)

		command = 'create table ' + const.pvp_rank_table + '(username char(' + str(const.username_maxlen) + '), rank int unsigned not null auto_increment, primary key(rank))'
		#print command
		cur.execute(command) # pvp rank table

		command = 'create table ' + const.user_data_table + '(username char(' + str(const.username_maxlen) + ') not null, gold int default 0, diamond int default 0, scene char(' + str(const.scene_maxlen) + ') default "0", power tinyint default 90, updateTime int unsigned, primary key(username))'
		cur.execute(command) # userdata table
		cur.close()
		conn.close()
	except:
		print 'Error when init database'

