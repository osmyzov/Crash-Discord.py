# osmuzov
# Crash Gambling v. 2.072021

import math
import random

import discord
from discord.ext import commands


class Crash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def crash(self, ctx, bet: int = None, coef: float = None):
        if bet is None:
            await ctx.send(f"{ctx.author.name}, Укажи сумму!")

        elif coef is None:
            await ctx.send(f"{ctx.author.name}, Укажи коэффициент!")

        elif coef <= 1:
            await ctx.send(f"{ctx.author.name}, Коэффициент должен быть выше 1x!")

        else:
            coef = round(coef, 2)
            cash = 0  # баланс участника из базы данных
            if cash < bet:
                await ctx.send(f"{ctx.author.name}, У тебя недостаточно денег!")

            else:
                # ограничение по беттингу (10/100000)
                if bet < 10:
                    await ctx.send("Минимальная ставка 10 монет!")
                elif bet > 100000:
                    await ctx.send("Максимальная ставка 100000 монет!")

                else:
                    # Для генерации результата в режиме Crash требуется 1 случайное число в интервале (0..1),
                    # которое затем переводится в коэффициент Crash, имеющий экспоненциальное распределение,
                    # по следующему алгоритму.
                    number = random.uniform(0, 1)
                    crashOutcome = 1000000 / (math.floor(number * 1000000) + 1) * (1 - 0.05)

                    # Иногда может выпасть число по типу 0.99 или меньше, в самой игре такого нет,
                    # этот IF спасает от таких ситуации.
                    if crashOutcome <= 1:
                        crashOutcome = 1.00

                    # если коэф пользователя выше или равен крашу, то он выиграл
                    if crashOutcome >= coef:
                        winCash = bet * coef - bet
                        roundWinCash = round(winCash)
                        await ctx.send(content=ctx.author.mention,
                                       embed=discord.Embed(
                                           title="📈 Сломанный Краш",
                                           description=f"{ctx.author.name}, "
                                                       f""f"ты выиграл: **+{round(roundWinCash)} :dollar:**\n\n"
                                                       f"Коэф: **{round(crashOutcome, 2)}**\n"
                                                       f"Ты поставил на коэф: **{round(coef, 2)}**\n"
                                                       f"Твоя ставка: **{bet}**"))

                        # Тут уже входит в силу ваша база данных.
                        # переменная roundWinCash, это выигрыш пользователя.

                    # или проиграл :(
                    else:
                        await ctx.send(content=ctx.author.mention,
                                       embed=discord.Embed(
                                           title="📈 Сломанный Краш",
                                           description=f"{ctx.author.name}, "
                                                       f"ты проиграл: **{bet} :dollar:**\n\n"
                                                       f"Коэф: **{round(crashOutcome, 2)}**\n"
                                                       f"Ты поставил на коэф: **{round(coef, 2)}**\n"
                                                       f"Твоя ставка: **{bet}**"))

                        # Тут уже входит в силу ваша база данных.
                        # тут вы должны снять с баланса пользователя его ставку


def setup(bot):
    bot.add_cog(Crash(bot))
