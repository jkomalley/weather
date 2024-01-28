import click
from weather import weather

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
    w = weather.Weather(39.215833, -76.709167)

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
        t = w.getCurrentTemperature()
        c = w.getConditions()
        print(f"Tempurature: {t}{DEGREE_SIGN}F")
        print(f"Weather: {c}")


if __name__ == "__main__":
    run()
