from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo, BotCommand, MenuButtonWebApp
from telegram.ext import CommandHandler, CallbackContext, Updater, MessageHandler, Filters

TOKEN = '7870052180:AAH64NJaMYKIqaB7hAF7jjPn4M470TLoA6I'



def timeout_message(context: CallbackContext):
    job = context.job
    context.bot.send_message(job.context,
        "Bộ phận CSKH rất tiếc khi chưa nhận được phản hồi từ phía anh. "
        "Vì quá lâu không nhận được phản hồi của quý khách nên em xin đóng khung chat để hỗ trợ khách hàng khác. Nếu quý khách vẫn còn vấn đề hoặc thắc mắc chưa được hỗ trợ quý khách vui lòng liên hệ lại CSKH 24/7 để bên em hỗ trợ nhé ạ."
    )

def start(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    job_name = str(chat_id)

    # set time hủy job cũ
    old_jobs = context.job_queue.get_jobs_by_name(job_name)
    for job in old_jobs:
        job.schedule_removal()

    # gui tn
    update.message.reply_text("Chào mừng quý khách đã đến với 789P nhà cái cá cược uy tín nhất, đa dạng thể loại trò chơi...")
    update.message.reply_text("Chào mừng quý khách đến với CSKH 24/7 của 789P. Em có thể hỗ trợ được gì cho quý khách ạ?")
    update.message.reply_text("789P xin thông báo sự kiện Khuyến Mãi bí ẩn mỗi ngày...")

    # gửi anrh
    context.bot.send_photo(
        chat_id=chat_id,
        photo=open('1.jpg', 'rb'),
        caption="🎯 Ưu đãi chỉ áp dụng trong tháng này, đừng bỏ lỡ!"
    )

    # nút app
    keyboard = [[InlineKeyboardButton("👉 Vào 789P ngay", web_app=WebAppInfo(url="https://789p.pages.dev/"))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Ấn nút dưới đây để mở Mini App 👇", reply_markup=reply_markup)

    # job moiwss tên riêng
    context.job_queue.run_once(timeout_message, 180, context=chat_id, name=job_name)

def cancel_timeout(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    jobs = context.job_queue.get_jobs_by_name(str(chat_id))
    for job in jobs:
        job.schedule_removal()


def set_menu(bot):
    bot.set_chat_menu_button(
        menu_button=MenuButtonWebApp(
            text="👉 Vào 789P",
            web_app=WebAppInfo(url="https://789p.pages.dev/")
        )
    )

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    set_menu(updater.bot)

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, cancel_timeout))  

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
