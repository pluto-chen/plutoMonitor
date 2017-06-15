#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import time
import operator

class DataProcesser(object):

	def __init__(self,redis_obj):

		self.redis_obj = redis_obj


	def data_calculating(self,host_id,service_name,trigger_obj):

		res_join = ''
		notify_data = []

		for expression in trigger_obj.triggerexpression_set.select_related():
			expression_handler = Expression(self.redis_obj,expression)
			expression_res = expression_handler.process(host_id,service_name)
			if str(expression_res['process_res']) == 'True':
				notify_data.append(expression_res)
			if expression.logic_type:
				res_join += str(expression_res['process_res']) + ' ' + expression.logic_type + ' '
			else:
				res_join += str(expression_res['process_res'])
		trigger_res = eval(res_join)
		print('service:%s trigger:%s 是否异常'% (service_name,trigger_obj.name),trigger_res)
		if trigger_res:
			self.trigger_notifier()

	def trigger_notifier(self):
		pass




class Expression(object):

	def __init__(self,redis_obj,expression):
		self.redis_obj = redis_obj
		self.expression_obj = expression
		self.process_res ={}

	def process(self,host_id,service_name):

		time_range = int(self.expression_obj.func_args.split(';')[0])*60
		point_count = (time_range + 60)//self.expression_obj.service.interval
		key_in_redis = 'Data_%s_%s_latest'%(host_id,service_name)
		point_set = self.redis_obj.lrange(key_in_redis,-int(point_count),-1)
		app_point_set = [json.loads(i.decode()) for i in point_set]
		valid_point_set =[]

		for point in app_point_set:
			if time.time() - point[1] < self.expression_obj.service.interval:
				valid_point_set.append(point)

		handle_func = getattr(self,'get_%s' % self.expression_obj.mode)
		if handle_func:
			func_data = handle_func(valid_point_set)
			data_dict = {
				'process_res':func_data[0],
				'process_res_val':func_data[1],
				'trigger_expression':self.expression_obj.service_index.key,
				'threshold':self.expression_obj.threshold,
			}
			return data_dict
		else:
			print('no handle func %s' % self.expression_obj.operator)

	def get_avg(self,data_set):

		data_list = []

		for point in data_set:
			var,savingtime = point
			if var:
				data_list.append(var[self.expression_obj.service_index.key])
		data_list = [float(i) for i in data_list]
		avg_res = sum(data_list)/len(data_list)
		judge_res = self.judge(avg_res)
		return [judge_res,avg_res]

	def judge(self,avg_res):
		op_func = getattr(operator,self.expression_obj.operator)
		return op_func(avg_res,self.expression_obj.threshold)






















