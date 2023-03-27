from aiogram.utils import executor
from create_bot import dp
from handlers import client, admin
from database import db

async def on_startup(_):
    print('Bot is online')
    db.sql_start()


def main():
    admin.reg_handlers_admin(dp)
    client.reg_handlers_client(dp)
    # other.register_handlers_other(dp)

    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)


# Запуск бота
if __name__ == '__main__':
    main()
