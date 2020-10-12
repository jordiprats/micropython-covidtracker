# micropython-covidtracker

## Config

config.py

```python
wifi_config = {
    'ssid':'SID',
    'password':'PASW0RD'
}

covid_config = {
    'baseurl': 'http://1.1.1.1:5000',
    'school': '1234'
}
```

## Upload

```
bash upload.sh
```

## Dependencies

https://github.com/mcauser/micropython-tm1637
