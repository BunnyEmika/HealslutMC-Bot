import disnake
import datetime

# Embed Builder
def embed_builder(title, description=None, author=None, footer=None, thumbnail=None):
    embed = disnake.Embed(title=title, description=description, color=disnake.Color.purple(), timestamp=datetime.datetime.now())
    if author != None:
        if hasattr(author, '.name'):
            embed.set_author(name=f"Search by {author.name}", icon_url=author.avatar)
        else:
            embed.set_author(name=f"Update from {author}")
    return embed