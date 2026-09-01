# Telegram bot deployment on PS.kz

This procedure deploys only the Telegram polling process. FastAPI is not
required by the bot.

## First deployment

Run administrative commands as root. Replace `<release-ref>` with the reviewed
commit or release tag. Never put the Telegram token in a command line, Git, or
the systemd unit.

```bash
getent group medsalarybot >/dev/null || groupadd --system medsalarybot
getent passwd medsalarybot >/dev/null || useradd --system \
  --gid medsalarybot --no-create-home --home-dir /nonexistent \
  --shell /usr/sbin/nologin medsalarybot
install -d -o root -g medsalarybot -m 0750 \
  /opt/projects/med-salary-bot-kz
git clone <repository-url> /opt/projects/med-salary-bot-kz
cd /opt/projects/med-salary-bot-kz
git checkout <release-ref>
python3.12 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements.txt
chown -R root:medsalarybot /opt/projects/med-salary-bot-kz
```

Create the secret file without printing its contents:

```bash
install -d -o root -g medsalarybot -m 0750 /etc/med-salary-bot
install -o root -g medsalarybot -m 0640 /dev/null /etc/med-salary-bot/bot.env
editor /etc/med-salary-bot/bot.env
```

The file must contain the variable named `TELEGRAM_TOKEN`. Do not commit or
copy this file into the project directory. Rotate the token before cutover: an
older environment file was tracked by Git, so removing it from the current tree
does not remove it from existing clones, Git history, or previously built
images.

`/opt/projects` is shared with Corpsite. It must already exist and this
procedure must not change its owner or mode. Only the
`/opt/projects/med-salary-bot-kz` child directory is managed here. systemd
creates the private `/run/med-salary-bot` runtime directory declared by
`RuntimeDirectory` when the service starts.

Install and validate the service:

```bash
install -o root -g root -m 0644 \
  deploy/systemd/med-salary-bot.service \
  /etc/systemd/system/med-salary-bot.service
systemd-analyze verify /etc/systemd/system/med-salary-bot.service
systemctl daemon-reload
systemctl enable med-salary-bot.service
```

Before cutover, run the offline checks as the service user:

```bash
sudo -u medsalarybot .venv/bin/python -m pytest -p no:cacheprovider -q
sudo -u medsalarybot .venv/bin/python run_smoke.py
```

## Cutover and verification

Only one polling process may use the token. Before rotating it, deploy the
reviewed bot revision with the `httpx`/`httpcore` log filtering to Beget. This
prevents Telegram request URLs from being written to its systemd journal after
the restart.

On Beget, edit `/var/www/med-salary-bot-kz/telegram_bot/.env` interactively and
set the newly rotated token. Do not print the file or place the value in a shell
command. Restart Beget and verify that it is active and answers one controlled
request using the new token:

```bash
systemctl restart med-salary-bot.service
systemctl is-active med-salary-bot.service
```

Install the same new token interactively in
`/etc/med-salary-bot/bot.env` on PS.kz, but do not start its service yet. Once
Beget has been verified, perform cutover in this order:

```bash
# Beget
systemctl stop med-salary-bot.service
systemctl is-active med-salary-bot.service

# PS.kz, only after Beget reports inactive
systemctl start med-salary-bot.service
systemctl is-active med-salary-bot.service
```

After PS.kz starts, inspect only normal service status and recent errors; never
print either environment file:

```bash
systemctl status med-salary-bot.service --no-pager
journalctl -u med-salary-bot.service --since=-5min --no-pager
```

Send one controlled Telegram calculation and verify the response. The runtime
snapshot is written to `/run/med-salary-bot/current_params.json`; it is
ephemeral, may be recreated after service restarts, and is not part of the
deployment tree.

## Update

Record the currently deployed commit before changing it:

```bash
cd /opt/projects/med-salary-bot-kz
git rev-parse HEAD
systemctl stop med-salary-bot.service
git fetch --prune
git checkout <new-release-ref>
.venv/bin/python -m pip install -r requirements.txt
sudo -u medsalarybot .venv/bin/python -m pytest -p no:cacheprovider -q
sudo -u medsalarybot .venv/bin/python run_smoke.py
systemctl start med-salary-bot.service
```

## Rollback

If verification fails because of the deployed revision, stop PS.kz and restore
the recorded commit:

```bash
systemctl stop med-salary-bot.service
cd /opt/projects/med-salary-bot-kz
git checkout <previous-release-ref>
.venv/bin/python -m pip install -r requirements.txt
systemctl start med-salary-bot.service
```

If PS.kz cannot be recovered quickly, roll back traffic in this strict order.
Beget already has the same new token from the pre-cutover verification:

```bash
# PS.kz
systemctl stop med-salary-bot.service
systemctl is-active med-salary-bot.service

# Beget, only after PS.kz reports inactive
systemctl start med-salary-bot.service
systemctl is-active med-salary-bot.service
```

Never run both polling services at the same time. Never print the token in a
terminal, journal, document, Git file, or process command line.
