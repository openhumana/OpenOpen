const { Telegraf } = require('telegraf');
const { askAlex } = require('./alexBrain');
require('dotenv').config();

const bot = new Telegraf(process.env.TELEGRAM_BOT_TOKEN);
const ADMIN_ID = process.env.ADMIN_CHAT_ID;

// Security Middleware: Only talks to YOU
bot.use(async (ctx, next) => {
  if (ctx.from.id.toString() !== ADMIN_ID.toString()) {
    return ctx.reply("System Locked. You are not authorized to command Alex.");
  }
  return next();
});

bot.start((ctx) => ctx.reply('Associate Alex online. Ready to lead Open Humana to the top. What is our first move?'));

bot.on('text', async (ctx) => {
  // Show Alex is "thinking"
  await ctx.sendChatAction('typing');
  
  const response = await askAlex(ctx.message.text);
  await ctx.reply(response);
});

bot.launch();

// Enable graceful stop
process.once('SIGINT', () => bot.stop('SIGINT'));
process.once('SIGTERM', () => bot.stop('SIGTERM'));

console.log("Alex is now listening on Telegram...");