import csv

def openCSVFile(file_name):
  reader = csv.DictReader(open(file_name))
  return reader