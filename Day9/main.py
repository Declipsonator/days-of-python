import requests

discord_token = "PUT YOUR DISCORD BOT TOKEN HERE"
discord_channel_id = "PUT YOUR DISCORD CHANNEL ID HERE"
after_message_id = "PUT THE MESSAGE ID WHERE YOU WANT TO START DOWNLOADING MESSAGES FROM HERE"


def download_messages(token, channel_id, after_message, limit=100, author_id=None):
    """
    :param after_message: where to start downloading messages, message id
    :param author_id: Discord user id
    :param token: Discord bot token
    :param channel_id: Discord channel id
    :param limit: How many messages to download at a time
    :return: dict array of messages
    """
    messages = []

    while True:
        url = f"https://discordapp.com/api/v6/channels/{channel_id}/messages?limit={limit}&after={after_message}"
        headers = {
            "Authorization": f"{token}"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            response = response.json()
            response = response[::-1]
            if author_id:
                response = [message for message in response if message["author"]["id"] == author_id]
            if len(response) == 0:
                break
            for message in response:
                messages.append({"author_id": message["author"]["id"], "content": message["content"]})
                print(message["content"])
            after_message = response[-1]["id"]
        else:
            print(f"Error: {response.status_code}")
            break


print(download_messages(discord_token, discord_channel_id, after_message_id))
