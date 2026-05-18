import os
import subprocess
import webbrowser
from pathlib import Path
from typing import List, cast

import click
from nb_cli.i18n import _ as nb_cli_i18n
from pydantic import SecretStr, ValidationError
from noneprompt import Choice, ListPrompt, ConfirmPrompt, CancelledError
from nb_cli.cli import CLI_DEFAULT_STYLE, ClickAliasedGroup, run_sync, run_async

from nb_cli_plugin_webui.i18n import _
from nb_cli_plugin_webui.app.utils.security import salt
from nb_cli_plugin_webui.app.application import STATIC_PATH
from nb_cli_plugin_webui.app.handlers.project import PROJECT_DATA_PATH
from nb_cli_plugin_webui.app.config import CONFIG_FILE_PATH, Config, AppConfig
from nb_cli_plugin_webui.app.utils.string_utils import generate_complexity_string

from .token import token
from .config import config
from .docker import docker


async def _ensure_config():
    if CONFIG_FILE_PATH.exists():
        try:
            Config.load(CONFIG_FILE_PATH)
        except ValidationError:
            click.secho(_("Config file is broken, run `nb ui clear` to fix."), fg="red")
            raise
        return

    _salt = salt.gen_salt()
    _token = generate_complexity_string(use_digits=True, use_punctuation=True)
    default_config = AppConfig(
        base_dir=str(),
        host="localhost",
        port="12345",
        secret_key=SecretStr(
            generate_complexity_string(32, use_digits=True, use_punctuation=True)
        ),
        salt=SecretStr(_salt),
        hashed_token=SecretStr(salt.get_token_hash(_salt + _token)),
    )
    CONFIG_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE_PATH.write_text(default_config.to_json(), encoding="utf-8")
    Config.load(CONFIG_FILE_PATH)
    click.secho(_("Generated default config."), fg="green")
    click.secho(_("Access token: {token}").format(token=_token), fg="green")


@click.group(
    cls=ClickAliasedGroup, invoke_without_command=True, help=_("Start up NB CLI UI.")
)
@click.pass_context
@run_async
async def webui(ctx: click.Context):
    if ctx.invoked_subcommand is not None:
        return

    if not STATIC_PATH.exists():
        click.secho(
            _("WebUI dist directory not found, please reinstall to fix."), fg="red"
        )
        return

    await _ensure_config()

    command = cast(ClickAliasedGroup, ctx.command)

    choices: List[Choice[click.Command]] = list()
    for sub_cmd_name in await run_sync(command.list_commands)(ctx):
        if sub_cmd := await run_sync(command.get_command)(ctx, sub_cmd_name):
            choices.append(
                Choice(
                    sub_cmd.help
                    or nb_cli_i18n("Run subcommand {sub_cmd.name!r}").format(
                        sub_cmd=sub_cmd
                    ),
                    sub_cmd,
                )
            )

    try:
        result = await ListPrompt(
            nb_cli_i18n("What do you want to do?"), choices=choices
        ).prompt_async(style=CLI_DEFAULT_STYLE)
    except CancelledError:
        ctx.exit()

    sub_cmd = result.data
    await run_sync(ctx.invoke)(sub_cmd)


@webui.command(help=_("Run WebUI."))
@run_async
async def run():
    if not STATIC_PATH.exists():
        click.secho(
            _("WebUI dist directory not found, please reinstall to fix."), fg="red"
        )
        return

    await _ensure_config()

    from nb_cli_plugin_webui import server

    host = Config.host
    port = int(Config.port)

    try:
        webbrowser.open(f"http://{host}:{port}/")
    except webbrowser.Error:
        pass
    await server.run_server(host, port)


@webui.command(help=_("Run frontend dev server with backend."))
@run_async
async def dev():
    await _ensure_config()

    Config.debug = 1
    Config.enable_api_document = True

    frontend_path = Path(__file__).parent.parent.parent / "frontend"
    if not frontend_path.exists():
        click.secho(_("Frontend directory not found."), fg="red")
        return

    click.secho(_("Starting frontend dev server..."), fg="green")
    frontend_proc = subprocess.Popen(
        ["pnpm", "dev"],
        cwd=frontend_path,
    )

    click.secho(_("Starting backend server..."), fg="green")
    try:
        from nb_cli_plugin_webui import server

        await server.run_server(Config.host, int(Config.port), reload=True)
    finally:
        frontend_proc.terminate()
        frontend_proc.wait()


@webui.command(help=_("Clear WebUI data."))
@run_async
async def clear():
    clear_file = await ListPrompt(
        _("Which data do you want to clear?"),
        choices=[
            Choice(CONFIG_FILE_PATH.name, CONFIG_FILE_PATH),
            Choice(PROJECT_DATA_PATH.name, PROJECT_DATA_PATH),
        ],
    ).prompt_async(style=CLI_DEFAULT_STYLE)

    if not await ConfirmPrompt(_("Are you sure to clear?")).prompt_async(
        style=CLI_DEFAULT_STYLE
    ):
        return

    if not clear_file.data.exists():
        click.secho(_("File not found."), fg="yellow")
        return

    try:
        os.remove(clear_file.data)
    except Exception as e:
        click.secho(str(e), fg="red")
        return

    click.secho(_("File cleared."), fg="green")


webui.add_command(config)
webui.add_command(docker)
webui.add_command(token)
