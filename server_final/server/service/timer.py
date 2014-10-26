# -*- coding: utf-8 -*-

import time

class task(object):
	def __init__(self):
		self.update_time = 0
		self.func = None

class timer(object):
	"""
	��ʱ�������ڴ�����Ҫ��ʱ��ɵ�����
	"""
	def __init__(self):
		self.tasks = []

	def add_task(self, update_time, func):
		"""
		����һ����Ҫ��update_timeִ�е�����func
		"""
		t = task()
		t.update_time = update_time
		t.func = func
		self.tasks.append(t)

	def click(self):
		"""
		����Ƿ���Ҫִ��ĳ������
		"""
		now = time.time()
		for i in range(self.tasks.__len__()-1, -1, -1):
			if now > self.tasks[i].update_time:
				self.tasks[i].func()
				self.tasks.pop(i)

