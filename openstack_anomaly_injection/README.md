# Install library

`python3 setup.py install`

# Usage:

- anomaly: 
```bash
chaos anomaly container --host wally098.cit.tu-berlin.de --id 1174a29bff7e  stress stress-ng -t 20s --stressors "--cpu 8"
```
- admin:
```bash
chaos admin node list
```

# Generate docs
In the `docs/` folder:
```bash
make clean build
```

# Debug mode

In order to view debug logs, use `--debug` flag in `chaos` command.

# Rally
### Init rally
```bash
source ./admin-openrc.sh
rally db create
rally deployment create --fromenv --name=default
```
### Run rally task
```bash
rally  --plugin-paths ./openstack_anomaly_injection/anomaly_injection/rally_plugin.py task start ./test_rally.yaml --deployment default
```
