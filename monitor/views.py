from django.shortcuts import render,HttpResponse
from monitor import models
from django.views.decorators.csrf import csrf_exempt
from monitor.serializer import ClientHandler
from Automation34 import settings
from monitor.backends import redis_conn
from monitor.backends import data_optimization
from monitor.backends import data_processing
import json

# Create your views here.

Redis_obj = redis_conn.redis_conn(settings)

def get_config(request,client_id):

	client = ClientHandler(client_id)
	client_config = client.fetch_config()
	if client_config['services']:
		return HttpResponse(json.dumps(client_config))

def dashboard(request):

	return HttpResponse('client dashboard page')

@csrf_exempt
def report_data(request):

	if request.method == 'POST':
		host_id = request.POST.get('client_id')
		service_name = request.POST.get('service_name')
		data = json.loads(request.POST.get('data'))
		data_handle_obj = data_optimization.DataHandler(host_id,service_name,data,Redis_obj)

		client = ClientHandler(host_id)
		client_triggers = client.fetch_triggers()

		trigger_handler = data_processing.DataProcesser(Redis_obj)
		for trigger in client_triggers:
			trigger_handler.data_calculating(host_id,service_name,trigger)

	return HttpResponse(json.dumps('got it'))