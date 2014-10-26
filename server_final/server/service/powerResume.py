# -*- coding: utf-8 -*-

import time
import world

class power_resume(object):
	"""
	Ϊˢ�»���������ṩ����
	"""
	def __init__(self):
		self.database = world.db_user_data

	def get_resume_time(self):
		"""
		��ȡ��һ��ˢ�µ�ʱ��
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
		ˢ�»�����
		"""
		world.onlineUsers.refresh_power()
		self.database.refresh_power()
		world.task_time.add_task(self.get_resume_time, self.get_resume_time)

