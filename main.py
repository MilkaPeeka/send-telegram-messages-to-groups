"""
Sources:
https://stackoverflow.com/questions/34569662/can-telegram-bot-sends-message-to-group
https://stackoverflow.com/questions/32423837/telegram-bot-how-to-get-a-group-chat-id
- Using @botFather to create bot and get a token
"""
import asyncio
import aiohttp


async def get_chat_id(bot_token: str, chat_title: str, aiohttp_sess: aiohttp.ClientSession) -> int:
    async with aiohttp_sess.get(f"https://api.telegram.org/bot{bot_token}/getUpdates") as resp:
        json_resp = await resp.json()

    if json_resp['ok'] is not True:
        print("Error with getting result, please try again.")
        return -1

    for result in json_resp['result']:
        chat_res = result['my_chat_member']['chat']
        if chat_res['title'] == chat_title:
            return chat_res['id']

    print("Group chat not found. please try again and make sure the correct title is inserted. if error persists, "
          "please make sure you sent a message with the group with the bot. if it still doesn't work re-add the bot "
          "or turn the group into supergroup")
    return -1


async def send_message(bot_token: str, chat_id: int, message: str, aiohttp_sess: aiohttp.ClientSession) -> bool:
    payload = {"chat_id": chat_id, "text": message}
    async with aiohttp_sess.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", data=payload) as resp:
        resp = await resp.json()

    return resp['ok']


async def main():
    token = "XXX"
    async with aiohttp.ClientSession() as session:
        chat_id = await get_chat_id(token, "Trending TikToks announcements", session)
        status = await send_message(token, chat_id, "test that everything is working", session)


if __name__ == '__main__':
    asyncio.run(main())
