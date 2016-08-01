from io import open
import urllib
from urllib2 import Request, urlopen
from bs4 import BeautifulSoup

# Open the Faculty/Affiliations file
faculty_affiliations_file = open('../faculty-affiliations.csv', 'r')

# Open the HERE API configuration
api_configuration_file = open('.private', 'r')

here_config = {}
for line in api_configuration_file.readlines():
    if '=' in line:
        config_keyvalue = line.split('=')
        if len(config_keyvalue) >= 2:
            here_config[config_keyvalue[0].strip()] = config_keyvalue[1].strip()

api_configuration_file.close()

here_geocode_url = 'https://geocoder.cit.api.here.com/6.2/geocode.xml?app_id={APP_ID}&app_code={APP_CODE}&gen=9&searchtext='
here_geocode_url = here_geocode_url.replace('{APP_ID}', here_config['APP_ID'])
here_geocode_url = here_geocode_url.replace('{APP_CODE}', here_config['APP_CODE'])

# Get distinct affiliations
affiliations = []
for line in faculty_affiliations_file.readlines()[1:]:
    institution = line.split(',')[-1].strip()
    affiliations.append(institution)

faculty_affiliations_file.close()

# uniq
affiliations = list(set(affiliations))

affiliation_location_file = open('../affiliation-location.csv', 'a')

# Get the location of the affiliations
for affiliation in affiliations:
    # Create here API call
    affiliation_url = here_geocode_url + urllib.quote_plus(affiliation)
    request = Request(affiliation_url)
    request.add_header('Content-Type', 'text/plain')
    xml_info = urlopen(request).read()
    soup = BeautifulSoup(xml_info, 'xml')

    try:
        displayposition = soup.find('Location').find('DisplayPosition')
        latitude = displayposition.find("Latitude").text
        longitude = displayposition.find("Longitude").text
    except:
        print '%s has no coordinates available' % affiliation

affiliation_location_file.close()






