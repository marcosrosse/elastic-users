import json

def openJSON(file_name):

  with open(file_name) as file:
    data = json.load(file)
  return data