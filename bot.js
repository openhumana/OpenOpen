const { Telegraf } = require('telegraf');
const http = require('http');
const fs = require('fs');
const path = require('path');

// 1. Initialize Bot with Token from Railway Variables
const bot = new Telegraf(process.env.BOT_TOKEN);

// 2. WEB SERVER: This restores your original index.html
const server = http.createServer((req, res) => {
    // This looks for your original website files in your folder
    const filePath = path.join(__dirname, req.url === '/' ? 'index.html' : req.url);
    
    fs.readFile(filePath, (err, data) => {
        if (err) {
            // If original file is missing, show a simple status to keep Railway green
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
    // Log to server console (Observing)
    console.log(`Alex observed message: ${ctx.message.text}`);

    // ONLY reply if it's a 1-on-1 private chat with you
    if (ctx.chat.type === 'private') {
        try {
            // This is where your AI logic (alexBrain) should be called
            // const response = await alexBrain.generate(ctx.message.text);
            // await ctx.reply(response);
            await ctx.reply("Observing. I will only respond to private directives.");
        } catch (err) {
            console.error("AI Error:", err);
        }
    }
});

// 4. LAUNCH: This must be at the very bottom
bot.launch().then(() => console.log("Alex is monitoring Telegram...")).catch(err => {
    console.error("CRITICAL: Bot failed to launch. Check your BOT_TOKEN variable!", err.message);
});