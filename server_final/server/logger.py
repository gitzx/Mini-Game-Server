# -*- coding: utf-8 -*-

# ���ڼ�¼�򵥵�log

import time

logfilename = 'test_log.txt'

def append(msg):
	f = file(logfilename, 'a')
	f.write(str(time.time()))
	f.write(':' + msg.encode('gbk') + '\n')


if __name__ == '__main__':
	append(u'\u6211\u4eec')

