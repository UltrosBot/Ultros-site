# coding=utf-8
import requests

from ultros_site.database.schema.news_post import NewsPost
from ultros_site.tasks.__main__ import app

__author__ = "Gareth Coles"


def notify_post(post: NewsPost, url: str):
    md = post.markdown
    md = md.replace("\n\n", "\r")
    md = md.replace("\n", "")
    md = md.replace("\r", "\n\n")

    discord_embed = {
        "title": post.title,
        "description": md,
        "url": "https://beta.ultros.io/news/{}".format(post.id),
        "author": {
            "name": post.user.username,
            "url": "https://beta.ultros.io/"
        }
    }

    app.send_task(
        "send_discord",
        args=[url, discord_embed]
    )


@app.task(name="send_discord")
def send_discord(hook_url: str, embed: None):
    if embed is None:
        embeds = []
    else:
        embeds = [embed]

    session = requests.session()
    return session.post(hook_url, json={
        "embeds": embeds
    })
