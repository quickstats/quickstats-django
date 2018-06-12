# Standalone personal stats server

A simple stats server to provide a personal stats dashboard created as a personal replacement for [numerous] which was shutdown.

## Goals

* Simple stats tracker in the style of [numerous]
* Grafana support through [grafana-json-datasource]
* Support for Prometheus's [pushgatway]
* Support for different charts
  * Basic
  * Countdown
  * Location


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

Using the [grafana-json-datasource] plugin you can connect to the ```/stats/grafana``` endpoint and generate graphs from the underlying data

## Clients

* https://github.com/kfdm/alfred-simplestats
* https://github.com/kfdm/bitbar-simplestats
* https://github.com/kfdm/ios-simplestats

[numerous]: https://www.youtube.com/watch?v=c0A9hEUnAOM
[grafana-json-datasource]: https://grafana.net/plugins/grafana-simple-json-datasource
[pushgateway]: https://github.com/prometheus/pushgateway
