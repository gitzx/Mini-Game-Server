# -*- coding: utf-8 -*-

#host = '10.240.34.63'
host = '127.0.0.1'	# 数据库地址
username = 'root'	# 数据库用户名
password = '123456'	# 数据库密码
port = 3306		# 数据库端口号

database = 'game'		# 游戏所使用的数据库名称
passwd_table = 'password'	# 用户名和密码的存储表
friend_table = 'friend'		# 好友信息存储表
hero_table = 'hero'		# 英雄卡牌信息存储表
legend_table = 'legend'		# 传奇卡牌信息存储表
user_data_table = 'userdata'	# 用户基本信息存储表(金钱，通关情况等)
pvp_rank_table = 'pvprank'	# pvp中的排名情况

username_maxlen = 20		# 用户名最大长度
username_minlen = 6		# 用户名最小长度
passwd_maxlen = 130		# 密码最大长度
passwd_minlen = 6		# 密码最小长度
hero_name_maxlen = 20		# 英雄名最大长度
legend_name_maxlen = 20		# 传奇名最大长度

scene_maxlen = 200		# 关卡数量最大值

num_random_pvp = 5

power_max = 90

