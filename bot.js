res.end(`
  <!DOCTYPE html>
  <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Open Humana</title>
      <style>
        body { margin: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #000; color: #fff; display: flex; justify-content: center; align-items: center; height: 100vh; }
        .container { text-align: center; }
        h1 { font-weight: 200; letter-spacing: 5px; text-transform: uppercase; font-size: 2.5rem; }
        .status-dot { height: 8px; width: 8px; background-color: #0f0; border-radius: 50%; display: inline-block; margin-right: 10px; box-shadow: 0 0 10px #0f0; }
        .footer { position: absolute; bottom: 20px; font-size: 0.8rem; opacity: 0.4; }
      </style>
    </head>
    <body>
      <div class="container">
        <h1>Open Humana</h1>
      </div>
      <div class="footer">
        <span class="status-dot"></span> System Encrypted & Secure
      </div>
    </body>
  </html>
`);