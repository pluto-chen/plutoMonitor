#!/usr/bin/env python
# -*- coding:utf-8 -*-


import time
import json
import urllib.request,urllib.parse
import threading

from conf import settings
from plugins import plugin_api


class Client_Manager(object):

    def __init__(self):
        self.monitor_configs = {}


    def run(self):

        stop_flag = False

        last_get_config_time = 0

        while not stop_flag:

            if time.time() - last_get_config_time > settings.configs['Config_update_interval']:
                self.get_latest_config()
                print('获取到最新的monitor_config',self.monitor_configs)
                print('获取到的数据类型',type(self.monitor_configs))
            #print('当前monitor_config:',self.monitor_configs)

            for service_name,val in self.monitor_configs['service'].items():
                if len(val) == 2:
                    self.monitor_configs['service'][service_name].append(0)
                monitor_interval = val[1]
                last_invoke_time = val[2]
                if time.time() - last_invoke_time > monitor_interval:
                    self.monitor_configs['services'][service_name][2] = time.time()
                    t = threading.Thread(target=self.invoke_plugin,args=(service_name,val))
                else:
                    print('将在%s秒后重新获取数据'%(monitor_interval - time.time() + last_invoke_time))
            time.sleep(1)

    def invoke_plugin(self,service_name,val):
        plugin_name = val[0]
        if hasattr(plugin_api,plugin_name):
            func = getattr(plugin_api,plugin_name)
            monitor_data = func()
            report_data = {
                'client_id':settings.configs['HostID'],
                'service_name':service_name,
                'data':json.dumps(monitor_data)
            }

            request_url = settings.configs['url_info']['report_data'][0]
            request_method = settings.configs['url_info']['report_data'][1]
            self.url_request(request_url,request_method,params=report_data)
        else:
            print('No plugin:%s in api' )

    def get_latest_config(self):

        request_url = '%s/%s'%(settings.configs['url_info']['get_config'][0],settings.configs['HostID'])
        request_method = settings.configs['url_info']['get_config'][1]

        monitor_callback = self.url_request(request_url,request_method)
        monitor_config = json.loads(monitor_callback.decode())
        self.monitor_configs.update(monitor_config)


    def url_request(self,request_url,method,**kwargs):

        base_url = 'http://%s:%s/' %(settings.configs['MonitorServer'],settings.configs['Port'],)
        url = base_url + request_url

        if method in ('get','GET'):
            req = urllib.request.Request(url)
            req_data = urllib.request.urlopen(req,timeout=settings.configs['Request_timeout'])
            callback = req_data.read()
            return callback

        elif method in ('post','POST'):
            post_data = urllib.parse.urlencode(kwargs['params']).encode(encoding='UTF8')
            req = urllib.request.Request(url,data=post_data)
            req_data = urllib.request.urlopen(req,timeout=settings.configs['Request_timeout'])
            callback = req_data.read()
            return callback
