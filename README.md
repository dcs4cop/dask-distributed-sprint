# DCFS demo

## EC2 instances

__Note:__

The dask scheduler's, jupyter notebook's and mongodb's public IPs are elastic IPs and therefore don't change on 
restarting the EC2 instance.


| Name                     | Instance ID         | Instance Type | Availability Zone | Instance State | Status Checks     | Alarm Status | Public DNS (IPv4)                                    | IPv4 Public IP |
|--------------------------|---------------------|---------------|-------------------|----------------|-------------------|--------------|------------------------------------------------------|----------------|
| dcfs-dask-mongo          | i-0c7d016594e28f27f | t2.medium     | eu-central-1c     | running        | 2/2 checks passed | None         | ec2-3-120-53-215.eu-central-1.compute.amazonaws.com  | 3.120.53.215   |
| dcfs-dask-worker1        | i-01d8df58dffac1257 | m5a.4xlarge   | eu-central-1c     | running        | 2/2 checks passed | None         | ec2-3-122-99-186.eu-central-1.compute.amazonaws.com  | 3.122.99.186   |
| dcfs-dask-worker2        | i-08d74285816c954e5 | m5a.4xlarge   | eu-central-1c     | running        | 2/2 checks passed | None         | ec2-18-197-164-4.eu-central-1.compute.amazonaws.com  | 18.197.164.4   |
| dcfs-dask-worker3        | i-0a09e01e4207f342f | m5a.4xlarge   | eu-central-1c     | running        | 2/2 checks passed | None         | ec2-3-120-145-89.eu-central-1.compute.amazonaws.com  | 3.120.145.89   |
| dcfs-dask-worker4        | i-069d25df87a475799 | m5a.4xlarge   | eu-central-1c     | running        | 2/2 checks passed | None         | ec2-35-158-100-79.eu-central-1.compute.amazonaws.com | 35.158.100.79  |
| dcfs-demo-dask-scheduler | i-0026ca9337838073b | t2.medium     | eu-central-1c     | running        | 2/2 checks passed | None         | ec2-52-58-160-50.eu-central-1.compute.amazonaws.com  | 52.58.160.50   |
| dcfs-demo-jupyter        | i-037584cb06c89904e | m5a.4xlarge   | eu-central-1c     | running        | 2/2 checks passed | None         | ec2-3-123-65-163.eu-central-1.compute.amazonaws.com  | 3.123.65.163   |


## How to restart the jupyter notbook

```
ssh aws-dask-jupyter
cd dask-distributed-sprint/docker_jupyter
docker-compose ps
```

For a clean start (e.g. code or environment vars have changed)

```
docker-compose kill
docker-compose rm -f
docker-compose build
docker-compose up -d
```

## How to start the scheduler

```
ssh aws-dask-scheduler
cd dask-distributed-sprint/docker_scheduler
docker-compose ps
```

For a clean start (e.g. code or environment vars have changed)

```
docker-compose kill
docker-compose rm -f
docker-compose build
docker-compose up -d
```

## How to (re-)start a worker

Check the status

```
ssh aws-dask-worker[1,2,3,4]
cd dask-distributed-sprint/docker_worker
docker-compose ps
```

For a clean start (e.g. code or environment vars have changed)

```
docker-compose kill
docker-compose rm -f
docker-compose build

docker-compose up -d
```


All necessary environment variables are in ```.env``` Except LOCAL_IP which is set on login in ```.bashrc```.


# dask-distributed-sprint Primary Production

## Running a Scheduler VM

The scheduler has been installed on a VM called dask-scheduler which uses the base image image-dask-scheduler-v1. The 
scheduler container will be started automatically on boot and will expose the ports 8786 (scheduler) and 8787 
(bokeh monitor). The port 8787 is mapped to the VM host port 80 and thus accessible from the outside via http. 

The following configuration has been used for the scheduler VM:

- The private image ```image-dask-scheduler-v1```
- The 'router' ```vpc-dask```
- The security group ```sg-dask```
- EIP: ```80.158.2.66```

The scheduler container has been installed using:

- dask-scheduler/Dockerfile
- [xcube conda environment](https://github.com/dcs4cop/xcube)
- which uses dask 1.2.2


To start the docker container use the update/start procedure below.


## Running a Worker VM

The worker has been installed on a VM called dask-worker-[number] which uses the base image ```image-dask-worker-v1```. 
The worker container is started automatically and will expose three ports of range 9000-9100 (worker 9000, 
nanny 9010, bokeh 9020). These ports can be configured in the file ```.env```. The worker registers itself to the 
scheduler.   

The following configuration has been used for the worker VM:

- The private image ```image-dask-worker-v1```
- The 'router' ```vpc-dask```
- The security group ```sg-dask```
- EIP: None. THE VPC router is configured whith SNAT enabled which allows the workers outbound connections

The scheduler itself has been installed using:

- [xcube conda environment](https://github.com/dcs4cop/xcube)
- which uses dask 1.2.2
- ports are configured in .env 
  - scheduler 192.168.1.166

For [re-]starting the worker, user the update procedure.

## UpdatingStarting a worker7scheduler VM

To update or manually starting a scheduler/worker user the sequence below. 
Modify the Dockerfile if you wish a different xcube version (this proceduer uses xcube version: 'latest').
=======
To update the xcube version to use in the work or scheduler, you will need to rebuild the docker image. At this stage, the 
image uses the latest version of xcube. Modify the Dockerfile if you wish to use a different version.
>>>>>>> e510ec11b7fab7e5f3011d9e08e9deef37167abc

Do the following:

- Start VM
- Login to VM
- Go to directory dask-distributed-sprint
- Go to directory dask-distributed-sprint/docker-[worker/scheduler]
- Exec: 

```
docker-compose build
docker-compose up -d
```

The build step can be omitted if nothing in the container needs to be updated. 

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

## Current VMS

- ecs-dask-scheduler
  - scheduler port: 8786
  - bokeh port: 8787 mapping to http://80.158.2.66
- ecs-dask-worker-0001:
  - worker port: 9010
  - nanny port: 9011
  - bokeh port: 9012
- ecs-dask-worker-0002:
  - worker port: 9020
  - nanny port: 9021
  - bokeh port: 9022
- ecs-dask-worker-0003:
  - worker port: 9030
  - nanny port: 9031
  - bokeh port: 9032
- ecs-dask-worker-0004:
  - worker port: 9040
  - nanny port: 9041
  - bokeh port: 9042


