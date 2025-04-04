import requests

class Waha:
	def __init__(self):
		self.__api_url = 'http://waha:3000'
	
	def send_menssage(self,chat_id,message):
		url = f'{self.__api_url}/api/sendText'
		headers = { 
			'Content-Type':'application/json'
		}
		payload = {
			'session':'default',
			'chatId':chat_id,
			'text':message
		}
		requests.post(url = url, json = payload, headers = headers)