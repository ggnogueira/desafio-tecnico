FROM apache/airflow:slim-2.7.3
COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
USER root
RUN apt-get update && apt-get install -y \
   openjdk-11-jdk
USER airflow
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
RUN export PATH=$PATH:$JAVA_HOME/bin

CMD [ "airflow", "standalone", "--port", "8080" ]
