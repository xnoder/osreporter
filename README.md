# osreporter
A tool that pulls in OpenStack data from the API's and then writes it to Elasticsearch or Excel.

## Config

You need a file called `~/.osreporter.yaml` which looks like:

```
elastic:
  server: "127.0.0.1"
  port: "9200"
  index: "osreporter"
  type: "usage"
rethinkdb:
  server: "127.0.0.1"
  port: 0
  database: "osreporter"
  table: "usage"
openstack:
  schema: "http"
  address: "127.0.0.1"
```

...obviously modifying the addresses for your own environment. This can be overridden by
supplying an environment variable called `OSREPORTER_CONFIG`.

## Usage

By and large, I use this to visualize data within Kibana from an Elasticsearch server. To do this:

```
$ osreporter --db elastic
```

If you'd rather write data to Excel:

```
$ osreporter --db excel
```

Elastic is useful for creating dashboards on states and quantities, whereas Excel compatibility
allows for some useful reporting.

## Copyright

Copyright &copy; 2017 Paul Stevens

## License

Licensed under the MIT License. See LICENSE for details.
