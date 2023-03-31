from aiogram.utils import executor
from create_bot import dp
from database import db
from handlers import client, admin, other
# from handlers import client, admin

async def on_startup(_):
    db.sql_start()
    print('Bot is online')
    


def main():
    # print('Bot is online')
    admin.reg_handlers_admin(dp)
    # other.reg_handlers_other(dp)
    client.reg_handlers_client(dp)

    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
    # executor.start_polling(dp, skip_updates=True)


# Запуск бота
if __name__ == '__main__':
    main()
