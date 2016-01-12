from debian

maintainer dpfg

run apt-get update
run apt-get install -y build-essential git
run apt-get install -y python3 python3-dev python3-setuptools
run apt-get install -y nginx supervisor
run easy_install3 pip

# install uwsgi now because it takes a little while
run pip install uwsgi

# install nginx
run apt-get install -y software-properties-common python-software-properties

# install our code
add . /home/docker/code/

# setup all the configfiles
run echo "daemon off;" >> /etc/nginx/nginx.conf
run rm /etc/nginx/sites-enabled/default
run ln -s /home/docker/code/ops/nginx-app.conf /etc/nginx/sites-enabled/
run ln -s /home/docker/code/ops/supervisor-app.conf /etc/supervisor/conf.d/

# run pip install
run pip install -r /home/docker/code/requirements.txt

expose 80
cmd ["supervisord", "-n"]
