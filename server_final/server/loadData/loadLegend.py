# -*- coding: utf-8 -*-

import xlrd
from lib import legend

class raw_legend(object):
	def __init__(self):
		self.legends = {}

	def get_name(self, table, row):
		name = table.cell(row, 0).value
		#print name
		name = str(int(name))
		return name

	def get_hp(self, table, row):
		hp = int(table.cell(row, 4).value)
		hp_grow = int(table.cell(row, 5).value)
		return (hp, hp_grow)

	def get_speed(self, table, row):
		speed = table.cell(row, 7).value
		return (speed, 0.2)

	def load_one_legend(self, table, row):
		name = self.get_name(table, row)
		hp = self.get_hp(table, row)
		speed = self.get_speed(table, row)
		self.legends[name] = [hp, speed]

	def load(self, filename, table_id):
		data = xlrd.open_workbook(filename)
		table = data.sheets()[table_id]
		for i in xrange(1, table.nrows):
			self.load_one_legend(table, i)

	def get_legend(self, legend_name, level):
		if legend_name in self.legends:
			data = self.legends[legend_name]
			ret = legend.legend(legend_name, level, int(data[0][0] + level * data[0][1]), int(data[1][0] + level * data[1][1]))
			return ret
		else:
			return None

