def main():
    print('START')

    from telegram.ext.updater import Updater as TUpdater
    from telegram.ext.callbackcontext import CallbackContext as TCallbackContext
    from telegram.ext.commandhandler import CommandHandler as TCommandHandler
    from telegram.ext.messagehandler import MessageHandler as TMessageHandler
    from telegram.ext.filters import Filters as TFilters
    from telegram.update import Update as TUpdate
    from eda_bot.constants import TOKEN

    def start(update: TUpdate, context: TCallbackContext):
        update.message.reply_text(
            text=
            'Hello!\n'
            'Welcome to this EDA bot! \U0001F47D\n'
            'How can I help you?\n'
            'Press /help to see the commands available.')

    def help(update: TUpdate, context: TCallbackContext):
        update.message.reply_text(
            '/link   - Set up dataset link.\n'
            '/vars   - See dataset variables.\n'
            '/info   - See variable info.\n'
            '/uvar   - Get univariate graph.\n'
            '/bvar   - Get bivariate graph.\n'
            '/mvar   - Get multivariate graph.'
        )

    def link(update: TUpdate, context: TCallbackContext):
        update.message.reply_text('Enter the dataset .csv link:')

    def vars(update: TUpdate, context: TCallbackContext):
        update.message.reply_text('Dataset variables:')

    def info(update: TUpdate, context: TCallbackContext):
        if len(context.args) == 0:
            update.message.reply_text('Enter the query variable:')
        else:
            update.message.reply_text(" ".join(context.args))

    def uvar(update: TUpdate, context: TCallbackContext):
        update.message.reply_text(f'Univariate graph for {update.message.text}:')

    def bvar(update: TUpdate, context: TCallbackContext):
        update.message.reply_text(f'Bivariate graph for {update.message.text}:')

    def mvar(update: TUpdate, context: TCallbackContext):
        update.message.reply_text(f'Multivariate graph for {update.message.text}:')

    def unknown_command(update: TUpdate, context: TCallbackContext):
        update.message.reply_text(f'{update.message.text} command doesn{chr(39)}t exists.')

    def unknown_text(update: TUpdate, context: TCallbackContext):
        update.message.reply_text(f'Sorry... when you said {chr(34)}{update.message.text}{chr(34)} I couldn{chr(39)}t understand you.')

    try:
        updater = TUpdater(TOKEN, use_context=True)

        updater.dispatcher.add_handler(TCommandHandler('start', start))
        updater.dispatcher.add_handler(TCommandHandler('help', help))
        updater.dispatcher.add_handler(TCommandHandler('link', link))
        updater.dispatcher.add_handler(TCommandHandler('vars', vars))
        updater.dispatcher.add_handler(TCommandHandler('info', info))
        updater.dispatcher.add_handler(TCommandHandler('uvar', uvar))
        updater.dispatcher.add_handler(TCommandHandler('bvar', bvar))
        updater.dispatcher.add_handler(TCommandHandler('mvar', mvar))
        updater.dispatcher.add_handler(TMessageHandler(TFilters.command, unknown_command))  # Filters out unknown commands
        updater.dispatcher.add_handler(TMessageHandler(TFilters.text, unknown_text))

        updater.start_polling()
    except Exception as e:
        print(e)
