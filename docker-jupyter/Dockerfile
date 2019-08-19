FROM quay.io/bcdev/xcube:0.2.0.dev1 

MAINTAINER helge.dzierzon@brockmann-consult.de

USER root 

WORKDIR /data
ADD ./xcube-dcfs xcube-dcfs
RUN chown -R xcube.xcube /data/xcube-dcfs
RUN usermod --shell /bin/bash xcube

USER xcube
WORKDIR /data/xcube-dcfs
RUN source activate xcube && conda install oauthlib=3.0 jupyterlab matplotlib
RUN source activate xcube && pip install requests_oauthlib
RUN source activate xcube && python setup.py install

WORKDIR /data

ENTRYPOINT ["/bin/bash", "-c"]



