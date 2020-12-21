from transitions.extensions import GraphMachine

from utils import send_text_message


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)
        self.question_num = 0
        self.questionaire = ['test1', 'test2', 'test3']
        self.username = ''

    # conditions
    def start_test_word(self, event):
        text = event.message.text
        return text == "開始測驗"

    # states
    def on_enter_name(self, event):
        print('enter name')
        reply_token = event.reply_token
        send_text_message(reply_token, "請輸入你的名字")

    def on_exit_name(self, event):
        print('exit name')
        text = event.message.text
        self.username = text
        # reply_token = event.reply_token
        # send_text_message(reply_token, f'嗨，{self.username}')

    def on_enter_questions(self, event):
        print(f'enter question{self.question_num}')
        reply_token = event.reply_token
        send_text_message(reply_token, self.questionaire[self.question_num])
        self.question_num += 1
        if self.question_num < len(self.questionaire):
            self.next_question(event)
        else:
            self.go_back(event)

    # def on_exit_questions(self, event):
    #     text = event.message.text
    #     reply_token = event.reply_token
    #     send_text_message(reply_token, f'你的答案是 {text}')

    def on_enter_user(self, event):
        self.question_num = 0
        self.username = ''
        reply_token = event.reply_token
        send_text_message(reply_token, "重新開始測驗")
