from .query_builder import QueryParamsBuilder
from .payloads import *

class ForecastAPI:
    def __init__(self, request_handler):
        self.request_handler = request_handler

    def get_daily(self, payload: WeatherPayload):
        """
        Fetch daily weather forecast.
        GET /v1/forecast/daily
        """
        builder = QueryParamsBuilder()
        params = (
            builder
            .add_payload(payload.get_params())
            .add_token("token", self.request_handler.token)
            .build()
        )
        return self.request_handler.make_request("GET", "v1/forecast/daily", params=params)

    def get_hourly(self, payload: WeatherPayload):
        """
        Fetch hourly weather forecast.
        GET /v1/forecast/hourly
        """
        builder = QueryParamsBuilder()
        params = (
            builder
            .add_payload(payload.get_params())
            .add_token("token", self.request_handler.token)
            .build()
        )
        return self.request_handler.make_request("GET", "v1/forecast/hourly", params=params)
    
    def get_period(self, payload: WeatherPayload):
        """
        Fetch period weather forecast.
        GET /v1/forecast/period
        """
        builder = QueryParamsBuilder()
        params = (
            builder
            .add_payload(payload.get_params())
            .add_token("token", self.request_handler.token)
            .build()
        )
        return self.request_handler.make_request("GET", "v1/forecast/period", params=params)

class ObservedAPI:
    def __init__(self, request_handler):
        self.request_handler = request_handler

    def get_daily(self, payload: WeatherPayload):
        """
        Fetch daily weather observed.
        GET /v1/observed/daily
        """
        builder = QueryParamsBuilder()
        params = (
            builder
            .add_payload(payload.get_params())
            .add_token("token", self.request_handler.token)
            .build()
        )
        return self.request_handler.make_request("GET", "v1/observed/daily", params=params)

    def get_hourly(self, payload: WeatherPayload):
        """
        Fetch hourly weather observed.
        GET /v1/observed/hourly
        """
        builder = QueryParamsBuilder()
        params = (
            builder
            .add_payload(payload.get_params())
            .add_token("token", self.request_handler.token)
            .build()
        )
        return self.request_handler.make_request("GET", "v1/observed/hourly", params=params)
    
    def get_period(self, payload: WeatherPayload):
        """
        Fetch period weather observed.
        GET /v1/observed/period
        """
        builder = QueryParamsBuilder()
        params = (
            builder
            .add_payload(payload.get_params())
            .add_token("token", self.request_handler.token)
            .build()
        )
        return self.request_handler.make_request("GET", "v1/observed/period", params=params)

    def get_station_data(self, payload: StationPayload):
        """
        Fetch station observed.
        GET /v1/station
        """
        builder = QueryParamsBuilder()
        params = (
            builder
            .add_payload(payload.get_params())
            .add_token("token", self.request_handler.token)
            .build()
        )
        return self.request_handler.make_request("GET", "v1/station", params=params)

    def get_fire_focus(self, payload: RadiusPayload):
        """
        Fetch observed fire focus.
        GET /v1/observed/fire-focus
        """
        builder = QueryParamsBuilder()
        params = (
            builder
            .add_payload(payload.get_params())
            .add_token("token", self.request_handler.token)
            .build()
        )
        return self.request_handler.make_request("GET", "v1/observed/fire-focus", params=params)
    
    def get_lightning(self, payload: RadiusPayload):
        """
        Fetch observed lightning.
        GET /v1/observed/lightning
        """
        builder = QueryParamsBuilder()
        params = (
            builder
            .add_payload(payload.get_params())
            .add_token("token", self.request_handler.token)
            .build()
        )
        return self.request_handler.make_request("GET", "v1/observed/lightning", params=params)
    
    def get_fire_focus_by_geometry(self, payload: GeometryPayload):
        """
        Fetch observed fire focus.
        POST /v1/observed/fire-focus
        """
        builder = QueryParamsBuilder()
        params = (
            builder
            .add_payload(payload.get_params())
            .add_token("token", self.request_handler.token)
            .build()
        )
        return self.request_handler.make_request("POST", "v1/observed/fire-focus", params=params, json_data=payload.getBody())
    
    def get_lightning_by_geometry(self, payload: GeometryPayload):
        """
        Fetch observed lightning.
        POST /v1/observed/lightning
        """
        builder = QueryParamsBuilder()
        params = (
            builder
            .add_payload(payload.get_params())
            .add_token("token", self.request_handler.token)
            .build()
        )
        return self.request_handler.make_request("POST", "v1/observed/lightning", params=params, json_data=payload.getBody())

class CurrentWeatherAPI:
    def __init__(self, request_handler):
        self.request_handler = request_handler

    def get(self, payload: CurrentWeatherPayload):
        """
        Fetch current weather.
        GET /v1/current-weather
        """
        builder = QueryParamsBuilder()
        params = (
            builder
            .add_payload(payload.get_params())
            .add_token("token", self.request_handler.token)
            .build()
        )
        return self.request_handler.make_request("GET", "v1/forecast/daily", params=params)

