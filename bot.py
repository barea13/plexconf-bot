from settings import *
from telegram.ext import Updater

# Función principal del bot
def main():
    updater = Updater(token=TOKEN_BOT, use_context=True)


# Ejecución del bot
if __name__ == '__main__':
    main()