# -*- coding: utf-8 -*-

import battleUser

class battle(object):
	"""
	ս���࣬һ�������ʾһ��ս��
	"""
	def __init__(self, player, enemy):
		#���ö�ս˫��
		self.player = player
		self.enemy = enemy
	
	def ready(self):
		"""
		�ж�ս�����Ƿ�ɹ�����
		"""
		if not self.player:
			return False
		if not self.enemy:
			return False
		return True

	def set_level(self, level):
		"""
		ˢ����ʱ��¼�ؿ���Ϣ���Ա���㽱��
		"""
		self.level = level

	def prepare_battle(self):
		"""
		ս��֮ǰ��׼������Ҫ������������г��Ƶ�˳��
		"""
		if not self.ready():
			return None
		self.player.init_heap()
		self.enemy.init_heap()

	def start_battle(self):
		"""
		ս����ʼ���û����Բ����Ľ׶�
		"""
		if not self.ready():
			return True, []
		ret = []
		if self.enemy.get_speed() > self.player.get_speed():
			process = self.enemy.attack(self.player, False)
			if process.__len__() > 0:
				ret.append(process)
			process = self.enemy.attack(self.player)
			if process.__len__() > 0:
				ret.append(process)
		else:
			process = self.player.attack(self.enemy, False)
			if process.__len__() > 0:
				ret.append(process)
		#self.output([ret], 0)
		#self.player.output()
		#self.enemy.output()
		if not self.player.alive():
			return True, [ret]
		return False, [ret]

	def move(self, _from, _to):
		"""
		ս���е������Ƶ�λ��
		"""
		if not self.ready():
			return 
		self.player.move(_from, _to)

	def output(self, data, indent):
		"""
		���ս������
		"""
		if type(data) == type({}):
			f = file('log.txt', 'a')
			for i in xrange(indent):
				f.write('\t')
				#print '\t',
			#print data
			f.write('{')
			print str(data)
			for key in data:
				print key
				f.write(str(key))
				f.write(':')
				#print type(data[key])
				#print type(u"")
				if type(data[key]) == type(u""):
					f.write(data[key].encode('gbk'))
				else:
					f.write(str(data[key]))
				f.write(',')
			f.write('}\n')
			#f.write('u"' + str(data) + '"\n')
			f.close()
		else:
			f = file('log.txt', 'a')
			for i in xrange(indent):
				#print '\t',
				f.write('\t')
			#print '['
			f.write('[\n')
			f.close()
			for subdata in data:
				self.output(subdata, indent + 1)
			f = file('log.txt', 'a')
			for i in xrange(indent):
				#print '\t',
				f.write('\t')
			#print ']'
			f.write(']\n')
			f.close()

	def step(self):
		"""
		ս��һ�غ�
		"""
		if not self.ready():
			return True, []
		ret = []
		process = self.player.attack(self.enemy)
		if process.__len__() > 0:
			ret.append(process)
		if not self.enemy.alive():
			return True, [ret]
		if not self.player.alive():
			return True, [ret]
		process = self.enemy.attack(self.player)
		if process.__len__() > 0:
			ret.append(process)
		if not self.player.alive():
			return True, [ret]
		if not self.enemy.alive():
			return True, [ret]
		#self.output([ret], 0)
		#print 'player:'
		#self.player.output()
		#print 'computer:'
		#self.enemy.output()
		print 'step over'
		#print ''
		return False, [ret]

	def step_all(self):
		"""
		�Զ�ս����ֱ������
		"""
		if not self.ready():
			return True, []
		ret = []
		while True:
			death, process = self.step()
			#if death:
				#self.output(process, 0)
				#print 'player:'
				#print self.player.alive()
				#print self.player.legend.hp
				#print type(self.player)
				#self.player.output()
				#print 'computer:'
				#self.enemy.output()
				#print 'step over'
				#print 'legend level: ',
				#print self.player.legend.level
				#raw_input('click Enter to continue')
			ret.extend(process)
			if death:
				break
		return ret

	def get_situation(self):
		"""
		��ȡ����״���������ڿ�ʼս��ʱ��ͻ���ͬ����Ϣ
		"""
		if not self.ready():
			return {}
		player = self.player.get_situation()
		computer = self.enemy.get_situation()
		return {'player': player, 'computer': computer}

	def win(self):
		"""
		�ж�ս���Ƿ�ʤ��
		"""
		if not self.ready():
			return False
		return self.player.alive()

