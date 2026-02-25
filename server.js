require('dotenv').config();

const express = require('express');
const { Groq } = require('groq-sdk');
const { Telegraf } = require('telegraf');

// Debug: verify BOT_TOKEN is loaded (shows only first 5 chars)
console.log('🔑 BOT_TOKEN loaded:', process.env.BOT_TOKEN ? process.env.BOT_TOKEN.substring(0, 5) + '...' : 'MISSING');

const app = express();
app.use(express.json());
app.use(express.static('.')); // Serves your index.html and other files

// 1. Initialize Alex's Brain (Groq) and Office Connection (Telegram)
// Guard against missing env vars so the server doesn't crash on startup
const groq = process.env.GROQ_API_KEY
    ? new Groq({ apiKey: process.env.GROQ_API_KEY })
    : null;

const bot = process.env.BOT_TOKEN
    ? new Telegraf(process.env.BOT_TOKEN)
    : null;

if (!groq) console.warn('⚠️  GROQ_API_KEY is missing – /api/chat will return errors until it is set.');
if (!bot) console.warn('⚠️  BOT_TOKEN is missing – Telegram integration disabled.');

// 2. Alex's Sales Job (Website Chat)
app.post('/api/chat', async (req, res) => {
    const { message } = req.body;
    if (!groq) {
        return res.status(503).json({ error: "Chat service is not configured (missing GROQ_API_KEY)." });
    }
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
        if (bot && process.env.ADMIN_CHAT_ID) {
            bot.telegram.sendMessage(process.env.ADMIN_CHAT_ID, 
                `💼 **Alex Interaction Report**\n\nLead said: "${message}"\n\nAlex replied: "${alexReply}"`
            ).catch(err => console.error("Telegram error:", err.message));
        }

        res.json({ reply: alexReply });
    } catch (error) {
        console.error("Alex Glitch:", error);
        res.status(500).json({ error: "Alex is taking a short break." });
    }
});

// 3. Safe Start: Don't let a bad token crash the whole site
const startAlex = async () => {
    if (bot) {
        try {
            await bot.launch();
            console.log('✅ Alex: Connected to Telegram Digital Office');
        } catch (err) {
            console.error('❌ Alex: Telegram connection failed. Error:', err.message);
            console.error('🔍 Check your BOT_TOKEN in Railway environment variables. Current token starts with:', process.env.BOT_TOKEN ? process.env.BOT_TOKEN.substring(0, 5) + '...' : 'MISSING');
        }
    }
    const PORT = process.env.PORT || 3000;
    app.listen(PORT, () => console.log(`🚀 Alex: Sales Agent live on port ${PORT}`));
};

startAlex();