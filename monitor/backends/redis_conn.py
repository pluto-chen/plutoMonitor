#!/usr/bin/env python
# -*- coding:utf-8 -*-


import redis

def redis_conn(settings):
	pool = redis.ConnectionPool(host=settings.Redis_info['Host'],port=settings.Redis_info['Port'])
	r = redis.Redis(connection_pool=pool)
	return r