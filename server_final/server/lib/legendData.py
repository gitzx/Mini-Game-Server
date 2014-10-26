# -*- coding: utf-8 -*-

import world
import xlrd
import const

class legend_data(object):
	"""
	��¼�������ݣ�����ʵ����
	"""
	def __init__(self, legendId, name, level, exp, position):
		self.legendId = legendId
		self.name = name
		self.level = level
		self.exp = exp
		self.position = position

		self.exp_needed = []

		data = xlrd.open_workbook(const.legend_upgrade_filename)
		table = data.sheets()[0]
		for i in xrange(1, table.nrows):
			exp = table.cell(i, 2).value
			if not exp:
				break
			self.exp_needed.append(exp)

	def get_legend(self):
		"""
		ʵ����һ��legend
		"""
		ret = world.legends.get_legend(self.name, self.level)
		#le = legend.legend(self.name, self.level, 260, self.level)
		return ret

	def set_legend(self):
		"""
		��������Ϊ��ս
		"""
		self.position = 1

	def remove_legend(self):
		"""
		���ô�����Ϣ
		"""
		self.position = 0

	def set_level(self, level):
		self.level = level

	def set_exp(self, exp):
		self.exp = exp

	def add_exp(self, exp):
		self.exp = self.exp + exp
		while self.level < self.exp_needed.__len__() and self.exp >= self.exp_needed[self.level]:
			self.exp = self.exp - self.exp_needed[self.level]
			self.level = self.level + 1

