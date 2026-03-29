import os
import telebot
from flask import Flask, request
from telebot.types import ReplyKeyboardMarkup

TOKEN = os.environ.get("BOT_TOKEN")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)


# ===== TEXT =====

disclaimer = """⚠️ Disclaimer

This bot is created for educational purposes only.
Trading involves financial risk and may result in loss.
We do not provide financial advice, signals, or guaranteed results.

By continuing, you confirm that you understand and accept this.
"""

welcome = """Welcome.

Most people jump into markets without understanding how they move.

This space is designed to help you slow down and think clearly.

Inside, you’ll explore:
• How markets actually behave
• Why most beginners get confused
• How structured thinking improves decisions

No signals. No shortcuts. Just learning.

Choose a topic to begin.
"""

market_basics = """📊 Market Basics

Markets don’t move randomly.

They follow patterns influenced by:
• Trends (direction)
• Ranges (consolidation)
• Liquidity zones
• Volatility changes

Understanding these helps you read charts with more clarity.
"""

psychology = """🧠 Trading Psychology

Most mistakes come from emotions, not strategy.

Common challenges:
• Fear after losses
• Overconfidence after wins
• Impatience in slow markets

Learning to stay neutral is key to long-term consistency.
"""

decision = """⚙️ Decision Framework

Before any action, ask:

• What is the current market condition?
• Is risk clearly defined?
• Am I reacting or following a plan?

A structured approach reduces unnecessary mistakes.
"""

support = """📩 Support

For questions about learning topics or guidance:

Contact: @tradewithparul

Support is limited to educational discussions only.
No trading advice or signals are provided.
"""


# ===== MENU =====

def menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("📊 Market Basics", "🧠 Trading Psychology")
    kb.row("⚙️ Decision Framework", "📩 Support")
    return kb


# ===== START =====

@bot.message_handler(commands=['start'])
def start(msg):

    d = bot.send_message(msg.chat.id, disclaimer)

    try:
        bot.pin_chat_message(msg.chat.id, d.message_id)
    except:
        pass

    bot.send_message(msg.chat.id, welcome, reply_markup=menu())


# ===== BUTTONS =====

@bot.message_handler(func=lambda m: m.text == "📊 Market Basics")
def b1(m):
    bot.send_message(m.chat.id, market_basics)

@bot.message_handler(func=lambda m: m.text == "🧠 Trading Psychology")
def b2(m):
    bot.send_message(m.chat.id, psychology)

@bot.message_handler(func=lambda m: m.text == "⚙️ Decision Framework")
def b3(m):
    bot.send_message(m.chat.id, decision)

@bot.message_handler(func=lambda m: m.text == "📩 Support")
def b4(m):
    bot.send_message(m.chat.id, support)


# ===== WEBHOOK =====

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    bot.process_new_updates(
        [telebot.types.Update.de_json(request.stream.read().decode("utf-8"))]
    )
    return "ok", 200


@app.route("/")
def home():
    return "Bot Running"


if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(
        url=os.environ.get("RENDER_EXTERNAL_URL") + "/" + TOKEN
    )
    app.run(host="0.0.0.0", port=10000)
