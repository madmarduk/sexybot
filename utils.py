import functools
import disnake


def log_error(coro):
    @functools.wraps(coro)
    async def wrapper(self, ctx, *args, **kwargs):
        try:
            print(self, ctx, args, kwargs)
            return await coro(self, ctx, *args, **kwargs)
        except Exception as ex:
            print(ex)
            embed = disnake.Embed(
                title="Error",
                description="Error has occured!\nMaybe server was offline",
                color=0xFF2E2E,
            )
            await ctx.send(embed=embed)

    return wrapper


def players(num: int) -> str:
    if num == 1:
        player = "player"
    else:
        player = "players"

    return f"{num} {player}"
