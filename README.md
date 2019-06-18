# dask-distributed-sprint

## Running a Scheduler VM

The scheduler has been installed on a VM called dask-scheduler which uses the basye image dask-scheduler. The 
scheduler container is started automatically and will expose the ports 8786 (scheduler) and 8787 (bokeh monitor).
The port 8787 is mapped to the host port 80 and thus accessible from the outside via http. 

The following configuration has been used for the scheduler VM:

- The private image ```image-dask-scheduler-v1```
- The 'router' ```vpc-dask```
- The security group ```sg-dask```
- EIP: ```80.158.2.66```

The scheduler container has been installed using:

- dask-scheduler/Dockerfile
- [xcube conda environment](https://github.com/dcs4cop/xcube)
- which uses dask 1.2.2


To start docker container use the update procedure below.


## Running a Worker VM

The worker has been installed on a VM called dask-worer-[number] which uses the base image ```image-dask-worker-v1```. 
The worker container is started automatically and will expose threeport of range 9000-9100 (worker, nanny, bokeh).
Teh worker registers itself to the scheduler. When a new worker VM is created, the worker port has to be configured
and the container restarted.  

The following configuration has been used for the worker VM:

- The private image ```image-dask-worker-v1```
- The 'router' ```vpc-dask```
- The security group ```sg-dask```
- EIP: None. THE VPC router is configured whith SNAT enabled which allows the workers outbound connections

The scheduler itself has been installed using:

- [xcube conda environment](https://github.com/dcs4cop/xcube)
- which uses dask 1.2.2
- ports are configured in .env

For [re-]starting the worker, user the update procedure.

## Updating VM

To update the xcube version you will need to rebuild the docker image. At this stage, the image uses the latest version of xcube. Modify the Dockerfile if you wish a different version.


- Start VM
- Login to VM
- Go to directory dask-distributed-sprint
- CD to dask-worker or dask-scheduler
- If you start/update a worker you may want to change the worker ports in .env. They need to be unique across the 
  cluster.
- Exec: 
```
git pull
docker-compose build
docker-compose up -d
```


## Configure Reverse proxy

At this stage the workers cannot be accessed through the bokeh web intgerface on http://80.158.2.66 as the 
worker are located behind a firewall. If that is need a reverse proxy has to be configures. Below is an
example how to do that using nginx and its configuration directory ```/etx/ngins/sites-available```. 
The example shows a reverse proxy to the scheduler bokeh web UI on port 8787. This configuration
is currently NOT used as the docker maps the bokee port 8787 directoy to the HTTP port 80.

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


