# -*- coding: utf-8 -*-

# 处理pvp的操作

import service
import const
import world
import json
from lib import pvpBattle

class pvp_service(service.service):
	def __init__(self):
		super(pvp_service, self).__init__(const.pvp_service_id)
		commands = {
				const.pvp_get_list: self.handle_get_list,
				const.pvp_fight: self.handle_fight
				}
		self.registers(commands)
		self.pvp_table = world.db_pvp

	def handle_get_list(self, msg, sender):
		"""
		获取pvp中可以挑战的对象列表
		"""
		player_id = msg.get(const.identification_id)
		player_data = world.onlineUsers.get_user(player_id, sender)
		if not player_data:
			return
		pvp_list = self.pvp_table.get_pvp_list(player_data.username)
		# return pvp_list
		ret = {const.sid: const.pvp_service_id, const.cid: const.pvp_get_list, const.result_data_id: pvp_list}
		sender.send(json.dumps(ret))

	def handle_fight(self, msg, sender):
		"""
		选择了对象之后开始pk
		"""
		player_id = msg.get(const.identification_id)
		player_data = world.onlineUsers.get_user(player_id, sender)
		if not player_data:
			return
		player_name = player_data.username
		enemy_name = msg.get('target')
		# TODO test if enemy is a user
		battle = pvpBattle.pvp_battle(player_id, enemy_name)
		if battle == None or not battle.ready():
			return
		rank_p = self.pvp_table.get_rank(player_name)
		rank_e = self.pvp_table.get_rank(enemy_name)
		if rank_p < rank_e:
			return
		world.logger.append('pvp ' + player_name + ' vs ' + enemy_name)
		battle.prepare_battle()
		ret = {const.cid: const.start_battle_command_id, const.sid: const.battle_service_id, const.result_data_id: battle.get_situation()}
		sender.send(json.dumps(ret))
		win, process = battle.fight()
		ret = {const.cid: const.step_all_battle_command_id, const.sid: const.battle_service_id, const.result_data_id: process}
		sender.send(json.dumps(ret))
		if win:
			self.pvp_table.exchange(player_name, enemy_name, rank_p, rank_e)
			world.logger.append('pvp ' + player_name + ' win')
			ret = {const.sid: const.battle_service_id, const.cid: const.battle_result_command_id, const.result_data_id: {'gold': 0, 'diamond': 0, 'exp': 0, 'result': 'win'}}
		else:
			world.logger.append('pvp ' + player_name + ' lose')
			ret = {const.sid: const.battle_service_id, const.cid: const.battle_result_command_id, const.result_data_id: {'gold': 0, 'diamond': 0, 'exp': 0, 'result': 'lose'}}
		sender.send(json.dumps(ret))
		# TODO: 
		#sender.send()

