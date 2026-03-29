FROM caddy:alpine

COPY Caddyfile /etc/caddy/Caddyfile
COPY . /srv/

EXPOSE ${PORT:-8080}
