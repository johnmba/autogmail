
import random
import requests


class Mailgenerator:
    
    def __init__(self, url=None, headers=None) -> None:
        if url is None and headers is None:
            self.url = "https://temp-gmail.p.rapidapi.com/get"
            self.headers = {
            'x-rapidapi-host': "temp-gmail.p.rapidapi.com",
            'x-rapidapi-key': "YOUR PRIVATE KEY"
            }
        else:
            self.url = url
            self.headers = headers
    
    def generator(self):
        """
        generate email registeration data from an api
        """
        
        ID = random(1, 1000)
        querystring = {"id":ID,"type":"alias"}
        
        # send a request to the API
        response = requests.request(
            "GET", self.url, headers=self.headers, params=querystring
        )
        
        # convert the response to JSON format 
        json_response = response.json()
        # get gmail address
        gmail = json_response['items']['username']
        # get gmail password
        password = json_response['items']['key']

        print('Gmail address: %s' % str(gmail))
        print('Password: %s' % str(password))

    def checkmail(self, gmail, password):
        """
        check if the user name now exists in gmail server
        """

        # access the API
        url = "https://temp-gmail.p.rapidapi.com/check"
        querystring = {"username":gmail,"key":password}
        headers = {
            'x-rapidapi-host': "temp-gmail.p.rapidapi.com",
            'x-rapidapi-key': "YOUR PRIVATE KEY"
            }
        
        # send a request to the API
        response = requests.request("GET", url, headers=headers, params=querystring)
        
        # convert the response to JSON format 
        json_response = response.json()
        
        # print the message from the API
        print('API message: %s' % str(json_response['msg']))

        # check whether the inbox is empty or not
        if json_response['items'] == []:
            print("inbox is empty")

        # if the inbox is not empty, print the details of the newest mail
        else:
            message_id = json_response['items'][0]['mid']
            print('Message ID: %s' % str(message_id))
            print('From: %s' % str(json_response['items'][0]['textFrom']))
            print('Date: %s' % str(json_response['items'][0]['textDate']))
            print('Subject: %s' % str(json_response['items'][0]['textSubject']))

