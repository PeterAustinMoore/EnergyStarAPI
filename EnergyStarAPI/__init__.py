#####
#
# Energy Star API
#
#####
import requests
import datetime
import xml.etree.ElementTree as Et


class EnergyStarTestClient(object):
    def __init__(self, username=None, password=None):
        if username is None or password is None:
            raise Exception("Username and Password required")
        self.domain = "https://portfoliomanager.energystar.gov/wstest"
        self.username = username
        self.password = password

    def create_account(self, account_file):
        if hasattr(account_file, "read"):
            resource = self.domain + '/account'
            account_info = account_file.read()
            headers = {'Content-Type': 'application/xml'}
            acct = str(account_info)
            response = requests.post(resource, data=acct, headers=headers)
            print(response.text)
            if response.status_code != 200:
                return _raise_for_status(response)
            return response.text

    def get_account_info(self):
        resource = self.domain + "/account"

        response = requests.get(resource, auth=(self.username, self.password))
        if response.status_code != 200:
            return _raise_for_status(response)
        return response.text

    def get_meter_list(self, prop_id):
        resource = 'https://portfoliomanager.energystar.gov/wstest/property/%s/meter/list' % str(prop_id)
        response = requests.get(resource, auth=(self.username, self.password))

        if response.status_code != 200:
            return _raise_for_status(response)
        return response


class EnergyStarClient(object):
    def __init__(self, username=None, password=None):
        if username is None or password is None:
            raise Exception("Username and Password required")
        self.domain = "https://portfoliomanager.energystar.gov/ws"
        self.username = username
        self.password = password

    def get_account_info(self):
        resource = self.domain + "/account"
        response = requests.get(resource, auth=(self.username, self.password))

        if response.status_code != 200:
            return _raise_for_status(response)
        return response.text

    def get_meter_list(self, prop_id):
        resource = self.domain + '/association/property/%s/meter' % str(prop_id)
        response = requests.get(resource, auth=(self.username, self.password))

        if response.status_code != 200:
            return _raise_for_status(response)

        data = response.text
        meters = dict()

        root = Et.fromstring(data)

        for e in root.iter("*"):
            if e.tag == "meterId":
                meter_type = self.get_meter_type(e.text)
                meters[e.text] = meter_type

        return meters

    def get_meter_type(self, meter_id):
        resource = self.domain + '/meter/%s' % str(meter_id)

        response = requests.get(resource, auth=(self.username, self.password))
        data = response.text

        root = Et.fromstring(data)
        meter_type = ''
        for e in root.iter("*"):
            if e.tag == "type":
                meter_type = e.text

        return meter_type

    def get_building_info(self, prop_id):
        resource = self.domain + '/building/%s' % str(prop_id)
        response = requests.get(resource, auth=(self.username, self.password))

        if response.status_code != 200:
            return _raise_for_status(response)
        return response.text

    def get_usage_data(self, meter_id, months_ago):
        # Get date in YYYY-MM-DD format from months ago
        date_format = '%Y-%m-%d'
        today = datetime.datetime.now()
        start_date = today - datetime.timedelta(days=months_ago * 30)
        start_date = datetime.datetime.strftime(start_date, date_format)
        resource = self.domain + '/meter/%s/consumptionData' % str(meter_id)

        usage = []

        url = resource + '?page=1&startDate=' + start_date
        page = 1
        while url:
            print(url)
            print("Getting data from page " + str(page))
            page += 1

            response = requests.get(url, auth=(self.username, self.password))

            if response.status_code != 200:
                print(response.status_code, response.reason)
                break
            # Set URL to none to stop loop if no more links
            url = None

            data = response.text
            root = Et.fromstring(data)
            for element in root.findall("meterConsumption"):
                month_data = dict()
                # Get the usage data
                month_data[element.find("endDate").text] = float(element.find("usage").text)
                usage.append(month_data)

            # Get the next URL
            for element in root.find("links"):
                for link in element.findall("link"):
                    if link.get("linkDescription") == "next page":
                        url = self.domain + link.get("link")
        # Return the usage for the time period
        return usage

    def get_cost_data(self, meter_id, months_ago):
        # Get date in YYYY-MM-DD format from months ago
        date_format = '%Y-%m-%d'
        today = datetime.datetime.now()
        start_date = today - datetime.timedelta(days=months_ago * 30)
        start_date = datetime.datetime.strftime(start_date, date_format)
        resource = self.domain + '/meter/%s/consumptionData' % str(meter_id)

        cost = []

        url = resource + '?page=1&startDate=' + start_date
        page = 1
        while url:
            print(url)
            print("Getting data from page " + str(page))
            page += 1

            response = requests.get(url, auth=(self.username, self.password))

            if response.status_code != 200:
                print(response.status_code, response.reason)
                break
            # Set URL to none to stop loop if no more links
            url = None

            data = response.text
            root = Et.fromstring(data)
            for element in root.findall("meterConsumption"):
                month_data = dict()
                # Get the cost data
                month_data[element.find("endDate").text] = float(element.find("cost").text)
                # append to cost
                cost.append(month_data)

            # Get the next URL
            for element in root.find("links"):
                for link in element.findall("link"):
                    if link.get("linkDescription") == "next page":
                        url = self.domain + link.get("link")
        # Return the cost for the time period
        return cost

    def get_usage_and_cost(self, meter_id, months_ago):
        # Get date in YYYY-MM-DD format from months ago
        date_format = '%Y-%m-%d'
        today = datetime.datetime.now()
        start_date = today - datetime.timedelta(days=months_ago * 30)
        start_date = datetime.datetime.strftime(start_date, date_format)
        resource = self.domain + '/meter/%s/consumptionData' % str(meter_id)

        usage_and_cost = []

        url = resource + '?page=1&startDate=' + start_date

        while url:
            print(url)

            response = requests.get(url, auth=(self.username, self.password))

            if response.status_code != 200:
                print(response.status_code, response.reason)
                break
            # Set URL to none to stop loop if no more links
            url = None

            data = response.text
            root = Et.fromstring(data)
            for element in root.findall("meterConsumption"):
                month_data = dict()
                # Get the usage and cost data
                usage_cost = [float(element.find("usage").text), float(element.find("cost").text)]

                # match with the date
                month_data[element.find("endDate").text] = usage_cost

                # append to usage
                usage_and_cost.append(month_data)

            # Get the next URL
            for element in root.find("links"):
                for link in element.findall("link"):
                    if link.get("linkDescription") == "next page":
                        url = self.domain + link.get("link")
        # Return the cost for the time period
        return usage_and_cost


def _raise_for_status(response):
    """
    Custom raise_for_status with more appropriate error message.
    """
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
