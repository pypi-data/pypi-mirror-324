# Configuration

Let's assume that cattle grid is running on its own domain
`cattlegrid.yourdomain.example`. Then you can give the
cattle grid actor the id `https://cattlegrid.yourdomain.example/actor`.

!!! info
    For how to use cattle_grid together with an application, see
    [the corresponding bovine_herd tutorial](https://bovine-herd.readthedocs.io/en/latest/tutorials/cattle_grid/).

## Setting up cattle grid

First cattle_grid can be installed from [PyPI](https://pypi.org/project/cattle-grid/) via

```bash
pip install cattle-grid
```

Then one can create the configuration file (including generating public and private keys)
using

```bash
python -mcattle_grid.auth.config
```

where you have to enter an actor id, We assume for this that you use
`https://cattlegrid.yourdomain.example/actor`.  The details for this
command are

<!-- ::: mkdocs-click
    :module: cattle_grid.auth.config
    :command: create_config
    :prog_name: python -m cattle_grid.auth.config
    :depth: 3 -->

The configuration is stored in the `cattle_grid.toml`. The details of
the config object are available [here][cattle_grid.config.auth.AuthConfig].

We furthermore, recommend that
you set up a [blocklist](blocking.md) using for example Seirdy's FediNuke by
running

```bash
python -mcattle_grid.auth.block
```

You can now run cattle_grid via

```bash
uvicorn --factory cattle_grid:create_app --uds /tmp/cattle_grid.sock
```

## systemd unit

To run cattle_grid as a systemd service, the unit file would look like

```systemd title="/etc/systemd/system/cattle_grid.service"
[Unit]
Description=cattle grid
After=network.target

[Service]
User=cattle_grid
Group=cattle_grid
Restart=always
Type=simple
WorkingDirectory=/opt/cattle_grid
ExecStart=uvicorn --factory cattle_grid:create_app --uds /tmp/cattle_grid.sock

[Install]
WantedBy=multi-user.target
```

## nginx configuration for cattle_grid's server

If you are running cattle_grid on the domain mentioned above,
the nginx configuration would look like:

```nginx
server {
    listen 80;
    server_name cattlegrid.yourdomain.example;

    location /auth {
        return 401;
    }

    location / {
        proxy_pass http://unix:/tmp/cattle_grid.sock;
    }
}
```

The above snippet skips details such as configuring SSL. We do not need to add any
additional headers to the requests to `/` as `cattle_grid` does not check signatures
for requests to its actor. See [here](https://funfedi.dev/testing_tools/technical_notes/public_key_fetching/#claire-requiring-signatures-for-get) for a sequence diagram
why this is necessary.

## nginx configuration for your application

For details of what this configuration does, see [request flow](request_flow.md).
The simplest example of a configuration is

```nginx title="/etc/nginx/conf.d/your_application.conf"
server {
    listen 80 default_server;

    location / {
        auth_request /auth;
        auth_request_set $requester $upstream_http_x_cattle_grid_requester;

        proxy_pass http://your_application;
        proxy_set_header X-Cattle-Grid-Requester $requester;
    }

    location = /auth {
        internal;
        proxy_pass http://unix:/tmp/cattle_grid.sock;
        proxy_pass_request_body off;
        proxy_set_header X-Original-URI $request_uri;
        proxy_set_header X-Original-Method $request_method;
        proxy_set_header X-Original-Host $host;
        proxy_set_header X-Original-Port $server_port;
    }
}
```

This will lead to all correctly signed requests having the `X-Cattle-Grid-Requester`
header containing the requester. If there is no signature, this header is empty.
If the request is rejected either due to having an invalid signature (401) or
being blocked (403), your application does not see the request.

<!-- ::: cattle_grid.auth.config -->
