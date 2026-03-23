# loki-log-generator

## Create VENV

### Create VENV

```shell
python -m venv venv_loki-log-generator
```

### Activate

```shell
venv_loki-log-generator\Scripts\activate.bat
```

## Install Requirements.txt

```shell
pip install -r requirements.txt
```


# Log QL

``
{service_name="gateway"} | json | client_ip =~ "192\\.168\\.1\\.82"
```

``
{service_name="gateway"} | json | client_ip =~ "192\\.168\\.1\\.82" | method = "POST"
```


``
{service_name="gateway"} | json | client_ip =~ "192\\.168\\.1\\..*"
```