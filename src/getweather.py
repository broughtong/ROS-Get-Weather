#!/usr/bin/env python
import time
import requests
import threading
import unicodedata
import rospy
from ros_get_weather.msg import Weather
from bs4 import BeautifulSoup

exit = False
exitLock = threading.Lock()
msg = Weather 
msgLock = threading.Lock()

class lookupThread(threading.Thread):
    def __init__(self, pollInterval, location):
        threading.Thread.__init__(self)

        self.pollInterval = pollInterval
        self.currentInterval = 0
        self.location = location

    def run(self):
        global msg, msgLock, exit, exitLock

        while not rospy.is_shutdown():
            while self.weather(self.location + " weather") == False:
                time.sleep(3)
            
            while self.currentInterval < self.pollInterval:
                time.sleep(1)
                self.currentInterval += 1
                exitLock.acquire()
                if exit == True:
                    exitLock.release()
                    return
                exitLock.release()
            self.currentInterval = 0

    def weather(self, location):
        global msg, msgLock, exit, exitLock

        rospy.loginfo("Making web request")

        try:
            url = "https://www.google.com/search?channel=fs&client=ubuntu&q=" + location.replace(" ", "+")
            headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0"}
            res = requests.get(url, headers=headers)
        except:
            rospy.logwarn("Failed to get weather")
            return False

        rospy.loginfo("Web request received")

        try:
            soup = BeautifulSoup(res.text, 'html.parser')

            msgLock.acquire()
            msg = Weather()
            msg.location = self.parse(soup.select("#wob_loc")[0].getText())
            msg.forecastTime = self.parse(soup.select('#wob_dts')[0].getText())
            msg.description = self.parse(soup.select('#wob_dc')[0].getText())
            msg.celsius = int(soup.select('#wob_tm')[0].getText())
            msg.precipitation = self.parse(soup.select('#wob_pp')[0].getText())
            msg.humidity = self.parse(soup.select('#wob_hm')[0].getText())
            msg.wind = self.parse(soup.select('#wob_ws')[0].getText())
            msgLock.release()

            rospy.logdebug("Parsed")

        except:
            rospy.logwarn("Unable to parse web data")
            return False
        return True

    def parse(self, string):
        return unicodedata.normalize('NFKD', string).encode('ascii', 'ignore').decode()

if __name__ == '__main__':

    rospy.init_node("weather")

    pollInterval = int(rospy.get_param("~pollInterval", "900"))
    publishRate = float(rospy.get_param("~publishRate", "0.2"))
    location = rospy.get_param("~location", "prague")

    pub = rospy.Publisher("weather", Weather, queue_size=10)

    thread = lookupThread(pollInterval, location)
    thread.start()

    r = rospy.Rate(publishRate)
    while not rospy.is_shutdown():
        msgLock.acquire()
        m = msg
        msgLock.release()
        pub.publish(m)
        r.sleep()
    
    exitLock.acquire()
    exit = True
    exitLock.release()

