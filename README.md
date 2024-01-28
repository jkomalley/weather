# weather
A Weather app.

## Usage
```
$ poetry run weather --help
Usage: weather [OPTIONS]

Options:
  -t, --temp_only        Only display the current tempurature.
  -c, --conditions_only  Only display the current conditions.
  -f, --forecast         Display the upcoming forecast.
  --help                 Show this message and exit.
```
```
$ poetry run weather             
Currently it is 50.0° and cloudy.
```
```
$ poetry run weather -t  
50.0°
```
```
$ poetry run weather -c
cloudy
```
