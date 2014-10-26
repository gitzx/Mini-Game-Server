# -*- coding: utf-8 -*-
"""
用于python对象与json字符串之间的相互转换
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

