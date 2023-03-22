import json
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True

intents = discord.Intents().all()
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

async def get_nft_info(ctx, rarity_id_int):
    with open('rarity.txt') as f:
        for line in f:
            if f"Scientist Goblin #{rarity_id_int}" in line:
                rank = line.split()[0][:-1]  # Remove trailing period
                break
        else:
            await ctx.send(f'ID {rarity_id_int} not found in rarity.txt')
            return

    with open('metadata.json') as f:
        metadata = json.load(f)
        for item in metadata:
            if f"Scientist Goblin #{rarity_id_int}" == item["meta"]["name"]:
                txid = item["id"]
                break
        else:
            await ctx.send(f"ID {rarity_id_int} not found in metadata.json")
            return

    url = f"https://ord.ordscan.xyz/inscription/{txid}"

    # Create an embed object and set its properties
    embed = discord.Embed(
        title=f"Scientist Goblin #{rarity_id_int}",
        description=f"Rank: {rank}\n[View on ordinals]({url})",
        color=0x0099FF
    )

    # Set the image of the embed using the URL of the image
    embed.set_image(url=f"https://ord.ordscan.xyz/content/{txid}")

    # Send the embed to the channel
    await ctx.send(embed=embed)

@bot.command(name='rarity')
async def rarity(ctx, rarity_id: str):
    try:
        # Remove the '#' symbol if present
        if rarity_id.startswith('#'):
            rarity_id = rarity_id[1:]

        # Convert the argument to an integer
        rarity_id_int = int(rarity_id)

        await get_nft_info(ctx, rarity_id_int)
    except ValueError:
        # Send an error message if the argument cannot be converted to an integer
        await ctx.send('Invalid ID. Please provide a valid integer ID.')

@bot.command()
async def rank(ctx, rank: int):
    try:
        with open('rarity.txt') as f:
            for i, line in enumerate(f, start=1):
                if i == rank:
                    rarity_id_int = int(line.split()[3][1:])
                    break
            else:
                await ctx.send(f'Rank {rank} not found in rarity.txt')
                return

        await get_nft_info(ctx, rarity_id_int)
    except ValueError:
        await ctx.send('Invalid rank. Please provide a valid integer rank.')

bot.run('MTA4Nzg4OTI5MjkyOTU0NDMxMg.G-Z3IW.fu8t7ue_48QTw2-kaxaTvsb-V1qNgg_BYSdFWc')