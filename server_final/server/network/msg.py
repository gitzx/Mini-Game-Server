# -*- coding: utf-8 -*-
"""
����python������json�ַ���֮����໥ת��
"""

import json

def parser(Msg):
	#print Msg
	try:
		ret = json.loads(Msg)
		return ret
	except:
		return None

def to_msg(obj):
	ret = json.dump(obj)
	return ret

