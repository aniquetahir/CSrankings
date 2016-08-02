from io import open
import urllib
from urllib2 import Request, urlopen
from bs4 import BeautifulSoup
import os
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import time

driver = webdriver.Firefox(firefox_binary=
                           FirefoxBinary('/Applications/Firefox.app/Contents/MacOS/firefox'))

driver.get("http://maps.google.com")


def getAddress(affiliation):
    try:
        driver.refresh()
        time.sleep(3)
        searchbox = driver.find_element_by_id('searchboxinput')
        searchbutton = driver.find_element_by_class_name("searchbox-searchbutton")

        searchbox.clear()
        searchbox.send_keys(affiliation)
        searchbutton.click()

        time.sleep(3)

        searchurl = driver.current_url
        info_components = searchurl.split('@', 1)[1].split(',')
        latitude = info_components[0]
        longitude = info_components[1]

        affiliation_location_file.write(u"%s,%s,%s\n" % (affiliation, latitude, longitude))
    except Exception as e:
        print 'nothing found for %s' % affiliation
        print e.message


# Open the Faculty/Affiliations file
faculty_affiliations_file = open('../faculty-affiliations.csv', 'r')


# Get distinct affiliations
affiliations = []
for line in faculty_affiliations_file.readlines()[1:]:
    institution = line.split(',', 1)[-1].strip()
    affiliations.append(institution)

faculty_affiliations_file.close()

# uniq
affiliations = list(set(affiliations))

#Remove the file if it exists to start fresh
if os.path.exists('../affiliation-location.csv'):
    os.remove('../affiliation-location.csv')

affiliation_location_file = open('../affiliation-location.csv', 'a')

affiliation_location_file.write(u"name,latitude,longitude\n")
# Get the location of the affiliations
for affiliation in affiliations:
    # Create here API call
    getAddress(affiliation)


affiliation_location_file.flush()
affiliation_location_file.close()

