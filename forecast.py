import forecastio
import os

dskey = os.environ['DARK_SKY_API_KEY']


def get_forecast(lat, lng):
    """ Get forecast for the requested location. """

    f = forecastio.load_forecast(dskey, lat, lng)

    hourly = f.hourly()
    hourly_sum = hourly.summary
    hourly_icon = hourly.icon

    hourly_f = []

    for hourly_data in hourly.data:
        hourly_f.append(hourly_data.temperature)

    return hourly_sum, hourly_icon, hourly_f
