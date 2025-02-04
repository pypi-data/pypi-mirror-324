from typing import List

class WeatherPayload:
    def __init__(
        self,
        locale_id: int = None,
        station_id: str = None,
        latitude: float = None,
        longitude: float = None,
        timezone: int = None,
        variables: List[str] = None,
        start_date: str = None,
        end_date: str = None,
    ):
        """
        Initializes the WeatherPayload object with optional parameters.
        """
        self.locale_id = locale_id
        self.station_id = station_id 
        self.latitude = latitude
        self.longitude = longitude
        self.timezone = timezone
        self.variables = variables
        self.start_date = start_date
        self.end_date = end_date

    def get_params(self) -> dict:
        """
        Returns the parameters as a dictionary for API requests.
        """
        return {
            "localeId": self.locale_id,
            "stationId": self.station_id,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "timezone": self.timezone,
            "variables[]": self.variables,
            "startDate": self.start_date,
            "endDate": self.end_date,
        }

class CurrentWeatherPayload:
    def __init__(
        self,
        locale_id: int = None,
        station_id: str = None,
        latitude: float = None,
        longitude: float = None,
        timezone: int = None,
        variables: List[str] = None,
    ):
        """
        Initializes the CurrentWeatherPayload object with optional parameters.
        """
        self.locale_id = locale_id
        self.station_id = station_id 
        self.latitude = latitude
        self.longitude = longitude
        self.timezone = timezone
        self.variables = variables
    
    def get_params(self) -> dict:
        """
        Returns the parameters as a dictionary for API requests.
        """
        return {
            "localeId": self.locale_id,
            "stationId": self.station_id,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "timezone": self.timezone,
            "variables[]": self.variables,
        }

class ClimatologyPayload:
    def __init__(
        self,
        locale_id: int = None,
        station_id: str = None,
        latitude: float = None,
        longitude: float = None,
        variables: List[str] = None,
    ):
        """
        Initializes the ClimatologyPayload object with optional parameters.
        """
        self.locale_id = locale_id
        self.station_id = station_id
        self.latitude = latitude
        self.longitude = longitude
        self.variables = variables

    def get_params(self) -> dict:
        """
        Returns the parameters as a dictionary for API requests.
        """
        return {
            "localeId": self.locale_id,
            "stationId": self.station_id,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "variables[]": self.variables,
        }

class RadiusPayload:
    def __init__(
        self,
        locale_id: int = None,
        station_id: str = None,
        latitude: float = None,
        longitude: float = None,
        start_date: str = None,
        end_date: str = None,
        radius: int = None,
    ):
        """
        Initializes the RadiusPayload object with optional parameters.
        """
        self.locale_id = locale_id
        self.station_id = station_id 
        self.latitude = latitude
        self.longitude = longitude
        self.start_date = start_date
        self.end_date = end_date
        self.radius = radius

    def get_params(self) -> dict:
        """
        Returns the parameters as a dictionary for API requests.
        """
        return {
            "localeId": self.locale_id,
            "stationId": self.station_id,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "startDate": self.start_date,
            "endDate": self.end_date,
            "radius": self.radius,
        }

class StationPayload:
    def __init__(
        self,
        station_id: str = None,
        layer: str = None,
        variables: List[str] = None,
        start_date: str = None,
        end_date: str = None,
    ):
        """
        Initializes the StationPayload object with optional parameters.
        """
        self.station_id = station_id 
        self.layer = layer
        self.variables = variables
        self.start_date = start_date
        self.end_date = end_date

    def get_params(self) -> dict:
        """
        Returns the parameters as a dictionary for API requests.
        """
        return {
            "stationId": self.station_id,
            "layer": self.layer,
            "variables[]": self.variables,
            "startDate": self.start_date,
            "endDate": self.end_date,
        }

class GeometryPayload:
    def __init__(
        self,
        radius: int = None,
        start_date: str = None,
        end_date: str = None,
        geometry: str = None
    ):
        """
        Initializes the GeometryPayload object with optional parameters.
        """
        self.radius = radius
        self.start_date = start_date
        self.end_date = end_date
        self.geometry = geometry

    def get_params(self) -> dict:
        """
        Returns the parameters as a dictionary for API requests.
        """
        return {
            "radius": self.radius,
            "startDate": self.start_date,
            "endDate": self.end_date,
        }

    def getBody(self) -> dict:
        """
        Returns the body of the request with the geometry information.
        """
        return {
            "geometry": self.geometry,
        }

class TmsPayload:
    def __init__(
        self,
        istep: str = None,
        fstep: str = None,
        server: str = None,
        mode: str = None,
        variable: str = None,
        aggregation: str = None,
        x: int = None,
        y: int = None,
        z: int = None,
    ):
        """
        Initializes the TmsPayload object with optional parameters.
        """
        self.istep = istep
        self.fstep = fstep
        self.server = server
        self.mode = mode
        self.variable = variable
        self.aggregation = aggregation
        self.x = x
        self.y = y
        self.z = z

    def get_params(self) -> dict:
        """
        Returns the parameters as a dictionary for API requests.
        """
        return {
            "istep": self.istep,
            "fstep": self.fstep,
        }
