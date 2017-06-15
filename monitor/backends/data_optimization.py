#!/usr/bin/env python
# -*- coding:utf-8 -*-

from Automation34 import settings
import time
import json
import copy

class DataHandler(object):

	def __init__(self,client_id,service_name,monitor_data,Redis_obj):
		self.client_id = client_id
		self.service_name = service_name
		self.monitor_data = monitor_data
		self.Redis_obj = Redis_obj
		self.latest_key = 'Data_%s_%s_latest'%(self.client_id,self.service_name)
		self.process_and_save()



	def process_and_save(self):

		if self.monitor_data['status'] == 0:
			if self.monitor_data['gameserver']:
				redis_key = 'Data_gamesrv_%s' %  self.client_id
				self.Redis_obj.rpush(redis_key,self.monitor_data)
				if self.Redis_obj.llen(redis_key) > 300:
					self.Redis_obj.lpop(redis_key)

			else:
				for type_key,type_val in settings.data_optimization_type.items():
					key_in_redis = 'Data_%s_%s_%s' % (self.client_id,self.service_name,type_key)

					last_point = self.Redis_obj.lrange(key_in_redis,-1,-1)
					if not last_point:
						self.Redis_obj.rpush(key_in_redis,json.dumps([None,time.time()]))
					if type_val[0] == 0:
						self.Redis_obj.rpush(key_in_redis,json.dumps([self.monitor_data,time.time()]))
					else:
						last_point_data,last_point_time = json.loads(self.Redis_obj.lrange(key_in_redis,-1,-1)[0].decode())

						if time.time() - last_point_time > type_val[0]:
							data_set = self.get_data_set(self.latest_key,type_val[0])
							optimized_data = self.data_optimized(data_set)

							self.save_data(key_in_redis,optimized_data)

		else:
			print('monitor data is invalid')

	def save_data(self,key_in_redis,optimized_data):

		self.Redis_obj.rpush(key_in_redis,json.dumps([optimized_data,time.time()]))


	def data_optimized(self,data_set):

		optimized_data = {}
		temp_data_dict = {}

		for key in data_set[0][0].keys():
			optimized_data[key] = []
			temp_data_dict[key] = []

		for data_item in data_set:
			for index,val in data_item[0].items():
				temp_data_dict[index].append(round(float(val),2))

		for k,vlist in temp_data_dict.items():
			avg_res = self.get_avg(vlist)
			max_res = self.get_max(vlist)
			min_res = self.get_min(vlist)

			optimized_data[k] = [avg_res,max_res,min_res]
		return optimized_data

	def get_avg(self,data_set):

		if len(data_set) > 0:
			return sum(data_set)/len(data_set)
		else:
			return 0

	def get_max(self,data_set):

		if len(data_set) > 0:
			return max(data_set)
		else:
			return 0

	def get_min(self,data_set):

		if len(data_set) > 0:
			return min(data_set)
		else:
			return 0

	def get_data_set(self,key_in_redis,interval):
			data_set = []
			all_latest_data = self.Redis_obj.lrange(key_in_redis,1,-1)
			temp_data = copy.deepcopy(all_latest_data)
			temp_data.reverse()
			for data_item in temp_data:
				data = json.loads(data_item.decode())
				if time.time() - data[1] < interval:
					data_set.append(data)
				else:
					break
			return data_set














