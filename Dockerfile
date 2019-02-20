FROM python:2.7

ENV DEBIAN_FRONTEND noninteractive

ENV PYTHONPATH=/app

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

RUN apt-get update \
	&& apt-get upgrade -y \
    && apt-get install -y \
    curl \
    gnupg \
    && curl -sL https://deb.nodesource.com/setup_10.x | bash - \
    && apt-get install -y nodejs \
    && npm install -g grunt-cli

# Download and install wkhtmltopdf
RUN apt-get install -y build-essential xorg libssl-dev libxrender-dev wget

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends xvfb libfontconfig 

RUN wget --no-check-certificate https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.4/wkhtmltox-0.12.4_linux-generic-amd64.tar.xz
RUN tar vxf wkhtmltox-0.12.4_linux-generic-amd64.tar.xz 
RUN cp wkhtmltox/bin/wk* /usr/local/bin/
RUN rm -rf wkhtmltox
RUN rm wkhtmltox-0.12.4_linux-generic-amd64.tar.xz

RUN apt-get install -y locales locales-all

RUN apt-get install -y pdftk

CMD ["/bin/bash"]
