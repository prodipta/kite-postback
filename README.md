# kite-postback
A basic web-hook postback handler for handling postback/ webhook from Zerodha Kite API trades. You can use the systemd (or similar) service to daemonize this python app.
```
sudo touch /etc/systemd/system/kite-postback.service
sudo chmod 664 /etc/systemd/system/kite-postback.service
sudo vi /etc/systemd/system/kite-postback.service
```
Inside the file define the followings
```
[Unit]
Description=Kite Order Postback webhook service
After=multi-user.target

[Service]
Type=simple
User=yourpreferredusername
WorkingDirectory=/path/to/the/code
ExecStart=/usr/bin/python /path/to/the/code/postback.py

[Install]
WantedBy=multi-user.target
```
For the specification of the postback data and interpretation, see [here](https://kite.trade/docs/connect/v3/postbacks/)
