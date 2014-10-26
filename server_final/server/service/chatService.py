import const
import world
import service

class chat_service(service.service):
	def __init__(self):
		super(chat_service, self).__init__(const.chat_service_id)
		commands = {
				const.chat_command_id: self.handle_chat,
				}
		self.registers(commands)

	def handle_chat(self, msg, sender):
		try:
			identification = msg.get(const.identification_id)
			user_data = world.onlineUsers.get_user(identification, sender)
			if not user_data:
				return
			username = user_data.username
			data = msg.get(const.result_data_id)
			world.logger.append('chat ' + username + ': ' + data)
			#print data
			if data[0] == '@':
				po = data.find(' ')
				if po > 1:
					recv_user_name = data[1:po]
					#print 'name :',
					#print recv_user_name
					recv_user = world.onlineUsers._get_identification(recv_user_name)
					#print recv_user
					if not recv_user:
						return
					data = data[po+1:]
					world.onlineUsers.send_data_one(recv_user, username + ': ' + data)
					world.onlineUsers.send_data_one(identification, username + ': @' + recv_user_name + ' ' + data)
				else:
					return
			else:
				data = username + ': ' + data
				world.onlineUsers.send_data_all(data)
		except:
			pass

