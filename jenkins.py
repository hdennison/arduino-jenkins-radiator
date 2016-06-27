import json
import sys
import urllib2
import time
import serial
# Configurations
ping_server = 30
jenkinsUrl = "https://ci.jenkins.io/"
jenkins_jobs=["Plugins/job/git-plugin/job/3.0.0-beta", "Core/job/pom"]
ser = serial.Serial('/dev/cu.usbmodem1421', 9600)
# Arduino Configuration
SUCCESS = 'b'
FAILURE = 'r'
BUILDING = 'a'
UNSTABLE = 'y'
time.sleep(5)
def get_status(jobName):
    try:
        jenkinsStream   = urllib2.urlopen( jenkinsUrl + "job/" + jobName + "/lastBuild/api/json" )
    except urllib2.HTTPError, e:
        print "URL Error: " + str(e.code)
        print "      (job name [" + jobName + "] probably wrong)"
        sys.exit(2)
    try:
        buildStatusJson = json.load( jenkinsStream )
    except:
        print "Failed to parse json"
        sys.exit(3)
    
    
    return jobName,buildStatusJson["timestamp"], buildStatusJson["result"],

while(1):
    for job in jenkins_jobs:
        status = get_status(job)
        print status[0], status[2]
        if status[2] == "UNSTABLE":
            ser.write(UNSTABLE)
        elif status[2] == "SUCCESS":
            ser.write(SUCCESS)
        elif status[2] == "FAILURE":
            ser.write(FAILURE)
        elif status[2] == None:
            ser.write(BUILDING)
        time.sleep(ping_server)