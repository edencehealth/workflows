FROM python:3-alpine
LABEL maintainer="edenceHealth NV <info@edence.health>"

COPY requirements.txt /

RUN set -eux; \
  apk add --no-cache --virtual build-dependencies \
    gcc \
    musl-dev \
  ; \
  pip install --upgrade pip; \
  pip install -r /requirements.txt; \
  pip cache purge; \
  apk del build-dependencies;

COPY main.py /app/

WORKDIR /work

ARG NONROOT_GID=65532
ARG NONROOT_UID=65532
RUN set -ex; \
  addgroup \
    -g ${NONROOT_GID} \
    nonroot \
  ; \
  adduser \
    -h /work \
    -u ${NONROOT_UID} \
    -G nonroot \
    -D \
    nonroot \
  ;
USER nonroot

ENTRYPOINT ["/app/main.py"]
