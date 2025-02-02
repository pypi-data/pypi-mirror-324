from __future__ import annotations

import logging
import os
import subprocess
import time

import click

from tobikodata.tcloud.config import load_project_config
from tobikodata.tcloud.installer import install_executors

EXECUTOR_MIN_INTERVAL_BETWEEN_RUNS_SEC = 5.0


@click.command()
@click.argument("executor_type", required=True, type=click.Choice(["run", "apply"]))
@click.option(
    "--once",
    is_flag=True,
    help="Runs the executor once and exit.",
)
@click.pass_context
def executor(ctx: click.Context, executor_type: str, once: bool) -> None:
    """Run the Tobiko Cloud executor"""
    logging.basicConfig(
        format="%(asctime)s - %(threadName)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)",
        level=logging.INFO,
    )

    project = ctx.obj["project"]
    project_config = load_project_config(project)

    def install_and_run() -> None:
        try:
            executors_bin_path = install_executors(project_config)
        except Exception as ex:
            raise click.ClickException(f"Failed to install the executor bin package: {ex}")
        assert project_config.token
        subprocess.run(
            [executors_bin_path, executor_type],
            stdout=None,
            stderr=None,
            env={
                **os.environ,
                "TCLOUD_URL": project_config.url,
                "TCLOUD_TOKEN": project_config.token,
            },
        )

    if once:
        install_and_run()
    else:
        while True:
            run_start_ts = time.monotonic()
            install_and_run()
            elapsed_sec = time.monotonic() - run_start_ts
            if elapsed_sec < EXECUTOR_MIN_INTERVAL_BETWEEN_RUNS_SEC:
                time.sleep(EXECUTOR_MIN_INTERVAL_BETWEEN_RUNS_SEC - elapsed_sec)
