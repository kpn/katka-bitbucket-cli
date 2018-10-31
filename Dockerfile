FROM python:3.6

ENV IN_DOCKER 1
ENV PYTHONUNBUFFERED 1
ENV PROJECT_ROOT /app

WORKDIR $PROJECT_ROOT

COPY . .
RUN make install_requirement_txt

CMD ["make", "test"]