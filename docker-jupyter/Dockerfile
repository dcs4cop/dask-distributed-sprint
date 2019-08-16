FROM quay.io/bcdev/xcube:0.2.0.dev1 

MAINTAINER helge.dzierzon@brockmann-consult.de

USER root 

ADD ./xcube-dcfs xcube-dcfs
RUN chown -R xcube.xcube /home/xcube/xcube-dcfs

USER xcube
WORKDIR /home/xcube/xcube-dcfs
RUN source activate xcube && conda install oauthlib=3.0 jupyterlab matplotlib
RUN source activate xcube && pip install requests_oauthlib
RUN source activate xcube && python setup.py install

WORKDIR /home/xcube

ENTRYPOINT ["/bin/bash", "-c"]



