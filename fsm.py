from transitions.extensions import GraphMachine
from utils import send_text_message, send_flex_message, parse_question
import pygsheets

import os
from dotenv import load_dotenv

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)
        self.reset()
        load_dotenv()

    # conditions
    def start_test_word(self, event):
        text = event.message.text
        return text == "開始測驗"

    def end_of_question(self, event):
        question_set = self.question_set[self.question_count]
        options = [
            str(question_set[key]) 
            for key in question_set 
            if key != '題目' and question_set[key] != ''
        ]
        text = event.message.text
        if text in options:
            self.ans.append(text)  
            self.question_count += 1
            if self.question_count < len(self.question_set):
                self.next_question(event)
            else:
                wks_write = self.sh[1]
                data = [self.username, *self.ans]
                wks_write.append_table(data, start='A2')
                reply_token = event.reply_token
                send_text_message(reply_token, f'嗨，{self.username}\n你的答案是{self.ans}')
                self.reset()
                self.go_back(event)
        else: 
            reply_token = event.reply_token
            send_text_message(reply_token, "沒有這個選項")

    # states
    def on_enter_name(self, event):
        print('-----enter name')
        reply_token = event.reply_token
        send_text_message(reply_token, "請輸入你的名字")

    def on_exit_name(self, event):
        print('*****exit name')
        text = event.message.text
        self.username = text

    def on_enter_questions(self, event):
        print(f'-----enter question {self.question_count}')
        reply_token = event.reply_token
        content = parse_question(self.question_set[self.question_count], self.question_count+1)
        send_flex_message(
            reply_token, 
            content
        )
    
    def on_exit_questions(self, event):
        print(f'*****exit question {self.question_count}')      

    # other
    def reset(self):
        gc = pygsheets.authorize(service_account_file='./key.json')
        self.sh = gc.open_by_url(os.getenv("GOOGLE_DOC_URL", None))
        wks_read = self.sh[0]
        self.question_count = 0
        self.question_set = wks_read.get_all_records()
        self.username = ''
        self.ans = []
