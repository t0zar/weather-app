#!/usr/bin/env python
import re
import urllib.request
from time import sleep
from bs4 import BeautifulSoup

__author__ = 'ozanenginoglu'


class Weather:

    def __init__(self):
        '''
        Containers are used to store all the information.
        They are first retrieved from the web site and then
        appended into them in each function defined in Weather
        Class.
        '''
        self.cityInfo = []  # Height, longtitude,latitude, sunset and sunrise
        self.currentWeather = []  # Temp, RH, Wind, Pressure, Line Sight, Event
        self.minTemperature = []  # Minimum temperatures
        self.maxTemperature = []  # Maximum temperatures
        self.minHumidity = []  # Minimum humidities
        self.maxHumidity = []  # Maximumm humidities
        self.events = []  # Events
        self.eventURL = []  # Event URLs
        self.windSpeed = []  # Wind speeds
        print('Weather information is being pulled from the web server...')

    def get_source(self, city):
        '''
        Retrieve weather data from mgm.gov.tr web site
        and transform it into a soup file which
        beautifulsoup can work on.
        '''
        # Base page URL
        url = 'http://www.mgm.gov.tr/tahmin/il-ve-ilceler.aspx?m='
        url += str(city)  # City name
        while True:
            # Get the web page source code. If it fails wait 1 second
            # self.assertNotIn(member, container)d try again until it's done.
            try:
                # Load the web page and save it to the variable
                source_code = urllib.request.urlopen(url)
                break
            except:
                sleep(1)  # Wait 1 second
        self.soup = BeautifulSoup(source_code)  # source code to Beautifulsoup
        return self.soup

    def get_cityInfo(self):
        '''
        Current weather information of the city.
        '''
        for i in self.soup.findAll('div', {'id': 'divMerkez'}):
            text = i.text.split()  # Split the whole text into parts
            city_height = text[1] + ' ' + text[2]
            city_longtitude = text[4] + text[5] + ' ' + text[6]
            city_latitude = text[8] + text[9] + ' ' + text[10]
            city_sunset = text[13]
            city_sunrise = text[16]
            self.cityInfo.append(city_height)
            self.cityInfo.append(city_longtitude)
            self.cityInfo.append(city_latitude)
            self.cityInfo.append(city_sunset)
            self.cityInfo.append(city_sunrise)

    def get_currentWeather(self):
        '''
        Retrieves today's weather conditions such as
        temperature, humidity, pressure, wind speed
        and line of sight.
        '''
        for i in self.soup.findAll('td'):
            for j in i.findAll('em'):
                self.currentWeather.append(j.text)
        for i in self.soup.findAll('table', {'class': 'tbl_sond'}):
            for j in i.findAll('td', {'rowspan': '2'}):
                self.currentWeather.append(j['title'])

    def get_minTemperature(self):
        '''
        Minimum temperature data of the following
        five days.
        '''
        for i in range(1, 6):
            for j in self.soup.findAll('td', {'id': 'cp_sayfa_thmMin'
                                              + str(i)}):
                self.minTemperature.append(j.text)

    def get_maxTemperature(self):
        '''
        Maximum temperature data of the following
        five days.
        '''

        for i in range(1, 6):
            for j in self.soup.findAll('td', {'id': 'cp_sayfa_thmMax'
                                              + str(i)}):
                self.maxTemperature.append(j.text)

    def get_minHumidity(self):
        '''
        Minimum humidity data of the following
        five days.
        '''
        for i in range(1, 6):
            for j in self.soup.findAll('td', {'id': 'cp_sayfa_thmNemMin'
                                              + str(i)}):
                self.minHumidity.append(j.text)

    def get_maxHumidity(self):
        '''
        Maximum humidity data of the following
        five days.
        '''
        for i in range(1, 6):
            for j in self.soup.findAll('td', {'id': 'cp_sayfa_thmNemMax'
                                              + str(i)}):
                self.maxHumidity.append(j.text)

    def get_events(self):
        '''
        Weather events of the following five
        days. Such as "cloudy, sunny etc."
        '''
        for i in range(1, 6):
            for j in self.soup.findAll('img', {'id': 'cp_sayfa_imgHadise'
                                               + str(i)}):
                self.events.append(j['alt'])

    def get_windSpeed(self):
        '''
        Wind speed of the following five days.
        '''
        for i in range(1, 6):
            for j in self.soup.findAll('td', {'id': 'cp_sayfa_thmRuzgarHiz'
                                              + str(i)}):
                self.windSpeed.append(j.text)

    def get_eventURL(self):
        link = self.soup.find('td', {'rowspan': '2'})
        re_search = re.findall(r'\/FILES.*png', str(link))
        re_result = 'http://www.mgm.gov.tr' + str(re_search[0])
        re_result2 = re.findall(r'-?..?\.png', str(link))
        self.eventURL.append(re_result)
        self.eventURL.append(re_result2[0])

    def weather_output(self):
        '''
        Print out the containers
        '''
        # container_dictionary = dict(zip(container_names,self.container))
        print('City Info', end=' >> ')
        print(self.cityInfo)
        print('Current City Weather Info', end=' >> ')
        print(self.currentWeather)
        print('Minimum Temperatures', end=' >> ')
        print(self.minTemperature)
        print('Maximum Temperatures', end=' >> ')
        print(self.maxTemperature)
        print('Minimum Humiditys', end=' >> ')
        print(self.minHumidity)
        print('Maximum Humiditys', end=' >> ')
        print(self.maxHumidity)
        print('Events', end=' >> ')
        print(self.events)
        print('Wind Speeds', end=' >> ')
        print(self.windSpeed)
        print('Main Event', end=' >> ')
        print(self.eventURL)

mgm = Weather()
city_name = str(input('Şehir >> ')).upper()
mgm.get_source(city_name)
mgm.get_cityInfo()
mgm.get_currentWeather()
mgm.get_minTemperature()
mgm.get_maxTemperature()
mgm.get_minHumidity()
mgm.get_maxHumidity()
mgm.get_events()
mgm.get_windSpeed()
mgm.get_eventURL()

mgm.weather_output()
