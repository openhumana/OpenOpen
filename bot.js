const { Telegraf } = require('telegraf');
const http = require('http');
const fs = require('fs');
const path = require('path');

// Initialize bot with the environment variable
const bot = new Telegraf(process.env.BOT_TOKEN);

// Website logic to restore your original index.html
const server = http.createServer((req, res) => {
    const filePath = path.join(__dirname, req.url === '/' ? 'index.html' : req.url);
    fs.readFile(filePath, (err, data) => {
        if (err) {
            res.writeHead(200, { 'Content-Type': 'text/plain' });
            res.end('Service Online');
            return;
        }
        res.writeHead(200);
        res.end(data);
    });
});

// Start the web server
server.listen(process.env.PORT || 8080, '0.0.0.0');

// Telegram Listener (Silent Observer Mode)
bot.on('text', async (ctx) => {
    console.log(`Alex observing: ${ctx.message.text}`);
    if (ctx.chat.type === 'private') {
        // Your AI generation code here
    }
});

// Launch bot AFTER the server is ready
bot.launch().catch(err => console.error('Bot launch failed:', err));

// 3. THE SILENT OBSERVER LOGIC
bot.on('text', async (ctx) => {
    console.log(`Alex observing: ${ctx.message.text}`); // He stays silent on server
    
    // Only responds if it's a private 1-on-1 message
    if (ctx.chat.type === 'private') {
        // ... your existing AI response code ...
        // ctx.reply(aiResponse);
    }
});

bot.launch();