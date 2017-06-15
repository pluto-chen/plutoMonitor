#!/usr/bin/env python
# -*- coding:utf-8 -*-


from plugins.linux import linux_ram_info,linux_llzb_linksrv_info


def get_linux_ram_info():

	return linux_ram_info.monitor()


def get_llzb_linksrv_info():

	return linux_llzb_linksrv_info.monitor()
