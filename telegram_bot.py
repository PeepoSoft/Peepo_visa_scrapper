from conf import telegram_token
import telegram.ext
from telegram.ext import CommandHandler
from scrapper import get_data
import time
Token = telegram_token
updater = telegram.ext.Updater(Token, use_context=True)
dispatcher = updater.dispatcher

def send_message(context):
    
    current_time = time.strftime('%a, %d %b %Y %H:%M:%S', time.localtime())
    context.bot.send_message(chat_id=context.job.context, text='Revisión de citas a las {}'.format(current_time))
    result = get_data()
    if result != '':
        context.bot.send_message(chat_id=context.job.context, text=result)
    else:
        context.bot.send_message(chat_id=context.job.context, text='No hay citas disponibles')

def callback_auto_message(context):
    context.job_queue.run_once(send_message, 0,context=context.job.context)

def start_auto_messaging(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text='Iniciando servicio de revisión!')
    chat_id = update.message.chat_id
    context.job_queue.run_once(send_message, 0, context=chat_id)
    context.job_queue.run_repeating(callback_auto_message, 180, context=chat_id, name=str(chat_id))


def stop_notify(update, context):
    chat_id = update.message.chat_id
    context.bot.send_message(chat_id=chat_id, text='Terminal el servicio de revisión!')
    job = context.job_queue.get_jobs_by_name(str(chat_id))
    job[0].schedule_removal()


dispatcher.add_handler(CommandHandler("start", start_auto_messaging))
dispatcher.add_handler(CommandHandler("stop", stop_notify))

updater.start_polling()
updater.idle()