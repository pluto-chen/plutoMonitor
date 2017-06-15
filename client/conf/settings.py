#!/usr/bin/env python
# -*- coding:utf-8 -*-


configs = {
    'HostID':1,
    'MonitorServer':'10.22.197.104',
    'Port':9000,
    'url_info':{
        'get_config':['monitor_api/client/get_config','get'],
        'report_data':['monitor_api/client/report_data','post']
    },
    'Request_timeout':30,
    'Config_update_interval':300
}

