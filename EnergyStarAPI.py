#####
#
# Energy Star API
#
#####

import requests
import json
from base64 import b64encode

class Energy_Star_Test_Client(object):
	def __init__(self,username=None,password=None):
		if username == None or password == None:
			raise Exception("Username and Password required")
		self.domain = "https://portfoliomanager.energystar.gov/wstest"
		self.username = username
		self.password = password
		
	def create_account(self,account_file):
		if hasattr(account_file,"read"):
			resource = self.domain + '/account'
			account_info = account_file.read()
			headers = {}
			headers['Content-Type'] = 'application/xml'
			acct = str(account_info)
			print(acct)
			response = requests.post(resource,data=acct,headers=headers)
			print response.text
			if response.status_code != 200:
				return _raise_for_status(response)
			return response
	
	def get_account_info(self):
		resource = self.domain + "/account"

		response = requests.get(resource, auth=(self.username, self.password))
		if response.status_code != 200:
			return _raise_for_status(response)
		return response.text

	def get_meter_list(self, prop_id):
		resource = 'https://portfoliomanager.energystar.gov/wstest/property/%s/meter/list' % str(prop_id)
		response = requests.get(resource, headers=self.get_headers())

		if response.status_code != 200:
			return _raise_for_status(response)
		return response  

class Energy_Star_Client(object):
	def __init__(self,username=None,password=None):
		if username == None or password == None:
			raise Exception("Username and Password required")
		self.domain = "https://portfoliomanager.energystar.gov/ws"
		self.username = username
		self.password = password

	def get_account_info(self):
		resource = self.domain+"/account"
		response = requests.get(resource)
		

	def get_meter_list(self, prop_id):
		resource = self.domain + '/property/%s/meter/list' % str(prop_id)
		
		response = requests.get(resource, headers=self.get_headers())

		if response.status_code != 200:
			return _raise_for_status(response)
		return response
	def get_headers(self):
		headers = {}

		headers["Authorization"] = "Basic %s" % get_auth_token(username=self.username,password=self.password)

		return headers

def get_auth_token(auth = None, username = None, password = None, do_print = False):
    if auth is not None:
        result = b64encode(b"%s" % auth).decode("ascii")
    else:
        result = b64encode(b"{0}:{1}".format(username, password).decode("ascii"))

    if do_print is True:
        print "your auth_token: %s" % result

    return result

def _raise_for_status(response):
    '''
    Custom raise_for_status with more appropriate error message.
    '''
    http_error_msg = ""

    if 400 <= response.status_code < 500:
        http_error_msg = "{0} Client Error: {1}".format(response.status_code,
                                                        response.reason)

    elif 500 <= response.status_code < 600:
        http_error_msg = "{0} Server Error: {1}".format(response.status_code,
                                                        response.reason)

    if http_error_msg:
        try:
            more_info = response.json().get("message")
        except ValueError:
            more_info = None
        if more_info and more_info.lower() != response.reason.lower():
            http_error_msg += ".\n\t{0}".format(more_info)
        raise requests.exceptions.HTTPError(http_error_msg, response=response)