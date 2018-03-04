import csv

def search(zipcode):
	with open('Zip_MedianValuePerSqft.csv', 'r') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			if row["RegionName"] == str(zipcode):
				print(row["RegionName"], row["2018-01"])


search(32304)