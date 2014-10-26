# -*- coding: utf-8 -*-

import json
import const
import world
import service

class hero_service(service.service):
	"""
	处理卡牌方面的问题，包括：
		卡牌升级
		编组
	"""
	def __init__(self):
		super(hero_service, self).__init__(const.update_service_id)
		commands = {
				const.update_heap_command_id: self.handle_update_heap,
				const.upgrade_card_command_id: self.handle_upgrade,
				}
		self.registers(commands)

	def handle_update_heap(self, msg, sender):
		"""
		重新编组
		"""
		data_all = msg.get(const.result_data_id)
		identification = msg.get(const.identification_id)
		user_data = world.onlineUsers.get_user(identification, sender)
		if not user_data:
			return
		heap0 = []
		heap1 = []
		heap2 = []
		for data in data_all:
			if data.get('pos') == 0:
				heap0.append(data.get('uuid'))
			elif data.get('pos') == 1:
				heap1.append(data.get('uuid'))
			elif data.get('pos') == 2:
				heap2.append(data.get('uuid'))
		user_data.set_hero_position(heap0, heap1, heap2)

	def handle_upgrade(self, msg, sender):
		"""
		卡牌升级
		"""
		identification = msg.get(const.identification_id)
		user_data = world.onlineUsers.get_user(identification)
		if not user_data:
			return
		upgrade = msg.get(const.upgrade_card_data_id)
		foods = msg.get(const.food_card_data_id)
		upgrade_card = upgrade.get('uuid')
		food_cards = []
		for food in foods:
			food_cards.append(food.get('uuid'))
		upgraded = user_data.upgrade_card(upgrade_card, food_cards)
		world.logger.append('upgrade ' + str(upgrade_card) + '<' + str(food_cards))
		if upgraded:
			heros = user_data.get_heros()
			ret = {const.sid: 'DataUpdate', const.cid: 'Formation', const.result_data_id: heros}
			sender.send(json.dumps(ret))

			hero_id = upgrade_card
			hero_data = upgraded
			hero_name = hero_data.name
			hero_level = hero_data.level
			position = hero_data.position
			(hp, atk) = world.heros.get_hero_data(hero_data.name, hero_data.level)

			ret = {const.sid: 'DataUpdate', const.cid: 'Enforcement', const.result_data_id: {'pos': position, 'uuid': hero_id, 'id': int(float(hero_name)), 'hp': int(hp), 'atk': int(atk), 'level': hero_level}}
			sender.send(json.dumps(ret))

