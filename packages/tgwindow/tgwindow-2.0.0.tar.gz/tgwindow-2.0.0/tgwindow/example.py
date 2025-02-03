from tgwindow.buttons import Inline, TextMessage
from tgwindow.static_window import StaticWindow
from tgwindow.wrapper import auto_window
from window_base import WindowBase


class D(StaticWindow):
    # Инициализируем Inline и текст в классе
    text = TextMessage(ru="Привет из TGWin", en="Hello from TGWin")
    button = Inline(ru="RU", en= "EN", callback_data="ru")
    button2 = Inline(ru="RUS",  en= "EN", callback_data="ru:")



class Hello(WindowBase):
    @auto_window
    def hello(self, lang):
        self.lang = lang
        self.photo = "AgACAgIAAxkBAAJaj2edTMZXRLk8rUBRyOyyeu9k_lwlAAJs8zEbWdroSA-XNyW_1svmAQADAgADeQADNgQ"
        self.add_window(D(lang))

    @auto_window
    def start(self, *args, **kwargs):
        self.add_window(D(self.lang))



if __name__ == '__main__':
    print(Hello().lang)
