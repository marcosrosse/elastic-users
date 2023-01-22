from src.open_json import *
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

  json_obj = openJSON("src/example.json")

  for indice in json_obj["users"]:
  
    print("Trying to create role: ", indice["rolename"])
    rolepayload = json.dumps({
          "cluster": ["all"],
          "indices": [
            {
              "names": [ "*" ],
              "privileges": indice["userroleprivileges"]
              }
          ]
        }, indent=4)

    print(rolepayload)
    try:
      r = requests.post(base_url + elasticsearch_role_api + indice["rolename"], data = rolepayload, headers = {"Content-Type": "application/json"}, auth = (elasticsearch_username, elasticsearch_password))
      print(r.text, '\n')
    except:
      print("An error occurred when trying to create the role", indice["rolename"], "on Elasticsearch")


    print("Trying to create user: ", indice["username"])
    userpayload = json.dumps({
        "password" : indice["password"],
        "enabled": True,
        "roles" : indice["roles"],
        "full_name" : indice["fullname"],
        "email" : indice["email"],
        "metadata" : {
          "intelligence" : 7
        }
      }, indent=4)

    print(userpayload)

    try:
      r = requests.post(base_url + elasticsearch_user_api + indice["username"], userpayload, headers = {"Content-Type": "application/json"}, auth= (elasticsearch_username, elasticsearch_password))
      print (r.text, '\n')
    except:
      print("An error occurred when trying to create the user", indice["username"], "on Elasticsearch")


def deleteElasticUser():

  json_obj = openJSON("src/example.json")

  for indice in json_obj["users"]:
      try:
        r = requests.delete(base_url+elasticsearch_role_api+indice["userrole"], headers = {"Content-Type": "application/json"}, auth = (elasticsearch_username, elasticsearch_password))
        print(r.text, '\n')
      except:
        print("An error occurred when trying to delete the role", indice["username"], "on Elasticsearch")

      try:
        r = requests.delete(base_url + elasticsearch_user_api + indice["username"], headers = {"Content-Type": "application/json"}, auth = (elasticsearch_username, elasticsearch_password))
        print (r.text, '\n')
      except:
        print("An error occurred when trying to delete the user", indice["username"], "on Elasticsearch")