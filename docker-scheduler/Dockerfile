FROM continuumio/miniconda:latest

MAINTAINER helge.dzierzon@brockmann-consult.de

RUN mkdir /data
RUN conda init

WORKDIR /tmp
RUN git clone https://github.com/dcs4cop/xcube.git
RUN cd xcube; conda env create

ENTRYPOINT ["/bin/bash", "-c"]



