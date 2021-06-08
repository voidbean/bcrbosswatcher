import json
import os
import hoshino
import asyncio
from hoshino import Service, priv
from hoshino.typing import CQEvent
from hoshino.modules.priconne.news.spider import BaseSpider
from hoshino import aiorequests
from nonebot import MessageSegment
import aiohttp
import asyncio

sv = Service('bosswatcher', enable_on_default=False)

cookie_str = "这里填写cookie"

boss_daily_report_url = "https://www.bigfun.cn/api/feweb?target=gzlj-clan-day-report-collect%2Fa"

cache_boss_info = {}

async def get_boss_status():
    cookies = {}
    for cookie in cookie_str.strip().split('; '):
        cookies[cookie.split('=')[0]] = cookie.split('=')[1]
    async with aiohttp.ClientSession(cookies=cookies) as session:
        async with session.get(boss_daily_report_url) as resp:
            result = await resp.json()
            return result['data']['boss_info']

@sv.on_prefix("boss状态")
async def returnboss(bot, ev):
    boss_info = await get_boss_status()
    msg = f'当前boss为{boss_info["lap_num"]}周目boss{boss_info["name"]}, 目前剩余{boss_info["current_life"]}HP'
    await bot.send(ev, msg)

@sv.scheduled_job('cron', minute='*/3', second='30', jitter=20)
async def search():
    boss_info = await get_boss_status()
    if 'name' not in cache_boss_info:
        cache_boss_info['name'] = boss_info['name']
        cache_boss_info['lap_num'] = boss_info['lap_num']
        print(f'初始化boss已切换至{cache_boss_info["lap_num"]}周目boss{cache_boss_info["name"]}')
    elif boss_info['name'] != cache_boss_info['name']:
        msg = f'当前boss已切换至{boss_info["lap_num"]}周目boss{boss_info["name"]}'
        print(msg)
        cache_boss_info['name'] = boss_info['name']
        cache_boss_info['lap_num'] = boss_info['lap_num']
        await sv.broadcast(msg, 'bosswatcher', 0)

if __name__ == "__main__":
    asyncio.run(search())
