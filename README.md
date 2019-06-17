# dask-distributed-sprint

## Setup VM

Login to the OTC and create a VM using the privete image ```image-dask-v1```. Configure the network 
using the 'router' ```vpc-dask``` and the security grouop ```sg-dask```.

Starting the VM will start a docker container automatically using the xcube conda environment. 

Describe start worker/ schewduler


## Updating VM

To update the xcube version to use in the work or scheduler, you will need to rebuild the docker image. At this stage, the 
image uses the latest version of xcube. Modify the Dockerfile if you wish to use a different version.

Do the following:

- Start VM
- Login to VM
- Go to directory dask-distributed-sprint/docker-[worker/scheduler]
- Exec: 

```
docker-compose build
docker-compose up -d
```


## Configure Reverse proxy

The scheduler VM does not allow to allocate ports 80 and 443 to the daskboard. We, hence, need a reverse proxy to gain public accesst to the whole monitoring infrastructure.

The scheduler VM uses NGINX with the following configuration in ```/etx/ngins/sites-available```. The monitoring site
will be available  under ```http://80.158.2.66```.

```
server {
    listen 80;
    server_name 80.158.2.66;

    location / {
          proxy_pass http://localhost:8787;
          proxy_set_header Host $http_host;
          proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
          proxy_set_header X-Real-IP $remote_addr;
          proxy_http_version 1.1;
          proxy_redirect off;
          proxy_buffering off;
          proxy_set_header Upgrade $http_upgrade;
          proxy_set_header Connection "upgrade";
          proxy_read_timeout 86400;
      }
}
```


