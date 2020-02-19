import logging

import os
from plexapi.server import PlexServer, Library
from plexapi.myplex import MyPlexAccount
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler, PicklePersistence)

data = PicklePersistence(filename='data')

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

SERVER, USER, PASSW, INVITAR = range(4)

def facts_to_str(user_data):
    facts = list()

    for key, value in user_data.items():
        facts.append('{} - {}'.format(key, value))

    return "\n".join(facts).join(['\n', '\n'])

def start(update, context):
    update.message.reply_text(
        'Hola! Vamos a configurar el Plex\n'
        'Envía /cancel para dejar de hablar conmigo'
    )
    update.message.reply_text('Dime la IP de tu servidor')
    return SERVER

def server(update, context):
    user = update.message.from_user
    logger.info("IP de %s: %s", user.first_name, update.message.text)

    server_ip = update.message.text
    context.user_data['server'] = server_ip
    text = "Perfecto! Tu IP guardada es: " + server_ip
    update.message.reply_text(text)

    update.message.reply_text('Dime tu correo de Plex')
    # text = str(cuenta.users())
    # update.message.reply_text(text)
    return USER

def user(update, context):
    user = update.message.from_user
    logger.info("Usuario de %s: %s", user.first_name, update.message.text)

    server_user = update.message.text
    context.user_data['user'] = server_user
    text = 'Estupendo! Tu usuario guardado es: ' + server_user
    update.message.reply_text(text)
    update.message.reply_text('Dime tu contraseña de Plex')
    return PASSW

def passw(update, context):
    user = update.message.from_user
    logger.info("Contraseña de %s: %s", user.first_name, update.message.text)

    server_pass = update.message.text
    context.user_data['pass'] = server_pass
    text = 'Estupendo! Ya tengo tu contraseña'
    update.message.reply_text(text)

    # Plex Connection
    # cuenta = MyPlexAccount(str(server_user), str(server_pass))
    # update.message.reply_text(str(cuenta.users()))

    return ConversationHandler.END

def cancel(update, context):
    user = update.message.from_user
    logger.info("Usuario %s ha cancelado la conversación.", user.first_name)

    update.message.reply_text('Adiós! Nos vemos pronto!')
    return ConversationHandler.END

def sesiones(update, context):
    user = update.message.from_user
    logger.info("Usuario %s ha visto las sesiones activas", user.first_name)

    update.message.reply_text('Aquí tienes las sesiones activas')
    update.message.reply_text(str(plex.library.sections()))


def invitar(update, context):
    user = update.message.from_user
    user_says = " ".join(context.args)
    logger.info("Usuario %s invita a %s", user.first_name, user_says)
    update.message.reply_text("Vas a invitar a: " + user_says)
    # Aquí invitaría al usuario en Plex
    # cuenta = MyPlexAccount(context.user_data['user'], context.user_data['pass'])
    # cuenta.inviteFriend(user_says)

def info(update, context):
    update.message.reply_text("This is what you already told me:"
                              "{}".format(facts_to_str(context.user_data)))

def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update.message.from_user, context.error)


# Función principal del bot
def main():

    updater = Updater(token="TOKEN_BOT", persistence=data, use_context=True)

    dp = updater.dispatcher

    cmd_config = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            SERVER: [MessageHandler(Filters.update.message, server)],
            USER: [MessageHandler(Filters.update.message, user)],
            PASSW: [MessageHandler(Filters.update.message, passw)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
        persistent=True,
        name='config'
    )

    cmd_invitar = CommandHandler('invitar', invitar, pass_args=True)
    cmd_sesiones = CommandHandler('sesiones', sesiones)
    cmd_info = CommandHandler('info', info)

    dp.add_handler(cmd_config)
    dp.add_handler(cmd_invitar)
    dp.add_handler(cmd_sesiones)
    dp.add_handler(cmd_info)

    dp.add_error_handler(error)

    updater.start_polling()

    updater.idle()

# Ejecución del bot
if __name__ == '__main__':
    main()