const { Telegraf } = require('telegraf');
const http = require('http');
const fs = require('fs');
const path = require('path');

// 1. Initialize Bot with Token from Railway Variables
const bot = new Telegraf(process.env.BOT_TOKEN);

// 2. WEB SERVER: This restores your original index.html
const server = http.createServer((req, res) => {
    // FIX: Tell the server to look in 'templates/landing.html'
    const filePath = path.join(__dirname, 'templates', req.url === '/' ? 'landing.html' : req.url);
    
    fs.readFile(filePath, (err, data) => {
        if (err) {
            res.writeHead(200, { 'Content-Type': 'text/plain' });
            res.end('Open Humana: System Online');
            return;
        }
        res.writeHead(200);
        res.end(data);
    });
});
// Bind to Port 8080 or Railway's dynamic port
server.listen(process.env.PORT || 8080, '0.0.0.0', () => {
    console.log("Website/Server is Live");
});

// 3. SILENT OBSERVER: Alex observes everything but only replies in Private
bot.on('text', async (ctx) => {
    // He logs everything (observing)
    console.log(`Alex observing: ${ctx.message.text}`);

    // He ONLY replies in a private chat
    if (ctx.chat.type === 'private') {
        try {
            // This is where your AI magic happens
            await ctx.reply("System active. Monitoring private channel.");
        } catch (e) {
            console.error("Reply failed:", e);
        }
    }
});
// 4. LAUNCH: This must be at the very bottom
bot.launch().then(() => console.log("Alex is monitoring Telegram...")).catch(err => {
    console.error("CRITICAL: Bot failed to launch. Check your BOT_TOKEN variable!", err.message);
});