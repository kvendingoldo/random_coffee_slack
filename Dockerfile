FROM python:3

#
# Create a base UID/GID and SUID/SGID which will be used by container
#
RUN groupadd --system --gid 1000 rcb \
 && useradd --system --gid rcb --uid 1000 --shell /bin/bash --create-home rcb \
 && mkdir -p /run/user/1000 \
 && chown -R rcb /run/user/1000 /home/rcb \
 && echo rcb:100000:65536 | tee /etc/subuid | tee /etc/subgid
USER 1000:1000
ENV HOME /home/rcb
ENV USER rcb
ENV XDG_RUNTIME_DIR=/run/user/1000

RUN mkdir -p ${HOME}/bot
COPY requirements.txt ${HOME}/bot
RUN pip3 install --upgrade pip \
 && pip3 install --no-cache-dir -r ${HOME}/bot/requirements.txt

COPY ./src ${HOME}/bot/src
COPY ./resources ${HOME}/bot/resources

WORKDIR ${HOME}/bot/src

ENTRYPOINT ["python3", "main.py"]
