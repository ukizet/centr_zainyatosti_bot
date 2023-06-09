from aiogram.utils import executor
from create_bot import dp
from database import db
from handlers import client, admin, other
# from handlers import client, admin


async def on_startup(_):
    db.sql_start()
    print('Bot is online')


def main():
    admin.reg_handlers(dp)
    other.reg_handlers(dp)
    client.reg_handlers(dp)

    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)


if __name__ == '__main__':
    main()
