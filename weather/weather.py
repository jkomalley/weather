import requests
# import json
from datetime import datetime, timezone


class Weather:
    # User agent to identify requests
    USER_AGENT = "(https://github.com/jkomalley/weather, j.kyle.omalley@gmail.com)"

    # NWS API address
    NWS_API_ADDRESS = "https://api.weather.gov"

    # ENDPOINTS
    GET_POINT_METADATA = "/points/{point}"
    GET_RAW_FORECAST_DATA = "/gridpoints/{wfo}/{x},{y}"
    GET_HOURLY_FORECAST_DATA = "/gridpoints/{wfo}/{x},{y}/forecast/hourly"
    GET_STATIONS = "/gridpoints/{wfo}/{x},{y}/stations"
    GET_LATEST_STATION_OBSERVATION = "/stations/{stationId}/observations/latest"
    GET_ACTIVE_ALERTS = "/alerts/active/zone/{zoneId}"

    def __init__(self, latitude, longitude):
        self.properties = self._getLocationMetadata(latitude, longitude)

        self.gridID = self.properties["gridId"]
        self.gridX = self.properties["gridX"]
        self.gridY = self.properties["gridY"]
    
    def getAlerts(self):
        ret = []

        # parse zone id from location properties
        zoneId = self.properties["forecastZone"].split("/")[-1]

        url = self.NWS_API_ADDRESS + self.GET_ACTIVE_ALERTS.format(
            zoneId=zoneId
        )

        headers = {"user_agent": self.USER_AGENT, "accept": "application/ld+json"}

        response = requests.get(url, headers=headers)

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(f"Error: {str(e)}")
            exit()

        # print(json.dumps(response.json(), indent=4))
        
        rawAlerts = response.json()["@graph"]
        
        for rawAlert in rawAlerts:
            alert = rawAlert["parameters"]["NWSheadline"][0]
            ret.append(alert)

        return ret

    def getTemperature(self):
        # get station id
        stationId = self._getStationId()

        # get latest observation
        observation = self._getLatestObservation(stationId)

        temp = observation["temperature"]["value"]

        if observation["temperature"]["unitCode"] == "wmoUnit:degC":
            temp = Weather.CtoF(temp)

        return temp

    def getConditions(self):
        # get station id
        stationId = self._getStationId()

        # get latest observation
        observation = self._getLatestObservation(stationId)

        # print(json.dumps(observation, indent=4))

        conditions = observation["textDescription"].lower()

        return conditions

    def getWindChill(self):
        # get station id
        stationId = self._getStationId()

        # get latest observation
        observation = self._getLatestObservation(stationId)

        windChill = observation["windChill"]["value"]

        units = observation["windChill"]["unitCode"]

        if windChill and units == "wmoUnit:degC":
            windChill = Weather.CtoF(windChill)

        # print(f"{windChill = }")
        # print(json.dumps(observation, indent=4))

        return windChill
    
    def getHumidity(self):
        # get station id
        stationId = self._getStationId()

        # get latest observation
        observation = self._getLatestObservation(stationId)

        humidity = observation["relativeHumidity"]["value"]

        # units = observation["humidity"]["unitCode"]

        # if humidity and units == "wmoUnit:degC":
        #     humidity = Weather.CtoF(humidity)

        # print(f"{humidity = }")
        # print(json.dumps(observation, indent=4))

        return humidity
    
    def getDewPoint(self):
        # get station id
        stationId = self._getStationId()

        # get latest observation
        observation = self._getLatestObservation(stationId)

        dewpoint = observation["dewpoint"]["value"]

        units = observation["dewpoint"]["unitCode"]

        if dewpoint and units == "wmoUnit:degC":
            dewpoint = Weather.CtoF(dewpoint)

        # print(f"{dewpoint = }")
        # print(json.dumps(observation, indent=4))

        return dewpoint
    
    def getWindSpeed(self):
        # get station id
        stationId = self._getStationId()

        # get latest observation
        observation = self._getLatestObservation(stationId)

        windSpeed = observation["windSpeed"]["value"]
        units = observation["windSpeed"]["unitCode"]
        if windSpeed and units == "wmoUnit:km_h-1":
            windSpeed = Weather.KPHtoMPH(windSpeed)

        windDirection = observation["windDirection"]["value"]
        if windDirection:
            windDirection = Weather.degToCardinal(windDirection)

        # print(f"{windSpeed = }")
        # print(f"{windDirection = }")
        # print(json.dumps(observation, indent=4))

        return f"{windDirection.upper()} {windSpeed:.0f} mph"
    
    def getLastUpdateTime(self):
        # get station id
        stationId = self._getStationId()

        # get latest observation
        observation = self._getLatestObservation(stationId)

        # print(json.dumps(observation, indent=4))

        update_timestamp = observation["timestamp"]

        # print(f"{update_timestamp = }")

        utc_update_datetime = datetime.fromisoformat(update_timestamp)
        utc_update_datetime = utc_update_datetime.replace(tzinfo=timezone.utc)
        local_update_datetime = utc_update_datetime.astimezone()

        # print(f"{local_update_datetime.strftime("%d %B %I:%M %p %Z")}")

        return local_update_datetime.strftime("%d %B %I:%M %p %Z")

    def getForecast(self):
        return "Idk maybe some rain"

    def _getHourlyData(self):
        url = self.NWS_API_ADDRESS + self.GET_HOURLY_FORECAST_DATA.format(
            wfo=self.gridID, x=self.gridX, y=self.gridY
        )

        headers = {"user_agent": self.USER_AGENT, "accept": "application/ld+json"}

        response = requests.get(url, headers=headers)

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(f"Error: {str(e)}")
            exit()

        # print(json.dumps(response.json(), indent=4))

        data = response.json()

        return data

    def _getLatestObservation(self, stationId):
        if hasattr(self, "_latestObservation"):
            return self._latestObservation
        
        url = self.NWS_API_ADDRESS + self.GET_LATEST_STATION_OBSERVATION.format(
            stationId=stationId
        )

        headers = {"user_agent": self.USER_AGENT, "accept": "application/ld+json"}

        response = requests.get(url, headers=headers)

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(f"Error: {str(e)}")
            exit()

        # print(json.dumps(response.json(), indent=4))
        
        self._latestObservation = response.json()

        return self._latestObservation

    def _getStationId(self):
        if hasattr(self, "_stationId"):
            return self._stationId

        url = self.NWS_API_ADDRESS + self.GET_STATIONS.format(
            wfo=self.gridID, x=self.gridX, y=self.gridY
        )

        headers = {"user_agent": self.USER_AGENT, "accept": "application/ld+json"}

        response = requests.get(url, headers=headers)

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(f"Error: {str(e)}")
            exit()

        # print(json.dumps(response.json(), indent=4))

        # print(response.url)

        # print(json.dumps(response.json()["@graph"][0]["stationIdentifier"], indent=4))

        stationId = response.json()["@graph"][0]["stationIdentifier"]

        self._stationId = stationId

        return self._stationId

    def _getLocationMetadata(self, latitude, longitude):
        url = self.NWS_API_ADDRESS + self.GET_POINT_METADATA.format(
            point=f"{latitude},{longitude}"
        )

        headers = {"user_agent": self.USER_AGENT, "accept": "application/ld+json"}

        response = requests.get(url, headers=headers)

        # print(json.dumps(response.json(), indent=4))

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(f"Error: {str(e)}")
            exit()

        metadata = response.json()

        return metadata

    def CtoF(tempurature):
        return (tempurature * 9.0/5.0) + 32

    def degToCardinal(deg):
        val=int((deg/22.5)+.5)
        arr=["N","NNE","NE","ENE","E","ESE", "SE", "SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"]
        return arr[(val % 16)]

    def KPHtoMPH(kph):
        return kph * 0.621371
