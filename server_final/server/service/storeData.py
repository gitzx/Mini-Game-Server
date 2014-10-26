# -*- coding: utf-8 -*-

import time
import world
import const

class store_data(object):
	"""
	将内存中的数据存储到数据库中
	"""
	def __init__(self):
		self.update_time = time.time()

	def store(self):
		"""
		存储数据
		"""
		print 'data storing'
		world.onlineUsers.store()
		world.task_time.add_task(time.time() + const.per_store_time, self.store)
		print 'data stored'
		world.logger.append('data stored')

