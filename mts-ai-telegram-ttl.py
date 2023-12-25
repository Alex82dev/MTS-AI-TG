import grpc
import json
import random
import os
import time

import requests
import telebot
import tts_pb2
import tts_pb2_grpc

TELEGRAM_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
TELEGRAM_CHAT_ID = 'YOUR_TELEGRAM_CHAT_ID'
GRPC_SERVER_ADDRESS = 'YOUR_GRPC_SERVER_ADDRESS'

def synthesize_text(text: str) -> bytes:
    request = tts_pb2.SynthesizeSpeechRequest(
        text=text,
        encoding=tts_pb2.AudioEncoding.LINEAR_PCM,
        sample_rate_hertz=22050,
        voice_name="gandzhaev",
        synthesize_options=tts_pb2.SynthesizeOptions(
            postprocessing_mode=tts_pb2.SynthesizeOptions.PostprocessingMode.POST_PROCESSING_DISABLE,
            model_type="default",
            voice_style=tts_pb2.VoiceStyle.VOICE_STYLE_NEUTRAL,
        ),
    )

    with grpc.insecure_channel(GRPC_SERVER_ADDRESS) as channel:
        stub = tts_pb2_grpc.TTSStub(channel)
        response = stub.Synthesize(request)

    return response.audio_content

def send_voice_message(bot: telebot.TeleBot, chat_id: int, audio_content: bytes):
    file_path = f'temp_audio_{random.randint(1000, 9999)}.wav'
    with open(file_path, 'wb') as f:
        f.write(audio_content)

    with open(file_path, 'rb') as f:
        bot.send_voice(chat_id=chat_id, voice=f)

    os.remove(file_path)

def handle_message(bot: telebot.TeleBot, update: telebot.types.Update):
    if update.message and update.message.text:
        text = update.message.text
        audio_content = synthesize_text(text)
        send_voice_message(bot, update.message.chat_id, audio_content)

bot = telebot.TeleBot(TELEGRAM_TOKEN)
bot.message_handler(Filters.text, handle_message)

while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        time.sleep(15)
        print(e)
