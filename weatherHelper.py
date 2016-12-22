# -*- coding: utf-8 -*-

import os
import datetime
import weatherPredict

def getYearsOfData(dataYears, todaysDate):
	todaysYear = todaysDate.year
	tempYearsList = [i for i in dataYears if i < todaysYear]
	tempYearsList.sort()
	return tempYearsList

def getDaysOfData(yearsFrameList, todaysDate):
	todaysMonth = todaysDate.month
	todaysDay = todaysDate.day
	daysFrameList = []
	for year in yearsFrameList:
		daysFrameList.append(datetime.date(int(year), int(todaysMonth), int(todaysDay)))
	return daysFrameList

def createFrameLists(dataYears, todaysDate):
	yearsFrameList = getYearsOfData(dataYears, todaysDate)
	daysFrameList = getDaysOfData(yearsFrameList, todaysDate)
	return yearsFrameList, daysFrameList

def flattenWindows(windows):
	returnWindow = {}
	counter = 0
	for i in windows:
		for j in i:
			returnWindow[counter] = i[j]
			counter = counter + 1
	return returnWindow

def reCalcPredicted(predicted, delta):
	maxTemp = float(predicted["maxTemp"]) + delta["maxTempDelta"]
	minTemp = float(predicted["minTemp"]) + delta["minTempDelta"]
	rainfall = float(predicted["rainfall"]) + delta["rainfallDelta"]
	morningHumidity = float(predicted["morningHumidity"]) + delta["morningHumidityDelta"]
	eveningHumidity = float(predicted["eveningHumidity"]) + delta["eveningHumidityDelta"]
	return {"maxTemp":maxTemp, "minTemp":minTemp, "rainfall":rainfall, "morningHumidity":morningHumidity, "eveningHumidity":eveningHumidity}

def predictWeather(todaysDate, frameSize):
	dataYears = [2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013]
	(yearsFrameList, daysFrameList) = createFrameLists(dataYears, todaysDate)
	fitDF = weatherPredict.getDataFromCSV()
	testFrame = weatherPredict.getTestFrame(fitDF, todaysDate, frameSize) #changed to fitFrame
	fitFrames = []
	for i in daysFrameList : fitFrames.append(weatherPredict.getFitFrame(fitDF, i, frameSize)) #changed to fitFrame
	windows = []
	for i in fitFrames : windows.append(weatherPredict.getWindows(i, frameSize)) #changed to fitFrame
	windows = flattenWindows(windows)
	euclideans = weatherPredict.getEuclideans(windows, testFrame)
	cdWindows = weatherPredict.findCD(windows, euclideans)
	deltas = [weatherPredict.calcPredictedVariations(i, testFrame) for i in cdWindows]
	predicted = weatherPredict.getPredictedWeather(testFrame, deltas[0])
	print "\n\nTest Frame"
	print testFrame
	for delta in deltas[1:]:
		predicted = reCalcPredicted(predicted, delta)
	return predicted, fitDF

if __name__ == "__main__":
	todaysDate = datetime.date(2013,6,2)
	frameSize = 7
	(predicted, fitDF) = predictWeather(todaysDate, frameSize)
	print "\n\nPredictions"
	print predicted
	print fitDF[fitDF["date"] == todaysDate]
