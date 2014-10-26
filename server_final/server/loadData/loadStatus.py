# -*- coding: utf-8 -*-

import xlrd
from lib.status import status

class load_status(object):
	def __init__(self):
		self.all_status = {}
	
	def load(self, filename, table_id = 0):
		data = xlrd.open_workbook(filename)
		table = data.sheets()[table_id]

		for i in xrange(1, table.nrows):
			name = table.cell(i, 0).value
			can_move = table.cell(i, 1).value
			if int(can_move) > 0:
				can_move = True
			else:
				can_move = False
			can_magic = table.cell(i, 2).value
			if int(can_magic) > 0:
				can_magic = True
			else:
				can_magic = False
			can_attack = table.cell(i, 3).value
			if int(can_attack) > 0:
				can_attack = True
			else:
				can_attack = False
			harm_type = table.cell(i, 4).value
			harm_type = int(harm_type)
			harm_before_move = table.cell(i, 5).value
			#harm_before_move = int(harm_before_move)
			harm_after_move = table.cell(i, 6).value
			#harm_after_move = int(harm_after_move)
			harm_when_attacked = table.cell(i, 7).value
			last_time = table.cell(i, 8).value
			can_add_hp = table.cell(i, 9).value
			if int(can_add_hp) > 0:
				can_add_hp = True
			else:
				can_add_hp = False
			last_time = int(last_time)
			st = status(name, can_move, can_magic, can_attack, harm_type, harm_before_move, harm_after_move, harm_when_attacked, last_time, can_add_hp)
			if name in self.all_status:
				raise Exception('status with name: ' + name + ' has already loaded')
			else:
				self.all_status[name] = st

	def get_status(self, name):
		if name in self.all_status:
			return self.all_status[name]
		else:
			print 'status name:',
			print eval('u"' + name + '"')
			raise Exception('no status with name: ' + name)

