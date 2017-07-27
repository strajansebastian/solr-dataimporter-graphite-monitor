# solr-dataimporter-graphite-monitor
Script used to log into graphite metrics about the performance of an import using the SOLR data import feature.

You should be able to run it once like in the example from below:

```bash
python solr_dataimport_graphite_mon.py solr_dataimport_graphite_mon.conf
```

In order to run it constantly use this in a screen:

```bash
while true; do
    python solr_dataimport_graphite_mon.py solr_dataimport_graphite_mon.conf;
    sleep 1;
done
```
