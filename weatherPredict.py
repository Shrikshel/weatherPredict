# -*- coding: utf-8 -*-

import os
import datetime
from pandas import Series, DataFrame
import pandas as pd
import numpy as np
from scipy.spatial import distance

def getDataFromCSV():
	df = pd.read_csv("weatherData/weather20042013.csv")
	df['date'] = pd.to_datetime(df['date'])
	return df

def getFitFrame(fitDF, todaysDate, frameSize): #frameSize used
	lowWeek = todaysDate - datetime.timedelta(days=frameSize)
	highWeek = todaysDate + datetime.timedelta(days=frameSize)
	return fitDF[(fitDF["date"] >= lowWeek) & (fitDF["date"] <= highWeek)]

def getTestFrame(fitDF, todaysDate, frameSize): #frameSize used
	yesterdayDate = todaysDate - datetime.timedelta(days=1)
	frameStartDate = yesterdayDate - datetime.timedelta(days=6)
	return fitDF[(fitDF["date"] >= frameStartDate) & (fitDF["date"] <= yesterdayDate)]

def getWindows(dataFrame, frameSize): #frameSize used
	windows = {}
	startAdd = 0
	endAdd = frameSize
	while endAdd <= (frameSize*2)+1:
		windows[startAdd] = dataFrame[startAdd:endAdd]
		startAdd = startAdd + 1
		endAdd = endAdd + 1
	return windows

def getEuclideans(windows, testFrame):
	euclideans = {}
	testMaxTemp = Series(testFrame["maxTemp"].astype(float)).round(2).tolist()
	testMinTemp = Series(testFrame["minTemp"].astype(float)).round(2).tolist()
	testRainfall = Series(testFrame["rainfall"].fillna(0).astype(float)).round(2).tolist()
	testMorningHumidity = Series(testFrame["morningHumidity"].fillna(0).astype(float)).round(2).tolist()
	testEveningHumidity = Series(testFrame["eveningHumidity"].fillna(0).astype(float)).round(2).tolist()
	for i in windows:
		iMaxTemp = Series(windows[i]["maxTemp"].astype(float)).round(2).tolist()
		iMinTemp = Series(windows[i]["minTemp"].astype(float)).round(2).tolist()
		iRainfall = Series(windows[i]["rainfall"].fillna(0).astype(float)).round(2).tolist()
		iMorningHumidity = Series(windows[i]["morningHumidity"].fillna(0).astype(float)).round(2).tolist()
		iEveningHumidity = Series(windows[i]["eveningHumidity"].fillna(0).astype(float)).round(2).tolist()
		maxTempEuclid = distance.euclidean(testMaxTemp, iMaxTemp)
		minTempEuclid = distance.euclidean(testMinTemp, iMinTemp)
		rainfallEuclid = distance.euclidean(testRainfall, iRainfall)
		morningHumidityEuclid = distance.euclidean(testMorningHumidity, iMorningHumidity)
		eveningHumidityEuclid = distance.euclidean(testEveningHumidity, iEveningHumidity)
		euclideans[i] = maxTempEuclid + minTempEuclid + rainfallEuclid + morningHumidityEuclid + eveningHumidityEuclid #[maxTempEuclid, minTempEuclid, rainfallEuclid] might want to look for other ways of doing this
	return euclideans

def findCD(windows, euclideans):
	sortedEuclids = sorted(euclideans.items(), key=lambda x: x[1])
	euclidsList = sortedEuclids[:5]
	cdWindowList = [windows[i[0]] for i in euclidsList]
	print "CD Window List"
	print cdWindowList
	return cdWindowList

def calcMeanByReverse(data):
	temp = data.fillna(0).astype(float).round(2)
	temp = temp.reindex(index=temp.index[::-1])
	
	return np.diff(temp).mean()

def calcPredictedVariations(cdWindow, testFrame):
	varCDMaxTemp = calcMeanByReverse(cdWindow["maxTemp"])
	varCDMinTemp = calcMeanByReverse(cdWindow["minTemp"])
	varCDRainfall = calcMeanByReverse(cdWindow["rainfall"])
	varCDMorningHumidity = calcMeanByReverse(cdWindow["morningHumidity"])
	varCDEveningHumidity = calcMeanByReverse(cdWindow["eveningHumidity"])
	varPDMaxTemp = calcMeanByReverse(testFrame["maxTemp"])
	varPDMinTemp = calcMeanByReverse(testFrame["minTemp"])
	varPDRainfall = calcMeanByReverse(testFrame["rainfall"])
	varPDMorningHumidity = calcMeanByReverse(testFrame["morningHumidity"])
	varPDEveningHumidity = calcMeanByReverse(testFrame["eveningHumidity"])
	maxTempMean = (varCDMaxTemp + varPDMaxTemp) / 2
	minTempMean = (varCDMinTemp + varPDMinTemp) / 2
	rainfallMean = (varCDRainfall + varPDRainfall) / 2
	morningHumidityMean = (varCDMorningHumidity + varPDEveningHumidity) / 2
	eveningHumidityMean = (varCDMorningHumidity + varPDEveningHumidity) / 2
	return {"maxTempDelta" : maxTempMean, "minTempDelta" : minTempMean, "rainfallDelta" : rainfallMean, "morningHumidityDelta" : morningHumidityMean, "eveningHumidityDelta" : eveningHumidityMean}

def getPredictedWeather(testFrame, deltas):
	yesterdayWeather = testFrame[-1:]
	maxTemp = float(yesterdayWeather["maxTemp"]) + deltas["maxTempDelta"]
	minTemp = float(yesterdayWeather["minTemp"]) + deltas["minTempDelta"]
	rainfall = float(yesterdayWeather["rainfall"]) + deltas["rainfallDelta"]
	morningHumidity = float(yesterdayWeather["morningHumidity"]) + deltas["morningHumidityDelta"]
	eveningHumidity = float(yesterdayWeather["eveningHumidity"]) + deltas["eveningHumidityDelta"]
	return {"maxTemp":maxTemp, "minTemp":minTemp, "rainfall":rainfall, "morningHumidity":morningHumidity, "eveningHumidity":eveningHumidity}

if __name__ == "__main__":
	fitDF = getDataFromCSV()
	todaysDate = datetime.date(2012,9,15)
	dataFrame = getFitFrame(7, fitDF, todaysDate)
	testFrame = getTestFrame(7, fitDF, todaysDate)
	windows = getWindows(dataFrame)
	euclideans = getEuclideans(windows, testFrame)
	cdWindow = findCD(windows, euclideans)
	deltas = calcPredictedVariations(cdWindow, testFrame)
	predicted = getPredictedWeather(testFrame, deltas)
	print deltas
	print predicted, fitDF[fitDF["date"] == todaysDate]
