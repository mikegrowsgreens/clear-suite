FROM caddy:alpine

# Copy Caddy config
COPY Caddyfile /etc/caddy/Caddyfile

# Copy landing page
COPY apps/landing/ /srv/landing/

# Copy individual apps (each gets its own service in production,
# but landing page references them by external domain)

EXPOSE ${PORT:-8080}
