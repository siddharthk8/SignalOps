# Nginx

This directory contains the Nginx configuration template used by the containerized SignalOps deployment.

## Role

The outer Nginx instance acts as the public reverse proxy. It:

* Terminates HTTPS using Let's Encrypt certificates.
* Routes `/api/*` requests to the FastAPI backend.
* Routes all other requests to the frontend container.
* Serves the ACME HTTP-01 challenge path used by Certbot.

The frontend container has its own Nginx instance that serves the compiled React application.

## Files

* `default.conf.example` — sanitized reference configuration for the production reverse proxy.

The actual deployment configuration is maintained separately and may contain environment-specific values.

## Certificate Volumes

The production deployment mounts:

* `./certbot/www` → `/var/www/certbot` for ACME challenges.
* `./certbot/letsencrypt` → `/etc/letsencrypt` for TLS certificates.

## Notes

When changing the reverse-proxy configuration, keep the Nginx upstreams, API routing, frontend port, domain, and certificate paths aligned with the Docker Compose deployment.
