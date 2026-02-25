const http = require('http');
const fs = require('fs');
const path = require('path');

const server = http.createServer((req, res) => {
    // This tells the server to look for your original 'index.html' file
    const filePath = path.join(__dirname, req.url === '/' ? 'index.html' : req.url);
    
    fs.readFile(filePath, (err, data) => {
        if (err) {
            // Keep Railway happy with a 200 even if a file is missing
            res.writeHead(200, { 'Content-Type': 'text/plain' });
            res.end('Service Online');
            return;
        }
        res.writeHead(200);
        res.end(data);
    });
});

// Bind to 0.0.0.0 so Railway can reach the site
server.listen(process.env.PORT || 8080, '0.0.0.0');
bot.on('text', async (ctx) => {
    // 1. OBSERVE: Log every message to the server console
    console.log(`Alex observing: ${ctx.message.text}`);

    // 2. SILENT LOGIC: Only reply if it's a private 1-on-1 chat with you
    if (ctx.chat.type === 'private') {
        const response = await generateAIResponse(ctx.message.text);
        return ctx.reply(response);
    }
    
    // Otherwise, he stays silent.
});