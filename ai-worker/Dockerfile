# renovate: datasource=docker depName=nvidia/cuda
FROM nvidia/cuda:12.4.1-runtime-ubuntu22.04@sha256:517da2300c184c9999ec203c2665244bdebd3578d12fcc7065e83667932643d9

ENV DEBIAN_FRONTEND=noninteractive \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

RUN apt-get update \
 && apt-get install -y --no-install-recommends python3 python3-pip \
 && apt-get upgrade -y \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp/requirements.txt
RUN python3 -m pip install --require-hashes -r /tmp/requirements.txt
RUN useradd --system --uid 65532 --create-home appuser
USER 65532:65532
