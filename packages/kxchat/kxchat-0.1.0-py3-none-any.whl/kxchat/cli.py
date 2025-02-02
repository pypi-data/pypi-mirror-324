import click

from kxchat.scripts.chat import start_chat_room


@click.group(chain=True)
def main():
    pass


@main.command("room")
@click.argument("repo", type=str)
@click.option("-r", "--revision", type=str, default="main")
def room(repo: str, revision: str):
    start_chat_room(repo=repo, revision=revision)
