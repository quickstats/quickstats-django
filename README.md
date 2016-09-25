# Standalone personal stats server

A simple stats server to provide a personal stats dashboard created as a personal replacement for [numerous] which was shutdown.

## Quick deploy with Heroku

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

## Local Development

```
virtualenv --python python3 simplestats
pip install -e .[standalone]
simplestats migrate
simplestats createsuperuser
simplestats runserver
```

## Using with Grafana

Using the [grafana-json] plugin you can connect to the ```/stats/grafana``` endpoint and generate graphs from the underlying data

[numerous]: https://www.youtube.com/watch?v=c0A9hEUnAOM
[grafana-json]: https://grafana.net/plugins/grafana-simple-json-datasource
