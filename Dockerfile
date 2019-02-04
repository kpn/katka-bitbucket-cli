FROM python:3.7.1

ENV IN_DOCKER 1
ENV PYTHONUNBUFFERED 1
ENV PROJECT_ROOT /app

WORKDIR $PROJECT_ROOT

COPY requirements.txt requirements.txt
COPY requirements requirements
COPY Makefile Makefile
RUN make install_requirement_txt

COPY . .

CMD ["make", "test"]