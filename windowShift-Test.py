# -*- coding: utf-8 -*-

import os
import datetime
import weatherPredict
import weatherHelper

def calcDays(yearsToSeeShift, monthsToSeeShift):
	"""Function to find 3 days in every months of given years. 3 days - 2nd day, 15th day, 27th day
	   This will create datelist that will be used to compare with past data to see dates in years to which they map with pearson's coefficient.
	"""
	daysToSeeShift = [2, 15, 27]
	selectedDays = []
	for year in yearsToSeeShift:
		for month in monthsToSeeShift:
			for day in daysToSeeShift:
				selectedDays.append(datetime.date(year, month, day))
	return selectedDays

if __name__ == "__main__":
	yearsToSeeShift = [2013] #reverse order is preferred
	monthsToSeeShift = [1]
	datesToMap = calcDays(yearsToSeeShift, monthsToSeeShift)
	for date in datesToMap:
		(predicted, fitDF) = weatherHelper.predictWeather(date, 7)
		print "\n\nPredictions"
		print predicted
		print fitDF[fitDF["date"] == date]
