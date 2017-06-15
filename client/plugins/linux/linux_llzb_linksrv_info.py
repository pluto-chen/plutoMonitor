#!/usr/bin/env python
# -*- coding:utf-8 -*-


import subprocess
import re

def monitor():

	shell_cmd = "ps aux|grep kl|grep glinkd"
	monitor_processes = ['zlogd','gdeliveryd','glinkd','gamedbd','gonlineinfod',
						 'gsalias1','gsalias2','gsalias3','gsalias4','gsalias5','gsalias6']
	#ret = subprocess.check_output(shell_cmd,shell=True)
	ret = subprocess.check_output(shell_cmd,shell=True)

	if ret:
		value_dict = {'status':0,'gameserver':True,}
		check_p = {}
		monitor_cout = 0
		for process in monitor_processes:
			check_p[process] = 0
		for item in ret.split('.conf\n'):
			key = re.split(' |/',item)[-1]
			check_p[key] += 1
			monitor_cout += 1
		value_dict['monitor_count'] = monitor_cout
		value_dict.update(check_p)
	else:
		value_dict = {'status':1}
	return value_dict
