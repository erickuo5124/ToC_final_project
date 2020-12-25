import os

from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FlexSendMessage

channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)


def send_text_message(reply_token, text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))
    return "OK"

def send_flex_message(reply_token, contents):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(
        reply_token, 
        FlexSendMessage(alt_text='*問題*',contents=contents)
    )
    return "OK"

def parse_question(question_set, num):
    question = question_set['題目']
    options = [
        question_set[key] 
        for key in question_set 
        if key != '題目' and question_set[key] != ''
    ]
    options = [{
        "type": "button",
        "action": {
            "type": "message",
            "label": str(option),
            "text": str(option)
        }
    } for option in options
    ]
    data = {
        "type": "bubble",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": f'問題 {num}',
                "align": "center"
            }
            ]
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": question
            }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": options
        }
    }
    return data
"""
def send_image_url(id, img_url):
    pass

def send_button_message(id, text, buttons):
    pass
"""
