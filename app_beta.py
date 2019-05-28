import requests as rq
import sys
import json


class Response:
    def __init__(self,url):
        self.response = rq.get(url)
        self.data = json.loads(self.response.content)
        self.self_url = self.data['links']['self']
        self.last_url = self.data['links']['last']

    def compute(self, arguments):
        if arguments[1] == 'mean':
            value = self.get_mean(arguments)
        elif arguments[1] == 'pass_percent':
            value = self.get_percent_pass(arguments)
        elif arguments[1] == 'pass_max':
            value = self.get_max_pass(arguments)
        elif arguments[1] == 'regress':
            value = self.get_regress(arguments)
        elif arguments[1] == 'compare':
            value = self.get_compare(arguments)
        else:
            print('Command not found, try something else or I dunno man, maybe we\'re just not meant for each other')
            quit()
        return value

    def get_mean(self, arguments):
        data_left = True
        sum = 0
        years = []
        while data_left:
            self.response = rq.get(self.self_url)
            self.data = json.loads(self.response.content)
            for i in self.data['data']:
                if i['attributes']['col1'].lower() == arguments[2].lower() and i['attributes']['col2'] == 'przystąpiło' \
                        and i['attributes']['col4'] <= int(arguments[3]):
                    sum = sum + i['attributes']['col5']
                    years.append(i['attributes']['col4'])
            if self.self_url == self.last_url:
                data_left = False
            else:
                self.self_url = self.data['links']['next']
        years = list(set(years))
        return sum / len(years)

    def get_percent_pass(self, arguments):
        data_left = True
        passed = {}
        entered = {}
        percent = {}
        while data_left:
            self.response = rq.get(self.self_url)
            self.data = json.loads(self.response.content)
            for i in self.data['data']:
                if i['attributes']['col2'] == 'przystąpiło' and i['attributes']['col1'].lower() == arguments[2].lower():
                    entered[str(int(i['attributes']['col4']))] = i['attributes']['col5'] + entered.get(str(int(i['attributes']['col4'])),0)
                elif i['attributes']['col2'] == 'zdało' and i['attributes']['col1'].lower() == arguments[2].lower():
                    passed[str(int(i['attributes']['col4']))] = i['attributes']['col5'] + passed.get(str(int(i['attributes']['col4'])),0)
            if self.self_url == self.last_url:
                data_left = False
            else:
                self.self_url = self.data['links']['next']
        for key, _ in entered.items():
            percent[key] = str(round((passed[key]/entered[key]) * 100)) + '%'
        return percent

    def get_max_pass(self, arguments):
        data_left = True
        percent = {}
        passed = {}
        entered = {}
        while data_left:
            self.response = rq.get(self.self_url)
            self.data = json.loads(self.response.content)
            for i in self.data['data']:
                if i['attributes']['col4'] == int(arguments[2]):
                    if i['attributes']['col2'] == 'przystąpiło':
                        passed[i['attributes']['col1'].lower()] = passed.get(i['attributes']['col1'].lower(), 0) + i['attributes']['col5']
                    elif i['attributes']['col2'] == 'zdało':
                        entered[i['attributes']['col1'].lower()] = entered.get(i['attributes']['col1'].lower(), 0) + i['attributes']['col5']
            if self.self_url == self.last_url:
                data_left = False
            else:
                self.self_url = self.data['links']['next']
        for key, _ in entered.items():
            percent[key] = passed[key]/entered[key]
        return max(percent, key=percent.get)

    def get_regress(self, arguments):
        return

    def get_compare(self, arguments):
        return


if __name__ == '__main__':
    query = Response("https://api.dane.gov.pl/resources/17363/data")
    print(query.compute(sys.argv))
