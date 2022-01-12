import discord
import requests 
import json
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
client = discord.Client()

def curl_request(message, user):

	headers = { 'Content-Type': 'application/json' }

	data = '{"sender": "'+ user +'","message": "'+ message +'","metadata": {}}'
	response = requests.post('http://localhost:5005/webhooks/rest/webhook', headers=headers, data=data)
	messages = json.loads(response.content)
	answer = list(map(lambda msg: msg['image'] if 'image' in msg else msg['text'], messages))

	return answer

@client.event
async def on_ready():
	print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_message(message):
	if message.author != client.user:

		answers = curl_request(message.content, str(message.author))

		end_response = " \n ".join((answers))

		return await message.channel.send(f'{message.author.mention} ' + end_response)

# Enter your token
client.run(token)