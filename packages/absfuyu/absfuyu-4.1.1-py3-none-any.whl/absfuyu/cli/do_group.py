"""
ABSFUYU CLI
-----------
Do

Version: 1.3.1
Date updated: 01/02/2025 (dd/mm/yyyy)
"""

__all__ = ["do_group"]

import subprocess
from typing import Literal

import click

from absfuyu import __title__
from absfuyu.cli.color import COLOR
from absfuyu.core import __package_feature__
from absfuyu.general.human import Human2
from absfuyu.tools.checksum import Checksum
from absfuyu.util.zipped import Zipper
from absfuyu.version import PkgVersion


@click.command()
@click.option(
    "--force_update/--no-force-update",
    "-F/-f",
    "force_update",
    type=bool,
    default=True,
    show_default=True,
    help="Update the package",
)
def update(force_update: bool) -> None:
    """Update the package to latest version"""
    click.echo(f"{COLOR['green']}")
    AbsfuyuPackage = PkgVersion(
        package_name=__title__,
    )
    AbsfuyuPackage.check_for_update(force_update=force_update)


@click.command()
@click.argument("pkg", type=click.Choice(__package_feature__))
def install(pkg: str) -> None:
    """Install absfuyu's extension"""
    cmd = f"pip install -U absfuyu[{pkg}]".split()
    try:
        subprocess.run(cmd)
    except Exception:
        try:
            cmd2 = f"python -m pip install -U absfuyu[{pkg}]".split()
            subprocess.run(cmd2)
        except Exception:
            click.echo(f"{COLOR['red']}Unable to install absfuyu[{pkg}]")
        else:
            click.echo(f"{COLOR['green']}absfuyu[{pkg}] installed")
    else:
        click.echo(f"{COLOR['green']}absfuyu[{pkg}] installed")


@click.command()
def advice() -> None:
    """Give some recommendation when bored"""
    from absfuyu.fun import im_bored

    click.echo(f"{COLOR['green']}{im_bored()}")


@click.command(name="fs")
@click.argument("date", type=str)
@click.argument("number_string", type=str)
def fs(date: str, number_string: str) -> None:
    """Feng-shui W.I.P"""

    instance = Human2(date)
    print(instance.fs(number_string))


@click.command(name="info")
@click.argument("date", type=str)
def info(date: str) -> None:
    """Day info"""

    instance = Human2(date)
    print(instance.info())


@click.command(name="unzip")
@click.argument("dir", type=str)
def unzip_files_in_dir(dir: str) -> None:
    """Unzip every files in directory"""

    engine = Zipper(dir)
    engine.unzip()
    print("Done")


@click.command(name="checksum")
@click.argument("file_path", type=str)
@click.option(
    "--hashmode",
    "-m",
    "hash_mode",
    type=click.Choice(["md5", "sha1", "sha256", "sha512"]),
    default="sha256",
    show_default=True,
    help="Hash mode",
)
@click.option(
    "--save-result",
    "-s",
    "save_result",
    type=bool,
    default=False,
    is_flag=True,
    show_default=True,
    help="Save checksum result to file",
)
@click.option(
    "--recursive",
    "-r",
    "recursive_mode",
    type=bool,
    default=False,
    is_flag=True,
    show_default=True,
    help="Do checksum for every file in the folder (including child folder)",
)
@click.option(
    "--compare",
    "-c",
    "hash_to_compare",
    type=str,
    default=None,
    show_default=True,
    help="Hash to compare",
)
def file_checksum(
    file_path: str,
    hash_mode: str | Literal["md5", "sha1", "sha256", "sha512"],
    save_result: bool,
    recursive_mode: bool,
    hash_to_compare: str,
) -> None:
    """Checksum for file"""
    # print(hash_mode, save_result, recursive_mode)
    instance = Checksum(file_path, hash_mode=hash_mode, save_result_to_file=save_result)
    res = instance.checksum(recursive=recursive_mode)
    if hash_to_compare:
        print(res == hash_to_compare)
    else:
        print(res)


@click.group(name="do")
def do_group() -> None:
    """Perform functionalities"""
    pass


do_group.add_command(update)
do_group.add_command(install)
do_group.add_command(advice)
do_group.add_command(fs)
do_group.add_command(info)
do_group.add_command(unzip_files_in_dir)
do_group.add_command(file_checksum)
