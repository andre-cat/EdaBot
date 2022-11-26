from telegram.ext.updater import Updater as TUpdater
from telegram.ext.dispatcher import Dispatcher as TDispatcher
from telegram.ext.callbackcontext import CallbackContext as TCallbackContext
from telegram.ext.commandhandler import CommandHandler as TCommandHandler
from telegram.ext.messagehandler import MessageHandler as TMessageHandler
from telegram.ext.filters import Filters as TFilters
from telegram.update import Update as TUpdate
from telegram import Bot as TBot
from eda_bot import constants
from eda_bot import commons
from eda_bot import titanic
import matplotlib.pyplot as pp  # type: ignore
import matplotlib as mp  # type: ignore
import pandas as pd  # type: ignore
import seaborn as sb  # type: ignore
import time

sb.set_style(style='whitegrid')
sb.set_context(context='notebook')
pp.rcParams['figure.figsize'] = (10, 7)

class Bot:

    def __new__(cls) -> 'Bot':
        if not hasattr(cls, 'instance'):
            cls.__instance: 'Bot' = super(Bot, cls).__new__(cls)
            cls.__isawait: bool = False
            cls.__com: str = ''
            cls.__data: pd.DataFrame = pd.DataFrame()
            cls.__vari: str = ''
            cls.__varu: str = ''
            cls.__varb: list = ['', '']
            cls.__varm: list = []
        return cls.__instance

    def run(cls) -> None:

        mp.use('agg')

        def start(update: TUpdate, context: TCallbackContext) -> None:
            cls.__com = start.__name__
            update.message.reply_text('\U0001F916')
            update.message.reply_text(
                text='Hello!\n'
                'Welcome to this EDA bot!'
                'How can I help you?\n'
                '`Press` /help `to see the commands available.`', parse_mode='Markdown')

        def help(update: TUpdate, context: TCallbackContext) -> None:
            cls.__com = help.__name__
            update.message.reply_text(
                'Select one option:\n'
                '*/data* - Set up dataset link. \U0001F517\n'
                '*/vars* - See dataset variables. \U0001f9ec\n'
                '*/info* - See variable info. \U0001F50E\n'
                '*/uvar* - Get univariate graph. \U0001f4ca\n'
                '*/bvar* - Get bivariate graph. \U0001f4c8\n'
                '*/mvar* - Get multivariate graph. \U0001F9E0\n', parse_mode='Markdown'
            )

        def data(update: TUpdate, context: TCallbackContext) -> None:
            cls.__com = data.__name__

            if type(context.args) == list:
                if len(context.args) == 0:
                    cls.__isawait = True
                    update.message.reply_text('_Enter a dataset .csv link or use /tita to select the default one:_', parse_mode='Markdown')
                else:
                    set_data(update, context, context.args[0])

        def vars(update: TUpdate, context: TCallbackContext) -> None:
            cls.__com = vars.__name__
            if cls.__data.empty:
                send_warn_message(update, 'First, enter a dataset with /data command')
            else:
                update.message.reply_text('Dataset variables:')
                types: str = cls.__data.dtypes.to_string()
                update.message.reply_text(types)

        def info(update: TUpdate, context: TCallbackContext) -> None:
            cls.__com = info.__name__

            if cls.__data.empty:
                send_warn_message(update, 'First, enter a dataset with /data command')
            else:
                sucess: bool = True
                if (type(context.args) == list):
                    if len(context.args) != 0:
                        if cls.__vari != context.args[0]:
                            sucess = set_vari(update, context.args[0])

                if cls.__vari == '':
                    cls.__isawait = True
                    update.message.reply_text('_Enter the info variable:_', parse_mode='Markdown')
                elif sucess == True:
                    update.message.reply_text(f'Info about *{cls.__vari}*:', parse_mode='Markdown')
                    update.message.reply_text(cls.__data[cls.__vari.lower()].describe().to_string())
                    update.message.reply_text(f'For delete var *{cls.__vari}*, tap in __/deli__', parse_mode='Markdown')

        def uvar(update: TUpdate, context: TCallbackContext) -> None:
            cls.__com = uvar.__name__

            if cls.__data.empty:
                send_warn_message(update, 'First, enter a dataset with /data command.')
            else:
                sucess: bool = True
                if (type(context.args) == list):
                    if len(context.args) != 0:
                        if cls.__varu != context.args[0]:
                            sucess = set_varu(update, context.args[0])

                if cls.__varu == '':
                    cls.__isawait = True
                    update.message.reply_text('_Enter the variable (1) for univariate graph:_', parse_mode='Markdown')
                elif sucess == True:
                    update.message.reply_text(f'Univariate graph for {cls.__varu}:')
                    plot = sb.catplot(
                        data=cls.__data,
                        x=cls.__varu,
                        kind='count',
                        palette='PiYG').set(title=f'Frequency for "{cls.__varu}" var')
                    path = commons.get_path('eda_bot\\sources\\images','/plotu.png')
                    file = plot.savefig(path)
                    update.message.bot.send_photo(update.message.chat.id, open(path, 'rb'))
                    update.message.bot.send_document(update.message.chat.id, open(path, 'rb'))
                    update.message.reply_text(f'For delete var *{cls.__varu}*, tap in __/delu__', parse_mode='Markdown')

        def bvar(update: TUpdate, context: TCallbackContext) -> None:
            cls.__com = bvar.__name__

            if cls.__data.empty:
                send_warn_message(update, 'First, enter a dataset with /data command.')
            else:
                sucess: bool = True
                if (type(context.args) == list):
                    if len(context.args) != 0:
                        if cls.__varb[0] != context.args[0] and cls.__varb[1] != context.args[1]:
                            sucess = set_varb(update, " ".join(map(str, context.args)))

                if cls.__varb[0] == '' or cls.__varb[1] == '':
                    cls.__isawait = True
                    update.message.reply_text('_Enter the variables (2) for bivariate graph:_', parse_mode='Markdown')
                elif sucess == True:
                    update.message.reply_text(f'Bivariate graph for *{cls.__varb[0]}* and *{cls.__varb[1]}*:',parse_mode='Markdown')

                    type_1: str = str(cls.__data[cls.__varb[0]].dtype).replace('object', 'str').replace('int64', 'num').replace('float64', 'num')
                    type_2: str = str(cls.__data[cls.__varb[1]].dtype).replace('object', 'str').replace('int64', 'num').replace('float64', 'num')

                    plot: sb.objects.Plot = None
                    if type_1 == 'num' and type_2 == 'num':
                        plot = sb.scatterplot(
                            data=cls.__data,
                            x=cls.__varb[0],
                            y=cls.__varb[1]
                        ).figure
                    elif type_1 == 'str' and type_2 == 'str':
                        send_fail_message(update, 'Is needed at least one numeric variable')
                        delb(update, context)
                    else:
                        plot = sb.boxplot(
                            data=cls.__data,
                            x=cls.__varb[0],
                            y=cls.__varb[1]
                        ).figure

                    path = commons.get_path('eda_bot\\sources\\images','plotb.png')

                    file = plot.savefig(path)
                    update.message.bot.send_photo(update.message.chat.id, open(path, 'rb'))
                    update.message.bot.send_document(update.message.chat.id, open(path, 'rb'))
                    update.message.reply_text(f'For delete vars *{cls.__varb[0]}* and *{cls.__varb[1]}*, tap in __/delb__', parse_mode='Markdown')

        def mvar(update: TUpdate, context: TCallbackContext) -> None:
            cls.__com = mvar.__name__
            update.message.reply_text(f'Not yed... \U0001F334')

        # Setters:
        def set_data(update: TUpdate, context: TCallbackContext, link: str) -> None:
            try:
                data = pd.read_csv(link)
                data = data.rename(columns=str.lower)
                cls.__data = data
                send_succ_message(update, 'Dataset set up')
                help(update, context)
            except Exception as e:
                send_fail_message(update, '\.csv not found')

        def set_vari(update: TUpdate, var: str) -> bool:
            if var.lower() in cls.__data.columns.tolist():
                cls.__vari = var.lower()
                send_succ_message(update, f'Var *{cls.__vari}* set up')
                return True
            else:
                send_fail_message(update, f'Var {chr(39)}{cls.__vari}{chr(39)} not found')
                return False

        def set_varu(update: TUpdate, var: str) -> bool:
            if var.lower() in cls.__data.columns.tolist():
                cls.__varu = var.lower()
                send_succ_message(update, f'Var *{cls.__varu}* set up')
                return True
            else:
                send_fail_message(update, f'Var {chr(39)}{cls.__varu}{chr(39)} not found')
                return False

        def set_varb(update: TUpdate, var: str) -> bool:
            bi_var = var.lower().split(chr(32))
            if bi_var[0] not in cls.__data.columns.tolist():
                send_fail_message(update, f'Var {chr(39)}{bi_var[0]}{chr(39)} not found')
                return False
            elif bi_var[1] not in cls.__data.columns.tolist():
                send_fail_message(update, f'Var {chr(39)}{bi_var[1]}{chr(39)} not found')
                return False
            else:
                cls.__varb[0] = bi_var[0]
                cls.__varb[1] = bi_var[1]
                send_succ_message(update, f'Vars *{cls.__varb[0]}* and *{cls.__varb[1]}* set up')
                return True

        # Aditional commands:
        def tita(update: TUpdate, context: TCallbackContext):
            cls.__com = tita.__name__
            try:
                cls.__data = titanic.get_data()
                send_succ_message(update, 'Titanic dataset selected. \U0001f6a2')
                help(update, context)
            except Exception as e:
                send_fail_message(update, '\.csv not found')
                print(e)

        def deli(update: TUpdate, context: TCallbackContext):
            cls.__com = deli.__name__
            cls.__vari = ''
            send_succ_message(update, 'Variable for /info deleted')

        def delu(update: TUpdate, context: TCallbackContext):
            cls.__com = delu.__name__
            cls.__varu = ''
            send_succ_message(update, 'Variable for /uvar deleted')

        def delb(update: TUpdate, context: TCallbackContext):
            cls.__com = delb.__name__
            cls.__varb = ['', '']
            send_succ_message(update, 'Variable for /bvar deleted')

        def delm(update: TUpdate, context: TCallbackContext):
            cls.__com = delm.__name__
            send_succ_message(update, 'Variable for /mvar deleted')
            cls.__varm = []

        # Messages
        def send_fail_message(update: TUpdate, error: str) -> None:
            update.message.reply_text(f'\U0000274C')
            update.message.reply_text(f'||Error: {error}\.||\nTry again with __/{cls.__com}__ command\.', parse_mode='MarkdownV2')

        def send_succ_message(update: TUpdate, message: str = '') -> None:
            if message != '':
                message = f': {message}.'
            update.message.reply_text(f'\U0001F680 Success!{message}', parse_mode='Markdown')
            time.sleep(1)

        def send_warn_message(update: TUpdate, message: str) -> None:
            update.message.reply_text(f'\U000026A0 {message}.')

        # Handlers
        def unknown_text(update: TUpdate, context: TCallbackContext) -> None:
            if cls.__isawait == True:
                cls.__isawait = False
                handler(update, context)
            else:
                update.message.reply_text(f'Sorry\.\.\. when you said {chr(34)}{update.message.text}{chr(34)}, I couldn{chr(39)}t understand you\.\n~Repeat, please~\.', parse_mode='MarkdownV2')

        def unknown_command(update: TUpdate, context: TCallbackContext) -> None:
            update.message.reply_text(f'\U0001f480 {update.message.text} command doesn{chr(39)}t exists.')

        def error(update: TUpdate, context: TCallbackContext) -> None:
            print(f'Error: {context.error}')

        def handler(update: TUpdate, context: TCallbackContext) -> None:
            if cls.__com == data.__name__:
                set_data(update, context, update.message.text)
            elif cls.__com == info.__name__:
                if set_vari(update, update.message.text):
                    info(update, context)
                else:
                    update.message.reply_text('See vars with /vars command.')
            elif cls.__com == uvar.__name__:
                if set_varu(update, update.message.text):
                    uvar(update, context)
                else:
                    update.message.reply_text('See vars with /vars command.')
            elif cls.__com == bvar.__name__:
                if set_varb(update, update.message.text):
                    bvar(update, context)
                else:
                    update.message.reply_text(
                        'See vars with /vars command or\n'
                        f'try writing vars between spaces: {chr(34)}var1 var2{chr(34)}')

        print('START')

        updater: TUpdater = TUpdater(constants.TOKEN, use_context=True)
        dispatcher: TDispatcher = updater.dispatcher  # type: ignore

        # Main commands
        dispatcher.add_handler(TCommandHandler('start', start))
        dispatcher.add_handler(TCommandHandler('help', help))
        dispatcher.add_handler(TCommandHandler('data', data))
        dispatcher.add_handler(TCommandHandler('vars', vars))
        dispatcher.add_handler(TCommandHandler('info', info))
        dispatcher.add_handler(TCommandHandler('uvar', uvar))
        dispatcher.add_handler(TCommandHandler('bvar', bvar))
        dispatcher.add_handler(TCommandHandler('mvar', mvar))

        # Additional commands
        dispatcher.add_handler(TCommandHandler('tita', tita))
        dispatcher.add_handler(TCommandHandler('deli', deli))
        dispatcher.add_handler(TCommandHandler('delu', delu))
        dispatcher.add_handler(TCommandHandler('delb', delb))
        dispatcher.add_handler(TCommandHandler('delm', delm))

        # Filters out unknown commands
        dispatcher.add_handler(TMessageHandler(TFilters.command, unknown_command))

        # Filters out unknown messages.
        dispatcher.add_handler(TMessageHandler(TFilters.text, unknown_text))

        # Error handler
        dispatcher.add_error_handler(error)  # type: ignore

        updater.start_polling()
        updater.idle()
