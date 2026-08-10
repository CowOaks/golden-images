# renovate: datasource=docker depName=gcr.io/distroless/python3-debian12
FROM gcr.io/distroless/python3-debian12@sha256:2fdb05402a2cf21cf78fdb3ba4c5db167241e9e498140f5bf689d7efb773731f
COPY --chown=65532:65532 mcp_sidecar/ /app
COPY --chown=65532:65532 step-ca-client /usr/local/bin/step
USER 65532:65532
ENTRYPOINT ["python3", "/app/sidecar.py"]
