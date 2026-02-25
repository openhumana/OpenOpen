const express = require('express');
const { Groq } = require('groq-sdk');
const { Telegraf } = require('telegraf');
require('dotenv').config();

const app = express();
app.use(express.json());
app.use(express.static('.')); // Serves your index.html and other files

// 1. Initialize Alex's Brain (Groq) and Office Connection (Telegram)
const groq = new Groq({ apiKey: process.env.GROQ_API_KEY });
const bot = new Telegraf(process.env.BOT_TOKEN); // Matches your Railway variable

// 2. Alex's Sales Job (Website Chat)
app.post('/api/chat', async (req, res) => {
    const { message } = req.body;
    try {
        // JOB 1: THE SALES AGENT (Talk to website user)
        const completion = await groq.chat.completions.create({
            messages: [
                { role: "system", content: "You are Alex, a high-performance Digital BDR for Open Humana. Be professional and drive sales." },
                { role: "user", content: message }
            ],
            model: "llama3-8b-8192",
        });

        const alexReply = completion.choices[0].message.content;

        // JOB 2: THE REPORTER (Ping the Digital Office)
        bot.telegram.sendMessage(process.env.TELEGRAM_CHAT_ID, 
            `💼 **Alex Interaction Report**\n\nLead said: "${message}"\n\nAlex replied: "${alexReply}"`
        ).catch(err => console.error("Telegram error:", err.message));

        res.json({ reply: alexReply });
    } catch (error) {
        console.error("Alex Glitch:", error);
        res.status(500).json({ error: "Alex is taking a short break." });
    }
});

// 3. Safe Start: Don't let a bad token crash the whole site
const startAlex = async () => {
    try {
        await bot.launch(); //
        console.log('✅ Alex: Connected to Telegram Digital Office');
    } catch (err) {
        console.error('❌ Alex: Telegram connection failed (401 Unauthorized). Check your BOT_TOKEN!');
    }
    const PORT = process.env.PORT || 3000;
    app.listen(PORT, () => console.log(`🚀 Alex: Sales Agent live on port ${PORT}`));
};

startAlex();