from eda_bot.bot import Bot
from eda_bot.web import Web
from eda_bot import constants

def main() -> None:
    print('START')
    print(f'Bot: {constants.BOT}')
    
    try:
        Web().run()
        Bot().run()
    except Exception as e:
        print(e)

    print('START')