# -*- coding: utf-8 -*-

import time
import world
import const

class store_data(object):
	"""
	���ڴ��е����ݴ洢�����ݿ���
	"""
	def __init__(self):
		self.update_time = time.time()

	def store(self):
		"""
		�洢����
		"""
		print 'data storing'
		world.onlineUsers.store()
		world.task_time.add_task(time.time() + const.per_store_time, self.store)
		print 'data stored'
		world.logger.append('data stored')

