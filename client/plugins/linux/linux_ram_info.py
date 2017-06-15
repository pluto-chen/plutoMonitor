#!/usr/bin/env python
# -*- coding:utf-8 -*-

import subprocess

def monitor():

	shell_cmd = "grep 'MemTotal\|MemFree\|Buffers\|^Cached\|SwapTotal\|SwapFree' /proc/meminfo"

	ret = subprocess.check_output(shell_cmd, shell=True)

	if ret:
		print('ret---->', ret, type(ret))
		value_dic = {'status': 0, }
		for i in ret.split('kB\n	'):
			if len(i.strip()):
				print('i----->', i, type(i))
				key = i.split()[0].strip(':')
				value = i.split()[1].strip()
				value_dic[key] = int(value)

		value_dic['SwapUsage'] = int(value_dic['SwapTotal']) - int(value_dic['SwapFree'])
		value_dic['MemUsage'] = int(value_dic['MemTotal']) - (int(value_dic['MemFree'])
															  + int(value_dic['Buffers'])
															  + int(value_dic['Cached']))
	else:
		value_dic = {'status':1}

	return value_dic

