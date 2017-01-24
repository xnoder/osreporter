# osreporter
A tool that pulls in OpenStack data from the API's and then writes it to Elasticsearch or RethinkDB. Or both.

## Config

You need a file called `/etc/osreporter.yaml` which looks like:

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

...obviously modifying the addresses for your own environment.

## Usage

By and large, I use this to visualize data within Kibana from an Elasticsearch server. To do this:

```
$ osreporter --db elastic
```

If you'd rather write data to RethinkDB:

```
$ osreporter --db rethink
```

or you can send the data to both services:

```
$ osreporter --db merged
```

RethinkDB is where I normally store data to run against matplotlib, while Elastic + Kibana is good for
dashboards and reporting purposes. I expect that most of my development into the future will focus on
RethinkDB and matplotlib.

## Copyright

Copyright &copy; 2017 Paul Stevens

## License

Licensed under the MIT License. See LICENSE for details.
