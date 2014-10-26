# -*- coding: utf-8 -*-

import battleUser

class battle(object):
	"""
	战斗类，一个对象表示一场战斗
	"""
	def __init__(self, player, enemy):
		#设置对战双方
		self.player = player
		self.enemy = enemy
	
	def ready(self):
		"""
		判断战斗类是否成功生成
		"""
		if not self.player:
			return False
		if not self.enemy:
			return False
		return True

	def set_level(self, level):
		"""
		刷副本时记录关卡信息，以便计算奖励
		"""
		self.level = level

	def prepare_battle(self):
		"""
		战斗之前的准备，主要是随机调整堆中出牌的顺序
		"""
		if not self.ready():
			return None
		self.player.init_heap()
		self.enemy.init_heap()

	def start_battle(self):
		"""
		战斗开始到用户可以操作的阶段
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
		战斗中调整卡牌的位置
		"""
		if not self.ready():
			return 
		self.player.move(_from, _to)

	def output(self, data, indent):
		"""
		输出战斗过程
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
		战斗一回合
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
		自动战斗，直到结束
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
		获取队列状况，现用于开始战斗时与客户端同步消息
		"""
		if not self.ready():
			return {}
		player = self.player.get_situation()
		computer = self.enemy.get_situation()
		return {'player': player, 'computer': computer}

	def win(self):
		"""
		判断战斗是否胜利
		"""
		if not self.ready():
			return False
		return self.player.alive()

