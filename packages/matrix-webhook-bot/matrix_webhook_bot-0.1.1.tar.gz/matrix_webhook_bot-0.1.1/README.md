# matrix-webhook-bot

Matrix bot for creating webhook endpoints and sending webhook messages to matrix rooms

- simple webservice that forwards webhook messages after formatting
- simple jinja template can be used to format messages
- webhook url creation and deletion through controll room
- creates controll and output room on startup

## Configuration

Either by config.ini or env variables. Env variables take precedence.
Rename sample_config.ini to config.ini and set every config value.

| Environment variable   | Config file name  | Example value  |
|---|---|---|
| HOMESERVER_URL | homeserver_url | https://matrix.domain.com |
| ADMIN_USER | admin_user | @admin:matrix.domain.com |
| BOT_USER | bot_user | @webhook:matrix.domain.com |
| TOKEN | token | syt_d2VgfG9eqr_dbvTrKgfDerOdseFMZNP_0z99KM |
| DEVICE_ID | device_id | AABBCCDDEE |

## Install/Run

Only if you run it non virtualized.
You need python ">=3.13"

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install matrix-webhook-bot
matrix-webhook-bot
```

## Docker

```bash
docker run -d --rm \
  --name matrix-webhook-bot \
  -v /on/host/bot/config:/app/config \
  -p 8228:8228 \
  ghcr.io/hidraulicchicken/matrix-webhook-bot
```

## Controll room commands

| Command   | Explanation |
|---|---|
| !webhook help | Show help message |
| !webhook list | List all webhooks |
| !webhook add [name] | Add a webhook with given name |
| !webhook remove [name] | Remove webhook with given name |

## Development

Python packages are handled by uv, but if you prefer, look into pyproject.toml and install dependencies yourself.

```bash
git clone https://github.com/hidraulicChicken/matrix-webhook-bot.git
cd matrix-webhook-bot
curl -LsSf https://astral.sh/uv/install.sh | sh
uv venv --python 3.13.0
uv pip install -e .
```

## Contribution

If you have jinja template for certain services webhooks, let me know in the issues page.
