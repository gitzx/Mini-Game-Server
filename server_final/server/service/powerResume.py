# -*- coding: utf-8 -*-

import time
import world

class power_resume(object):
	"""
	为刷新活力点操作提供服务
	"""
	def __init__(self):
		self.database = world.db_user_data

	def get_resume_time(self):
		"""
		获取下一次刷新的时间
		"""
		t = time.localtime(time.time())
		y = t.tm_year
		m = t.tm_mon
		d = t.tm_mday
		h = t.tm_hour
		if h < 6:
			ret = time.mktime([y, m, d, 6, 0, 0, 0, 0, 0])
		elif h < 12:
			ret = time.mktime([y, m, d, 12, 0, 0, 0, 0, 0])
		elif h < 18:
			ret = time.mktime([y, m, d, 18, 0, 0, 0, 0, 0])
		else:
			ret = time.mktime([y, m, d+1, 6, 0, 0, 0, 0, 0])
		return ret

	def resume(self):
		"""
		刷新活力点
		"""
		world.onlineUsers.refresh_power()
		self.database.refresh_power()
		world.task_time.add_task(self.get_resume_time, self.get_resume_time)

