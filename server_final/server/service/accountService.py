# -*- coding: utf-8 -*-

import service
import json
import const
import world

class account_service(service.service):
	"""
	处理用户账户的相关信息，其中包括：
		用户注册
		用户登陆
	"""
	def __init__(self):
		super(account_service, self).__init__(const.account_service_id)

		commands = {
				const.register_command_id: self.handle_register,
				const.login_command_id: self.handle_check}
		self.registers(commands)

		self.passwdDB = world.db_password

	def respon_register(self, sender, success):
		"""
		返回注册结果
		"""
		ret = {const.sid:const.account_service_id, const.cid: const.register_command_id, const.result_data_id: success}
		sender.send(json.dumps(ret))

	def handle_register(self, msg, sender):
		"""
		处理注册信息
		TODO: 返回信息中加入原因
		"""
		try:
			username = msg.get(const.username_data_id)
			passwd = msg.get(const.password_data_id)
			if not username.isalnum():
				self.respon_register(sender, False)
				return 
			if not passwd.isalnum():
				self.respon_register(sender, False)
				return 
			if self.passwdDB.insert(username, passwd):
				world.logger.append('newuser ' + username)
				self.respon_register(sender, True)
			else:
				self.respon_register(sender, False)
		except:
			self.respon_register(sender, False)

	def respon_login(self, sender, success, identification):
		"""
		返回登陆结果
		"""
		ret = {const.sid:const.account_service_id, const.cid: const.login_command_id, const.result_data_id: success, const.identification_id: identification}
		sender.send(json.dumps(ret))
		if success:
			user = world.onlineUsers.get_user(identification, sender)
			fences = user.get_fences_msg()
			ret = {const.sid: 'DataUpdate', const.cid: 'MapLevels', const.result_data_id: fences}
			sender.send(json.dumps(ret))
			gold, diamond = user.get_money()
			ret = {const.sid: 'DataUpdate', const.cid: 'AssetData', const.result_data_id: {'gold': gold, 'diamond':diamond, 'exp': 0}}
			sender.send(json.dumps(ret))
			heros = user.get_heros()
			ret = {const.sid: 'DataUpdate', const.cid: 'Formation', const.result_data_id: heros}
			sender.send(json.dumps(ret))

	def handle_check(self, msg, sender):
		"""
		处理用户登陆
		"""
		try:
			username = msg.get(const.username_data_id)
			passwd = msg.get(const.password_data_id)
			password = self.passwdDB.get_passwd(username)
			if password != None and passwd == password:
				identification = world.onlineUsers.add_user(username, sender)
				self.respon_login(sender, True, identification)
				world.logger.append('login ' + username)
			else:
				self.respon_login(sender, False, "")
		except:
			self.respon_login(sender, False, "")

if __name__ == '__main__':
	s = account_service()
	print s.handle_register('g', 'g')
	print s.handle_check('a', 'b')
	print s.handle_check('a', 'c')
	print s.handle_check('g', 'g')

