FROM continuumio/miniconda:latest

MAINTAINER helge.dzierzon@brockmann-consult.de

RUN conda init

WORKDIR /tmp
RUN git clone https://github.com/dcs4cop/xcube.git
RUN cd xcube; conda env create

RUN groupadd -g 1000 ubuntu
RUN useradd -u 1000 -g 1000 -ms /bin/bash ubuntu
USER ubuntu
WORKDIR /home/ubuntu

ENTRYPOINT ["/bin/bash", "-c"]



