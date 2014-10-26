import world
import socket
from network.netstream import netstream
import const
import json

num_of_user = 50
num_of_chat = 3
test_user_name = 'hello111'

host = const.host
port = const.port
addr = (host, port)


if __name__ == '__main__':
	for i in xrange(num_of_user):
		username = 'netease' + str(i)
		password = str(i) * 10

		client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		client.connect(addr)
		client.setblocking(0)
		client = netstream(client)

		identification = world.onlineUsers._get_identification(username)
		data = []
		data.append({'sid': const.account_service_id, 'cid': const.register_command_id, const.username_data_id: username, const.password_data_id: password})
		data.append({'sid': const.account_service_id, 'cid': const.login_command_id, const.username_data_id: username, const.password_data_id: password})

		for j in xrange(num_of_chat):
			msg = '@' + test_user_name + ' ' + username + str(j)
			data.append({'sid': const.chat_service_id, 'cid': const.chat_command_id, const.identification_id: identification, const.result_data_id: msg})
		for msg in data:
			client.send(json.dumps(msg))
			while True:
				s = client.recv()
				if s and s.__len__() > 0:
					pass
				else:
					break
			#print json.dumps(msg)
			#print ''

