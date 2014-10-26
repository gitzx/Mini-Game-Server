# -*- coding: utf-8 -*-

import xlrd
from lib.fence import fence

class raw_fences(object):
	def __init__(self):
		self.fences = {} # level ~ level_data ���ڼ�¼���йؿ�������
		self.level_list = [] # ����ؿ��б����ڲ���ʵ�ʹؿ��Ͷ�Ӧ���

	def get_level_id(self, level):
		"""
		��ʵ�ʹؿ�����ؿ����
		"""
		try:
			level = (level[0], level[1])
			for (i, lv) in enumerate(self.level_list):
				if lv == level:
					return i
			print 'unknow level'
			raise Exception('unknow level')
		except:
			return None

	def get_level(self, table, row):
		"""
		�ӱ��еĵ�row�е���levelֵ
		"""
		scene = table.cell(row, 0).value
		level = table.cell(row, 1).value
		if scene == '':
			return None
		else:
			return (int(scene), int(level))

	def get_legend_name(self, table, row):
		"""
		�ӱ��еĵ�row�е���legend����
		"""
		name = table.cell(row, 5).value
		return name

	def get_legend(self, table, row):
		"""
		�ӱ��еĵ�row�е���legend����[���֣�����hp��speed]
		"""
		name = table.cell(row, 5).value
		return [name, (1, 1, 1), (200, 200, 200), (1, 1, 1)]

	def get_hero(self, table, row):
		"""
		�ӱ��е�row�л�ȡӢ�ۿ��Ƶ�����[���֣�����λ��]
		"""
		name = int(table.cell(row, 11).value)
		name = str(name)
		po1 = int(table.cell(row, 13).value)
		po2 = int(table.cell(row, 14).value)
		po3 = int(table.cell(row, 15).value)
		lv1 = int(table.cell(row, 16).value)
		lv2 = int(table.cell(row, 17).value)
		lv3 = int(table.cell(row, 18).value)
		return [name, (lv1, lv2, lv3), (po1, po2, po3)]

	def load(self, filename, table_id):
		"""
		���ļ�filename�ĵ�table_id�����е�������
		"""
		try:
			data = xlrd.open_workbook(filename)
			table = data.sheets()[table_id]

			level = None

			for i in xrange(2, table.nrows):
				tlevel = self.get_level(table, i)
				if tlevel:
					if level:
						self.fences[level] = fence_data
						self.level_list.append(level)
					level = tlevel
					fence_data = fence(level)

					legend_name = self.get_legend_name(table, i)
					fence_data.set_legend_name(legend_name)
					legend = self.get_legend(table, i)
					fence_data.set_legend(legend)

					hero = self.get_hero(table, i)
					fence_data.add_hero(hero)
				else:
					hero = self.get_hero(table, i)
					fence_data.add_hero(hero)
			if level:
				self.fences[level] = fence_data
				self.level_list.append(level)
			return True
		except:
			return False

	def get_guard(self, scene, level, stars):
		"""
		�ɹؿ���Ϣ����ս���û�����
		"""
		#print scene
		#print level
		#for lv in self.fences:
		#	print lv
		if (scene, level) in self.fences:
			try:
				return self.fences[(scene, level)].get_enemy(stars)
			except:
				print 'Error when create guard ' + str(scene) + ',' + str(level) + ',' + str(stars)
				return None
		else:
			print 'unknow level, no guard created'
			return None

