const { Telegraf } = require('telegraf');
const http = require('http');
const fs = require('fs');
const path = require('path');

// 1. Initialize Alex (The Bot)
// This pulls the token from your Railway Variables tab
const bot = new Telegraf(process.env.BOT_TOKEN);

// 2. THE WEBSITE SERVER (Handles landing page + CSS/Images)
const server = http.createServer((req, res) => {
    let filePath;
    
    // Route for the homepage: looks in templates/landing.html
    if (req.url === '/' || req.url === '/index.html') {
        filePath = path.join(__dirname, 'templates', 'landing.html');
    } else {
        // Route for CSS, Images, and JS (e.g., /static/landing.css)
        // This looks for files in your project folders based on the URL
        filePath = path.join(__dirname, req.url.replace(/^\//, ''));
    }

    fs.readFile(filePath, (err, data) => {
        if (err) {
            // Fallback to keep the server from crashing if a file is missing
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

// Start the web server on Railway's assigned port
server.listen(process.env.PORT || 8080, '0.0.0.0', () => {
    console.log("🚀 Web Server initialized. Website is live at openhumana.com");
});

// 3. SILENT OBSERVER LOGIC
bot.on('text', async (ctx) => {
    // Alex logs everything (observing the server)
    console.log(`Alex observing message from ${ctx.from.username}: ${ctx.message.text}`);

    // Alex ONLY replies if it is a private 1-on-1 message to you
    if (ctx.chat.type === 'private') {
        try {
            // For now, this confirms the connection is working. 
            // You can replace this with your actual AI brain call.
            await ctx.reply("System authorized. Observing and ready for directives.");
        } catch (error) {
            console.error("Alex failed to reply:", error.message);
        }
    }
});

// 4. LAUNCH THE BRAIN
bot.launch()
    .then(() => console.log("🤖 Alex is now observing Telegram..."))
    .catch(err => {
        console.error("❌ Bot failed to start. 401 means your BOT_TOKEN is wrong!");
        console.error(err.message);
    });

// Handle graceful shutdowns
process.once('SIGINT', () => bot.stop('SIGINT'));
process.once('SIGTERM', () => bot.stop('SIGTERM'));