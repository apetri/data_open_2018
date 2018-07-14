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
events_cols = 'event_date,city,state'.split(",")

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
	return df.sort_values("date")

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

#Join in airport info, weather, events
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

	#Sort events
	events = events.sort_values(["event_date","city","state"])

	#Attach closest event to origin
	ren = { c:"origin_"+c for c in events_cols }
	em = events.rename(ren,axis=1)
	traffic = pd.merge_asof(traffic.sort_values(["date","origin_city","origin_state"]),em[list(ren.values())],left_on="date",right_on="origin_event_date",by=["origin_city","origin_state"],direction="nearest")
	traffic["origin_closest_event_days"] = (traffic.origin_event_date - traffic.date).dt.days

	#Attach closest event to destination
	ren = { c:"destination_"+c for c in events_cols }
	em = events.rename(ren,axis=1)
	traffic = pd.merge_asof(traffic.sort_values(["date","destination_city","destination_state"]),em[list(ren.values())],left_on="date",right_on="destination_event_date",by=["destination_city","destination_state"],direction="nearest")
	traffic["destination_closest_event_days"] = (traffic.destination_event_date - traffic.date).dt.days

	#Done
	return traffic

#Join in flight density
def joinFlightDensity(traffic,fd):

	#Attach origin info
	fd_origin = fd.rename({"airport_id":"origin_airport","total":"origin_total_flights"},axis=1)
	traffic = pd.merge(traffic,fd_origin[["date","origin_airport","origin_total_flights"]],on=["date","origin_airport"])

	#Attach destination info
	fd_destination = fd.rename({"airport_id":"destination_airport","total":"destination_total_flights"},axis=1)
	traffic = pd.merge(traffic,fd_destination[["date","destination_airport","destination_total_flights"]],on=["date","destination_airport"])

	return traffic


######################
#Qualitative analysis#
######################

#Flight density
def flightDensity(trf):
	
	leave = trf.rename({"origin_airport":"airport_id"},axis=1).groupby(["date","airport_id"]).airline_id.count()
	leave.name = "depart"

	arrive = trf.rename({"destination_airport":"airport_id"},axis=1).groupby(["date","airport_id"]).airline_id.count()
	arrive.name = "arrive"

	leave_arrive = pd.merge(leave.reset_index(),arrive.reset_index(),on=["date","airport_id"])
	leave_arrive["total"] = leave_arrive.depart + leave_arrive.arrive

	return leave_arrive