class ClimatologyAPI:
    def __init__(self, request_handler):
        self.request_handler = request_handler

    def get_daily(self, payload: ClimatologyPayload):
        """
        Fetch daily climatology weather.
        GET /v1/climatology/daily
        """
        builder = QueryParamsBuilder()
        params = (
            builder
            .add_payload(payload.get_params())
            .add_token("token", self.request_handler.token)
            .build()
        )
        return self.request_handler.make_request("GET", "v1/climatology/daily", params=params)

    def get_monthly(self, payload: ClimatologyPayload):
        """
        Fetch monthly climatology weather.
        GET /v1/climatology/monthly
        """
        builder = QueryParamsBuilder()
        params = (
            builder
            .add_payload(payload.get_params())
            .add_token("token", self.request_handler.token)
            .build()
        )
        return self.request_handler.make_request("GET", "v1/climatology/monthly", params=params)

class MonitoringAlertsAPI:
    def __init__(self, request_handler):
        self.request_handler = request_handler

    def get_alerts(self):
        """
        Fetch alerts.
        GET /v1/monitoring/alerts
        """
        builder = QueryParamsBuilder()
        params = (
            builder
            .add_token("token", self.request_handler.token)
            .build()
        )
        return self.request_handler.make_request("GET", "v1/monitoring/alerts", params=params)

class PlanAPI:
    def __init__(self, request_handler):
        self.request_handler = request_handler

    def get_info(self):
        """
        Fetch plan information.
        GET /v1/plan/{token}
        """
        return self.request_handler.make_request("GET", f"v1/plan/{self.request_handler.token}")

class ChartAPI:
    def __init__(self, request_handler):
        self.request_handler = request_handler

    def get_forecast_daily(self, payload: WeatherPayload):
        """
        Fetch daily weather forecast chart.
        GET /v1/forecast/daily/chart
        """
        builder = QueryParamsBuilder()
        params = (
            builder
            .add_payload(payload.get_params())
            .add_token("token", self.request_handler.token)
            .build()
        )
        return self.request_handler.make_request("GET", "v1/forecast/daily/chart", params=params)
    
    def get_forecast_hourly(self, payload: WeatherPayload):
        """
        Fetch hourly weather forecast chart.
        GET /v1/forecast/hourly/chart
        """
        builder = QueryParamsBuilder()
        params = (
            builder
            .add_payload(payload.get_params())
            .add_token("token", self.request_handler.token)
            .build()
        )
        return self.request_handler.make_request("GET", "v1/forecast/hourly/chart", params=params)
    
    def get_observed_daily(self, payload: WeatherPayload):
        """
        Fetch daily observed weather chart.
        GET /v1/observed/daily/chart
        """
        builder = QueryParamsBuilder()
        params = (
            builder
            .add_payload(payload.get_params())
            .add_token("token", self.request_handler.token)
            .build()
        )
        return self.request_handler.make_request("GET", "v1/observed/daily/chart", params=params)
    
    def get_observed_hourly(self, payload: WeatherPayload):
        """
        Fetch hourly observed weather chart.
        GET /v1/observed/hourly/chart
        """
        builder = QueryParamsBuilder()
        params = (
            builder
            .add_payload(payload.get_params())
            .add_token("token", self.request_handler.token)
            .build()
        )
        return self.request_handler.make_request("GET", "v1/observed/hourly/chart", params=params)

class TmsAPI:
    def __init__(self, request_handler):
        self.request_handler = request_handler

    def get(self, payload: TmsPayload):
        """
        Fetch daily weather forecast.
        GET /v1/tms/{server}/{mode}/{variable}/{aggregation}/{x}/{y}/{z}.png
        """
        builder = QueryParamsBuilder()
        params = (
            builder
            .add_payload(payload.get_params())
            .add_token("token", self.request_handler.token)
            .build()
        )
        path = f"v1/tms/{payload.server}/{payload.mode}/{payload.variable}/{payload.aggregation}/{payload.x}/{payload.y}/{payload.z}.png"
        return self.request_handler.make_request("GET", path, params=params)

class SchemaAPI:
    def __init__(self, request_handler):
        self.request_handler = request_handler

    def get_definition(self):
        """
        Fetch schema definition.
        GET /v1/schema/definition
        """
        builder = QueryParamsBuilder()
        params = (
            builder
            .add_token("token", self.request_handler.token)
            .build()
        )
        return self.request_handler.make_request("GET", "v1/schema/definition", params=params)
    
    def post_definition(self, payload):
        """
        Set schema definition.
        POST /v1/schema/definition
        """
        builder = QueryParamsBuilder()
        params = (
            builder
            .add_token("token", self.request_handler.token)
            .build()
        )
        return self.request_handler.make_request("POST", "v1/schema/definition", params=params, json_data=payload)
    
    def post_parameters(self, payload):
        """
        Post schema parameters.
        POST /v1/schema/parameters
        """
        builder = QueryParamsBuilder()
        params = (
            builder
            .add_token("token", self.request_handler.token)
            .build()
        )
        return self.request_handler.make_request("POST", "v1/schema/parameters", params=params, json_data=payload)
