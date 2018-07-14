import os
import gzip
import pandas as pd

#########################################
#Globals: columns needed to load, etc...#
#########################################

data_path = "data"

heads_path = os.path.join("data","heads")

def getColNames(fname):
	h = pd.read_csv(fname)
	return { c:n for n,c in enumerate(h.columns) }

airport_cols = 'city,state,latitude,longitude'.split(",")
traffic_cols = 'year,month,day,airline_id,origin_airport,destination_airport,distance,scheduled_departure,actual_departure,scheduled_arrival,actual_arrival,airline_delay,air_system_delay,security_delay,aircraft_delay'.split(",")
weather_cols = 'elevation,temperature,visibility,wind_direction,wind_direction,wind_speed,snow_depth'.split(",")

###########
#Load data#
###########

def loadTraffic(fname,nrows,names):

	#Names of columns to pull
	cnames = getColNames(os.path.join(heads_path,"traffic.csv"))
	coln =  [ cnames[c] for c in names ]
	coln.sort()

	#Read data
	with gzip.open(fname,"rb") as fp:
		df = pd.read_csv(fp,usecols=coln,nrows=nrows)

	#Attach dates, sum delays
	df["date"] = df.apply(lambda x:pd.Timestamp(year=x.year,month=x.month,day=x.day),axis=1)
	df["total_delay"] = df[['airline_delay','air_system_delay','security_delay','aircraft_delay']].sum(1)
	
	#Done
	return df

def loadWeather(fname):
	
	#Read
	df = pd.read_csv(fname,parse_dates=["datetime"])

	#Aggregate by day
	df = df.groupby(["airport_id",df.datetime.dt.round("D")])[['elevation','temperature','visibility','wind_direction','wind_speed','snow_depth']].mean()

	#Done
	return df.reset_index().rename({"datetime":"date"},axis=1)

def loadAirports(fname):
	df = pd.read_csv(fname,encoding="ISO-8859-1")
	return df

def loadEvents(fname):
	df = pd.read_csv(fname,parse_dates=["date"],encoding="ISO-8859-1")
	return df.rename({"date":"event_date"},axis=1)

#######
#Joins#
#######

def joinTraffic(traffic,airports,weather,events):

	#Attach origin info
	ren = { c:"origin_"+c for c in airport_cols }
	ren["airport_id"] = "origin_airport"
	air_source = airports.rename(ren,axis=1)
	traffic = pd.merge(traffic,air_source[list(ren.values())],on="origin_airport")

	#Attach destination info
	ren = { c:"destination_"+c for c in airport_cols }
	ren["airport_id"] = "destination_airport"
	air_dest = airports.rename(ren,axis=1)
	traffic = pd.merge(traffic,air_dest[list(ren.values())],on="destination_airport")

	#Attach origin weather
	ren = { c:"origin_"+c for c in weather_cols }
	ren["airport_id"] = "origin_airport"
	wm = weather.rename(ren,axis=1)
	traffic = pd.merge(traffic,wm[["date"]+list(ren.values())],on=["date","origin_airport"])

	#Attach destination weather
	ren = { c:"destination_"+c for c in weather_cols }
	ren["airport_id"] = "destination_airport"
	wm = weather.rename(ren,axis=1)
	traffic = pd.merge(traffic,wm[["date"]+list(ren.values())],on=["date","destination_airport"])

	#Attach closest event to origin

	#Attach closest event to destination


	#Done
	return traffic

