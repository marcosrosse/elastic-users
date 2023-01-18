from open_csv_file import *
import os
from pickle import TRUE
import requests
import json

elasticsearch_url = os.environ['ELASTICSEARCH_URL']
elasticsearch_port = os.environ['ELASTICSEARCH_PORT']
elasticsearch_username = os.environ['ELASTICSEARCH_USERNAME']
elasticsearch_password = os.environ['ELASTICSEARCH_PASSWORD']
elasticsearch_role_api = "/_security/role/"
elasticsearch_user_api = "/_security/user/"

base_url = elasticsearch_url + ":" + elasticsearch_port

def createElasticUser():
  reader = openCSVFile("csv/users.csv")
  for row in reader:

    print("Trying to create role: ", row["roles"])
    payload = json.dumps({
          "cluster": ["all"],
          "indices": [
            {
              "names": [ "*" ],
              "privileges": ["read", "write"]
              }
          ]
        })
    
    r = requests.post(base_url + elasticsearch_role_api + row["roles"], data = payload, headers = {"Content-Type": "application/json"}, auth = (elasticsearch_username, elasticsearch_password))
    print(r.text, '\n')


    print("Trying to create user: ", row["username"])
    payload = json.dumps({
        "password" : row['password'],
        "enabled": True,
        "roles" : [ "kibana_user", "kibana_admin", "reporting_user", row['roles'] ],
        "full_name" : row['fullname'],
        "email" : "",
        "metadata" : {
          "intelligence" : 7
        }
      })
    r = requests.post(base_url + elasticsearch_user_api + row["username"], payload, headers = {"Content-Type": "application/json"}, auth= (elasticsearch_username, elasticsearch_password))
    print (r.text, '\n')


def deleteElasticUser():

  reader = openCSVFile("csv/delete-users.csv")
  for row in reader:

      print("Trying to delete role: ", row["roles"])
      r = requests.delete(base_url+elasticsearch_role_api+row["roles"], headers = {"Content-Type": "application/json"}, auth = (elasticsearch_username, elasticsearch_password))
      print(r.text, '\n')

      print("Trying to delete user: ", row["username"])
      r = requests.delete(base_url + elasticsearch_user_api + row["username"], headers = {"Content-Type": "application/json"}, auth = (elasticsearch_username, elasticsearch_password))
      print (r.text, '\n')