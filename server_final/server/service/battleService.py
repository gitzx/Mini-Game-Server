# -*- coding: utf-8 -*-

import json
import const
import world
import service

class battle_service(service.service):
	def __init__(self):
		super(battle_service, self).__init__(const.battle_service_id)

		commands = {const.start_battle_command_id: self.handle_start,
				const.step_one_battle_command_id: self.handle_step,
				const.step_all_battle_command_id: self.handle_toEnd,
				const.move_card_command_id: self.handle_move
				}
		self.registers(commands)

	def handle_start(self, msg, sender):
		"""
		开始战斗
		"""
		user = msg.get(const.identification_id)
		if world.onlineUsers.get_user(user, sender) == None:
			return
		battle = world.battles.add_battle(user, msg.get('level'))
		if battle == None:
			return False
		world.logger.append('battle ' + user + str(msg.get('level')))
		battle.prepare_battle()
		ret = {const.cid: const.start_battle_command_id, const.sid: const.battle_service_id, const.result_data_id: battle.get_situation()}
		sender.send(json.dumps(ret))
		death, process = battle.start_battle()

		if process.__len__() < 1:
			return 

		if death:
			user = msg.get(const.identification_id)
			world.battles.remove_battle(user)
			process = {const.cid:  const.step_all_battle_command_id, const.sid: const.battle_service_id, const.result_data_id: process}
		else:
			process = {const.cid:  const.step_one_battle_command_id, const.sid: const.battle_service_id, const.result_data_id: process}
		sender.send(json.dumps(process))

	def output(self, data, indent):
		if type(data) == type({}):
			for i in xrange(indent):
				print '\t',
			print eval('u"' + data.__str__() + '"')
		else:
			for i in xrange(indent):
				print '\t',
			print '['
			for subdata in data:
				self.output(subdata, indent + 1)
			for i in xrange(indent):
				print '\t',
			print ']'

	def handle_step(self, msg, sender):
		"""
		战斗进行一回合
		"""
		new_scene = None
		reward = None
		battle_result = None
		user = msg.get(const.identification_id)
		if world.onlineUsers.get_user(user, sender) == None:
			return
		battle = world.battles.get_battle(user)
		if not battle:
			return 
		death, ret = battle.step()
		#self.output(ret, 0)
		if death:
			user = msg.get(const.identification_id)
			ret = {const.cid:  const.step_all_battle_command_id, const.sid: const.battle_service_id, const.result_data_id: ret}
			level = battle.level
			reward = world.reward.get_reward(level[0], level[1], level[2], True, battle.win())
			world.onlineUsers.get_user(user).add_reward(exp = reward[0], gold = reward[1], hero_card = reward[2])
			if battle.win():
				new_scene = world.onlineUsers.get_user(user).pass_scene(level)
				battle_result = 'win'
			else:
				battle_result = 'lose'
			world.logger.append('battle ' + user + ' ' + battle_result)
			world.logger.append('battleReward ' + user + ' ' + str(reward))
			#f = file('log.txt', 'a')
			#f.write('exp: ' + str(reward[0]))
			#f.write(' gold: ' + str(reward[1]))
			#f.write(' new hero: ' + str(reward[2]))
			#f.close()
			#f = file('result.txt', 'a')
			if battle.win():
				print 'player win'
			#	f.write('player win\n')
			else:
				print 'computer win'
			#	f.write('computer win\n')
			#f.close()
			world.battles.remove_battle(user)
		else:
			ret = {const.cid:  const.step_one_battle_command_id, const.sid: const.battle_service_id, const.result_data_id: ret}
		#print json.dumps(ret)
		sender.send(json.dumps(ret))
		if new_scene:
			ret = {const.sid: 'DataUpdate', const.cid: 'MapLevels', const.result_data_id: new_scene}
			sender.send(json.dumps(ret))
		if reward:
			ret = {const.sid: const.battle_service_id, const.cid: const.battle_result_command_id, const.result_data_id: {'gold': reward[1], 'diamond': 0, 'exp': reward[0], 'result': battle_result}}
			sender.send(json.dumps(ret))
			if reward[2]:
				heros = world.onlineUsers.get_user(user).get_heros()
				ret = {const.sid: 'DataUpdate', const.cid: 'Formation', const.result_data_id: heros}
				sender.send(json.dumps(ret))

	def handle_move(self, msg, sender):
		"""
		战斗中移动卡牌
		"""
		user = msg.get(const.identification_id)
		if world.onlineUsers.get_user(user, sender) == None:
			return
		battle = world.battles.get_battle(user)
		if not battle:
			return 
		result = msg.get('result')
		from_heap = result.get(const.move_from_heap)
		from_po = result.get(const.move_from_po)
		to_heap = result.get(const.move_to_heap)
		to_po = result.get(const.move_to_po)
		battle.move([from_heap, from_po], [to_heap, to_po])
		#print 'player:'
		#battle.player.output()
		#print 'computer:'
		#battle.enemy.output()

	def handle_toEnd(self, msg, sender):
		"""
		自动战斗，直到结束
		"""
		new_scene = None
		battle_result = None
		user = msg.get(const.identification_id)
		if world.onlineUsers.get_user(user, sender) == None:
			return
		battle = world.battles.get_battle(user)
		if not battle:
			return 
		ret = battle.step_all()
		#self.output(ret, 0)
		user = msg.get(const.identification_id)
		ret = {const.cid: const.step_all_battle_command_id, const.sid: const.battle_service_id, const.result_data_id: ret}
		#print json.dumps(ret)

		level = battle.level
		reward = world.reward.get_reward(level[0], level[1], level[2], True, battle.win())
		world.onlineUsers.get_user(user).add_reward(exp = reward[0], gold = reward[1], hero_card = reward[2])
		if battle.win():
			new_scene = world.onlineUsers.get_user(user).pass_scene(level)
			battle_result = 'win'
		else:
			battle_result = 'lose'
		#f = file('log.txt', 'a')
		#f.write('level: ' + str(level[0]) + '\t' + str(level[1]) + '\t' + str(level[2]) + '\n')
		#f.write('exp: ' + str(reward[0]))
		#f.write(' gold: ' + str(reward[1]))
		#f.write(' new hero: ' + str(reward[2]))
		#if reward[2]:
		#	f.write(' new hero: ' + world.heros.get_hero_card_name(str(reward[2])).encode('gbk'))
		#else:
		#	f.write(' new hero: None')
		#f.write('\n')
		#f.write('-' * 80)
		#f.write('\n')
		#f.close()
		#f = file('result.txt', 'a')
		if battle.win():
			print 'player win'
		#	f.write('player win\n')
		else:
			print 'computer win'
		#	f.write('computer win\n')
		#f.close()

		sender.send(json.dumps(ret))
		world.logger.append('battle ' + user + ' ' + battle_result)
		world.logger.append('battleReward ' + user + ' ' + str(reward))
		world.battles.remove_battle(user)
		if new_scene:
			ret = {const.sid: 'DataUpdate', const.cid: 'MapLevels', const.result_data_id: new_scene}
			sender.send(json.dumps(ret))
		if reward:
			ret = {const.sid: const.battle_service_id, const.cid: const.battle_result_command_id, const.result_data_id: {'gold': reward[1], 'diamond': 0, 'exp': reward[0], 'result': battle_result}}
			sender.send(json.dumps(ret))
			if reward[2]:
				heros = world.onlineUsers.get_user(user).get_heros()
				ret = {const.sid: 'DataUpdate', const.cid: 'Formation', const.result_data_id: heros}
				sender.send(json.dumps(ret))

