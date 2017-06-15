#!/usr/bin/env python
# -*- coding:utf-8 -*-


from monitor import models


class ClientHandler(object):

	def __init__(self,client_id):

		self.client_id = client_id
		self.client_monitor_config = {
			'service':{},
		}
		self.host_triggers = []


	def fetch_config(self):
		templates = []
		client_obj = models.Host.objects.get(id=self.client_id)
		host_templates = client_obj.templates.select_related()
		templates.extend(host_templates)
		for hostgroup in client_obj.hostgroups.select_related():
			templates.extend(hostgroup.templates.select_related())

		for template in templates:
			for service in template.services.select_related():
				self.client_monitor_config['services'][service.sname] = [service.plugin_name,service.interval]

		return self.client_monitor_config

	def fetch_triggers(self):

		client_obj = models.Host.objects.get(id=self.client_id)
		host_templates = client_obj.templates.select_related()
		for template in host_templates:
			self.host_triggers.extend(template.triggers.select_related())
		for group in client_obj.hostgroups.select_related():
			for template in group.templates.select_related():
				self.host_triggers.extend(template.triggers.select_related())
		return self.host_triggers

