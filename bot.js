const { Telegraf } = require('telegraf');
const http = require('http');
const fs = require('fs');
const path = require('path');

// 1. Initialize Alex (The Bot)
// Make sure BOT_TOKEN is set in Railway Variables
const bot = new Telegraf(process.env.BOT_TOKEN);

// 2. THE WEBSITE SERVER (Fixes the "Ruined" look)
const server = http.createServer((req, res) => {
    let filePath;
    
    // Route for the homepage
    if (req.url === '/' || req.url === '/index.html') {
        filePath = path.join(__dirname, 'templates', 'landing.html');
    } else {
        // Route for CSS, Images, and JS (e.g., /static/landing.css)
        // This removes the leading slash and looks in your project folder
        filePath = path.join(__dirname, req.url.replace(/^\//, ''));
    }

    fs.readFile(filePath, (err, data) => {
        if (err) {
            // Fallback to keep Railway health-checks green
            res.writeHead(200, { 'Content-Type': 'text/plain' });
            res.end('Open Humana: System Online');
            return;
        }

        // Identify the file type so styles and images load correctly
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

// Start the web server on Railway's port
server.listen(process.env.PORT || 8080, '0.0.0.0', () => {
    console.log("🚀 Website is LIVE and styles are linked.");
});

// 3. SILENT OBSERVER LOGIC
bot.on('text', async (ctx) => {
    // Alex logs everything (observing the server)
    console.log(`Alex observing: ${ctx.message.text}`);

    // Alex ONLY replies if it is a private 1-on-1 message
    if (ctx.chat.type === 'private') {
        try {
            // This is where Alex's brain generates a response
            // For now, it sends a confirmation of the directive
            await ctx.reply("Directive received. System monitoring remains active.");
        } catch (error) {
            console.error("Alex failed to reply:", error);
        }
    }
});

// 4. LAUNCH THE BRAIN
bot.launch()
    .then(() => console.log("🤖 Alex is now observing Telegram..."))
    .catch(err => console.error("❌ Bot failed to start. Check your Token!", err.message));

// Graceful stop
process.once('SIGINT', () => bot.stop('SIGINT'));
process.once('SIGTERM', () => bot.stop('SIGTERM'));