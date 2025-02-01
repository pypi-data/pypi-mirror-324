# matrix-webhook-bot

Matrix bot for creating webhook endpoints and sending webhook messages to matrix rooms

- simple webservice that forwards webhook messages after formatting
- simple jinja template can be used format messages
- webhook url creation and deletion through controll room
- creates controll and output room on startup

Configuration

Either by config.ini or env variables. Env variables take precedence.
Rename sample_config.ini to config.ini and set every config value.

Running

Python packages are handled by uv, but if you prefer, look into pyproject.toml and install dependencies yourself.

```
git clone https://github.com/hidraulicChicken/matrix-webhook-bot.git
cd matrix-webhook-bot
curl -LsSf https://astral.sh/uv/install.sh | sh

```

