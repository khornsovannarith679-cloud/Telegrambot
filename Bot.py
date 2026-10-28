import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# បើកប្រព័ន្ធ Log ដើម្បីមើលកំហុសកូដ (Errors)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# ១. មុខងារឆ្លើយតបពេលចុច /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "👋 សួស្តី! ខ្ញុំជា Bot សម្រាប់រំលឹកកិច្ចការសាលារបស់អ្នក។\n\n"
        "ដើម្បីកំណត់ការរំលឹក សូមវាយតាមទម្រង់ខាងក្រោម៖\n"
        "<code>/remind [ចំនួនវិនាទី] [ឈ្មោះកិច្ចការ]</code>\n\n"
        "ឧទាហរណ៍៖ <code>/remind 10 កិច្ចការប្រវត្តិវិទ្យា</code>",
        parse_mode="HTML"
    )

# ២. មុខងារសម្រាប់ផ្ញើសាររំលឹក នៅពេលដល់ម៉ោងកំណត់
async def send_reminder(context: ContextTypes.DEFAULT_TYPE) -> None:
    job = context.job
    await context.bot.send_message(
        chat_id=job.chat_id, 
        text=f"🚨 **រំលឹកកិច្ចការ!** កុំភ្លេចធ្វើ ឬប្រគល់កិច្ចការ៖ **{job.data}** ណា៎!"
    )

# ៣. មុខងារទទួលបញ្ជាពី /remind រួចកំណត់នាឡិកាថយក្រោយ
async def set_reminder(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_message.chat_id
    try:
        due_seconds = float(context.args[0])
        assignment_name = " ".join(context.args[1:])

        if not assignment_name:
            await update.message.reply_text("❌ សូមបញ្ជាក់ពីឈ្មោះកិច្ចការផង។")
            return

        if due_seconds < 0:
            await update.message.reply_text("❌ ពេលវេលាមិនអាចអវិជ្ជមានទេ!")
            return

        # បញ្ជាឲ្យប្រព័ន្ធរាប់ម៉ោងថយក្រោយ
        context.job_queue.run_once(
            send_reminder, 
            when=due_seconds, 
            chat_id=chat_id, 
            name=str(chat_id), 
            data=assignment_name
        )

        await update.message.reply_text(
            f"✅ បានកំណត់ជោគជ័យ! ខ្ញុំនឹងរំលឹកអ្នកអំពី «{assignment_name}» ក្នុងរយៈពេល {due_seconds} វិនាទីទៀត។"
        )

    except (IndexError, ValueError):
        await update.message.reply_text("❌ របៀបប្រើប្រាស់ខុសហើយ! សូមវាយ៖ /remind [ចំនួនវិនាទី] [ឈ្មោះកិច្ចការ]")

def main() -> None:
    # ដាក់លេខកូដសម្ងាត់ Token របស់អ្នកនៅទីនេះ
    TOKEN = "9180119018:AAGas2yZoht1QfbP_UW7r6ZtWwtu6lCySbU"

    # បង្កើត Application របស់ Bot
    app = Application.builder().token(TOKEN).build()

    # ភ្ជាប់ពាក្យបញ្ជា /start និង /remind ជាមួយមុខងារក្នុងកូដ
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("remind", set_reminder))

    # បើកឲ្យ Bot ដំណើរការរង់ចាំសារចូល
    print("Bot កំពុងចាប់ផ្តើមដំណើរការ...")
    app.run_polling()

if __name__ == "__main__":
    main()
