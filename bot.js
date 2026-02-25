const http = require('http');

// This creates the actual website content for openhumana.com
const server = http.createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'text/html' });
  res.end(`
    <!DOCTYPE html>
    <html>
      <head><title>Open Humana</title></head>
      <body style="font-family: sans-serif; text-align: center; padding: 50px;">
        <h1>Open Humana</h1>
        <p>Alex is currently active and monitoring Telegram.</p>
        <div style="color: green;">● Systems Operational</div>
      </body>
    </html>
  `);
});

// Railway provides the PORT variable automatically
const PORT = process.env.PORT || 8080;
server.listen(PORT, () => {
  console.log('Website is live on port ' + PORT);
});