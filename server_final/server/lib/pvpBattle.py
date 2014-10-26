# -*- coding: utf-8 -*-

import world
import battle

class pvp_battle(battle.battle):
	"""
	pvp��ս���࣬��һ��ս���������ǣ�pvpս��һ��ʼ��ֱ�ӿ���ֱ������
	"""
	def __init__(self, player_id, enemy_name):
		player_data = world.onlineUsers.get_user(player_id)
		#player_data = user_data.user_data(player_name)
		player = player_data.get_battle_user()
		#enemy_data = user_data.user_data(enemy_name)
		enemy_data = world.db_user_data.get_user_data(enemy_name)
		if enemy_data == None:
			enemy = None
		else:
			enemy = enemy_data.get_battle_user(4)
		super(pvp_battle, self).__init__(player, enemy)

	def fight(self):
		"""
		��ʼս��
		"""
		ret = []
		death, process = self.start_battle()
		ret.extend(process)
		if not death:
			process = self.step_all()
			ret.extend(process)
		return self.win(), ret

