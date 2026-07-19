FROM python:3.13-alpine AS content-builder

WORKDIR /app
COPY src/ src/
COPY scripts/ scripts/
COPY public/ public/
RUN python scripts/build_bazi.py

FROM nginx:1.27-alpine

ENV PORT=8080

COPY --from=content-builder /app/public/ /usr/share/nginx/html/
COPY nginx/default.conf.template /etc/nginx/templates/default.conf.template

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 CMD wget -qO- "http://127.0.0.1:${PORT}/healthz" >/dev/null || exit 1
