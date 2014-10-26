# -*- coding: utf-8 -*-

import time

class task(object):
	def __init__(self):
		self.update_time = 0
		self.func = None

class timer(object):
	"""
	计时器，用于处理需要定时完成的任务
	"""
	def __init__(self):
		self.tasks = []

	def add_task(self, update_time, func):
		"""
		加入一个需要在update_time执行的任务：func
		"""
		t = task()
		t.update_time = update_time
		t.func = func
		self.tasks.append(t)

	def click(self):
		"""
		检查是否需要执行某项任务
		"""
		now = time.time()
		for i in range(self.tasks.__len__()-1, -1, -1):
			if now > self.tasks[i].update_time:
				self.tasks[i].func()
				self.tasks.pop(i)

