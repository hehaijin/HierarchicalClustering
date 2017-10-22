import csv
import re
import sys


def readData():
	data=[]
	with open('data.txt', newline='') as csvfile:
			for line in csvfile:
				sp=re.split(" +",line)
				p=[]
				for i in range(len(sp)-1):
					p.append(float(sp[i+1]))
				data.append(p)
	return data


data=readData()
			
with open('data.csv', "w") as csvfile:
		testwriter=csv.writer(csvfile)
		#testwriter.writerow(["id","class"])
		for row in data:
			testwriter.writerow(row)	
