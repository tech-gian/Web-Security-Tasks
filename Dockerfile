FROM debian:latest

# install packages
RUN apt update
RUN apt install -y python3

RUN apt install -y python3-requests curl

# copy script inside container
COPY docker-run.sh /root/

# Copy python scripts to automate the tasks
COPY task_1.py /root/
COPY task_3.py /root/

# run when container starts
CMD ["bash", "/root/docker-run.sh"]
