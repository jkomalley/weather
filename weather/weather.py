import requests
# import json
# import datetime


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

        print(f"{zoneId = }")

        url = self.NWS_API_ADDRESS + self.GET_ACTIVE_ALERTS.format(
            zoneId=zoneId
        )

        # print(f"{url = }")

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
            print(rawAlert)
            print(type(rawAlert))
            alert = rawAlert["parameters"]["NWSheadline"][0]
            ret.append(alert)

        return ret

    def getCurrentTemperature(self):
        # get station id
        stationId = self._getStationId()

        # get latest observation
        observation = self._getLatestObservation(stationId)

        temp = observation["temperature"]["value"]

        if observation["temperature"]["unitCode"] == "wmoUnit:degC":
            temp = (temp * (9.0 / 5.0)) + 32.0

        return temp

    def getConditions(self):
        # get station id
        stationId = self._getStationId()

        # get latest observation
        observation = self._getLatestObservation(stationId)

        # print(json.dumps(observation, indent=4))

        conditions = observation["textDescription"].lower()

        return conditions

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
