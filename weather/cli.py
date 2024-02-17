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
        c = w.getConditions()
        t = w.getTemperature()
        wc = w.getWindChill()
        h = w.getHumidity()
        d = w.getDewPoint()
        ws = w.getWindSpeed()
        lu = w.getLastUpdateTime()

        print(f"[cyan on blue] Weather near {lat},{lon} [/cyan on blue]")
        for alert in alerts:
            print(f"[bold red]Alert: {alert}[/bold red]")
        print(f" Conditions: [cyan]{c.capitalize()}[/cyan]")
        print(f"Tempurature: [cyan]{t:.0f}{DEGREE_SIGN}F[/cyan]")
        if wc:
            print(f" Wind Chill: [cyan]{wc:.0f}{DEGREE_SIGN}F[/cyan]")
        print(f"   Humidity: [cyan]{h:.0f}%[/cyan]")
        print(f"  Dew Point: [cyan]{d:.0f}{DEGREE_SIGN}F[/cyan]")
        print(f" Wind Speed: [cyan]{ws}[/cyan]")
        print(f"Last Update: [cyan]{lu}[/cyan]")


if __name__ == "__main__":
    run()
