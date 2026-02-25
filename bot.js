const { Telegraf } = require('telegraf');
const http = require('http');
const fs = require('fs');
const path = require('path');

// 1. Initialize Alex (The Bot)
const token = process.env.BOT_TOKEN;

// DEBUG: This helps us see if Railway is actually passing the token to the code
if (!token) {
    console.error("CRITICAL: BOT_TOKEN variable is empty in Railway!");
} else {
    console.log(`System: Token detected (starting with: ${token.substring(0, 5)}...)`);
}

const bot = new Telegraf('8796414492:AAHp90vVeJXinWRD-e2OZNFAu2Giqv9KQZk')

// 2. THE WEBSITE SERVER (Handles landing page + CSS/Images)
const server = http.createServer((req, res) => {
    let filePath;
    
    if (req.url === '/' || req.url === '/index.html') {
        filePath = path.join(__dirname, 'templates', 'landing.html');
    } else {
        // Correctly serves /static/ files for your styles/images
        filePath = path.join(__dirname, req.url.replace(/^\//, ''));
    }

    fs.readFile(filePath, (err, data) => {
        if (err) {
            res.writeHead(200, { 'Content-Type': 'text/plain' });
            res.end('Open Humana: System Online');
            return;
        }

        const ext = path.extname(filePath).toLowerCase();
        const mimeTypes = {
            '.html': 'text/html',
            '.css': 'text/css',
            '.js': 'text/javascript',
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.gif': 'image/gif',
            '.svg': 'image/svg+xml',
        };

        res.writeHead(200, { 'Content-Type': mimeTypes[ext] || 'application/octet-stream' });
        res.end(data);
    });
});

server.listen(process.env.PORT || 8080, '0.0.0.0', () => {
    console.log("🚀 Web Server initialized. openhumana.com is live.");
});

// 3. SILENT OBSERVER LOGIC
bot.on('text', async (ctx) => {
    // Observer Role: Log all activity to the server console
    console.log(`[Observer] Message from ${ctx.from.username || 'User'}: ${ctx.message.text}`);

    // Response Role: Alex ONLY speaks in private 1-on-1 chats
    if (ctx.chat.type === 'private') {
        try {
            await ctx.reply("System authorized. I am observing and ready for private directives.");
        } catch (error) {
            console.error("Telegram Reply Error:", error.message);
        }
    }
});

// 4. LAUNCH
bot.launch()
    .then(() => console.log("🤖 Alex is now observing Telegram..."))
    .catch(err => {
        console.error("❌ Bot failed to start. Telegram rejected the token (401).");
        console.error("Error Detail:", err.message);
    });

// Handle graceful shutdowns
process.once('SIGINT', () => bot.stop('SIGINT'));
process.once('SIGTERM', () => bot.stop('SIGTERM'));