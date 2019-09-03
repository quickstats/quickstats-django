# Standalone personal stats server

A simple stats server to provide a personal stats dashboard created as a personal replacement for [numerous] which was shutdown.

## Goals

- Simple stats tracker in the style of [numerous]
- Grafana support through [grafana-json-datasource]
- Support for Prometheus's [pushgateway]
- Support for different charts

  - Basic
  - Countdown
  - Location

Support    | Input         | Output
---------- | ------------- | -------------------------
Prometheus | [pushgateway] | X
Grafana    |               | [grafana-json-datasource]

## Local Development

```
virtualenv --python python3 simplestats
pip install -e .[standalone]
simplestats migrate
simplestats createsuperuser
simplestats runserver
```

## Using with Grafana

Using the [grafana-json-datasource] plugin you can connect to the `/stats/grafana` endpoint and generate graphs from the underlying data

## Clients

- <https://github.com/kfdm/alfred-simplestats>
- <https://github.com/kfdm/bitbar-simplestats>
- <https://github.com/kfdm/ios-simplestats>

[grafana-json-datasource]: https://grafana.net/plugins/grafana-simple-json-datasource
[numerous]: https://www.youtube.com/watch?v=c0A9hEUnAOM
[pushgateway]: https://github.com/prometheus/pushgateway
