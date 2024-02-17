import click
from weather import weather
from rich import print

DEGREE_SIGN = chr(176)


@click.command()
@click.option(
    "-t",
    "--temp_only",
    "display",
    flag_value="tempurature",
    help="Only display the current tempurature.",
)
@click.option(
    "-c",
    "--conditions_only",
    "display",
    flag_value="conditions",
    help="Only display the current conditions.",
)
@click.option(
    "-f",
    "--forecast",
    "display",
    flag_value="forecast",
    help="Display the upcoming forecast.",
)
def run(display):
    lat = 39.215833
    lon = -76.709167
    w = weather.Weather(lat, lon)

    if display == "tempurature":
        t = w.getCurrentTemperature()
        print(f"{t}{DEGREE_SIGN}")

    elif display == "conditions":
        c = w.getConditions()
        print(f"{c}")

    elif display == "forecast":
        f = w.getForecast()
        print(f"{f}")

    else:
        alerts = w.getAlerts()
        t = w.getCurrentTemperature()
        c = w.getConditions()
        wc = 43.0 # w.getWindChill()
        h = 0.29 # w.getHumidity()
        d = 16.0 # w.getDewPoint()
        ws = "W 9 G 20 mph" # w.getWindSpeed()
        lu = "16 February 2:54 pm EST" # w.getLastUpdateTime()

        print(f"[green]Weather near {lat},{lon}[/green]")
        for alert in alerts:
            print(f"[bold red]Alert: {alert}[/bold red]")
        print(f" Conditions: {c.capitalize()}")
        print(f"Tempurature: {t:.2f}{DEGREE_SIGN}F")
        print(f" Wind Chill: {wc:.2f}{DEGREE_SIGN}F")
        print(f"   Humidity: {h * 100:.2f}%")
        print(f"  Dew Point: {d:.2f}{DEGREE_SIGN}F")
        print(f" Wind Speed: {ws}")
        print(f"Last Update: {lu}")


if __name__ == "__main__":
    run()
