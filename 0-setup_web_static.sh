#!/usr/bin/env bash

# bash script that sets up web servers for deployment of web_static

sudo apt update -y
sudo apt install -y nginx

sudo mkdir -p /data/web_static/shared/
sudo mkdir -p /data/web_static/releases/test/

cat <<EOF > /data/web_static/releases/test/index.html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Welcome to My Test Server</title>
</head>
<body>
    <h1>It works!</h1>
    <p>This is a fake page served by Nginx</p>
</body>
</html>
EOF

sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

sudo chown -R mwangii:mwangii /data/

sudo bash -c 'cat > /etc/nginx/sites-available/default << "EOF"
  server {
    listen 80 default_server;
    listen [::]:80 default_server;

    root /var/www/html;
    index index.html index.htm;

    server_name _;

    location /mwj_static {
      alias /data/web_static/current/;
    }
  }
EOF'

sudo service nginx reload
