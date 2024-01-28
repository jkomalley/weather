import requests
import json
import datetime


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

    def __init__(self, latitude, longitude):
        self.properties = self._getLocationMetadata(latitude, longitude)

        self.gridID = self.properties["gridId"]
        self.gridX = self.properties["gridX"]
        self.gridY = self.properties["gridY"]

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

    def getAlerts(self):
        return "AHHHHHHH WE'RE ALL GONNA DIE"

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

        return response.json()

    def _getStationId(self):
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

        return stationId

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
