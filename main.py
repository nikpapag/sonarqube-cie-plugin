import argparse
import json
import os
import sys
import time
from urllib.error import HTTPError

import requests
from requests.auth import HTTPBasicAuth
from junit_xml import TestSuite, TestCase


url=os.getenv('PLUGIN_SONAR_URL')
port=os.getenv('PLUGIN_SONAR_PORT')
token=os.getenv('PLUGIN_SONAR_TOKEN')
projectKey=os.getenv('PLUGIN_SONAR_PROJECT_KEY')
reportName=os.getenv('PLUGIN_SONAR_REPORT_NAME')

url=url+":"+str(port)+"/api/qualitygates/project_status"
payload = {'projectKey': projectKey}

try:
    response = requests.get(url, auth=HTTPBasicAuth(token,''), params=payload)
    print("Connecting to sonarqube instance " +url +"with response" + str(response))
    results = response.json()
    test_cases = []

    for test_result in results['projectStatus']['conditions']:
        test_case = TestCase(test_result['metricKey'],
                             "Violate if " + test_result['comparator'] + " " + str(test_result['errorThreshold']), 0,
                             str(test_result['actualValue']), str(test_result['errorThreshold']), "", "",
                             test_result['status'])
        test_cases.append(test_case)

    ts = TestSuite(reportName, test_cases)
    f = open("SonarqubeJunitResults.xml", "a")
    f.write(TestSuite.to_xml_string([ts]))
    f.close()


except HTTPError as http_err:
    print(f'HTTP error occurred: {http_err}')
except Exception as err:
    print(f'Other error occurred: {err}')


