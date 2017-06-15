#!/usr/bin/env python
# -*- coding:utf-8 -*-

from core import client

class Argv_Handler(object):

    def __init__(self,argv):
        self.argv_list = argv
        if len(self.argv_list) !=2:
            self.msg_helper()
        if hasattr(self,self.argv_list[1]):
            func = getattr(self,self.argv_list[1])
            func()
        else:
            print('Wrong Arguments')
            self.msg_helper()

    def msg_helper(self):
        help_info = '''
        start   start monitor
        stop    stop monitor
        '''
        exit(help_info)


    def start(self):
        client_handler = client.Client_Manager()
        client_handler.run()


    def stop(self):
        print('stop monitor')