import world
import const
import socket
import time

from network import msg
from network.network import net
from network.netstream import netstream
from network.connectionPool import connection_pool
from service.mainService import main_service

def test_started():
	try:
		client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		client.connect((const.host, const.port))
		return True
	except:
		return False

if __name__ == '__main__':
	if test_started():
		print 'server have started'
	else:
		print 'server started'
		print 'initilizing'
		host = net()
		online_user = connection_pool()
		serv = main_service()
		net = online_user.recv()
		world.task_time.add_task(time.time() + const.per_store_time, world.data_store.store)
		world.task_time.add_task(world.power_resumer.get_resume_time(), world.power_resumer.resume)
		print 'initilize finished'
		while 1:
			while 1:
				client = host.get_new_connect()
				if not client:
					break
				online_user.add_connection(netstream(client))
			(client, new_msg) = net.next()
			if new_msg:
				new_msg = msg.parser(new_msg)
				if new_msg:
					serv.handle(new_msg, client)

			online_user.click()
			world.task_time.click()

