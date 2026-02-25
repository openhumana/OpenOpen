const express = require('express');
const { Groq } = require('groq-sdk');
const { Telegraf } = require('telegraf');
require('dotenv').config();

const app = express();
app.use(express.json());
app.use(express.static('.')); 

// Initialize Groq and Telegram
const groq = new Groq({ apiKey: process.env.GROQ_API_KEY });
const bot = new Telegraf(process.env.BOT_TOKEN);

// Alex's Chat Logic
app.post('/api/chat', async (req, res) => {
    const { message } = req.body;
    try {
        // JOB 1: THE SALES AGENT
        const completion = await groq.chat.completions.create({
            messages: [
                { role: "system", content: "You are Alex, a high-performance Digital BDR for Open Humana. You are professional, high-energy, and drive sales." },
                { role: "user", content: message }
            ],
            model: "llama3-8b-8192",
        });

        const alexReply = completion.choices[0].message.content;

        // JOB 2: THE REPORTER (Sends to Telegram)
        bot.telegram.sendMessage(process.env.TELEGRAM_CHAT_ID, 
            `💼 **Alex Interaction Report**\n\nLead: "${message}"\n\nAlex: "${alexReply}"`
        ).catch(err => console.error("Telegram error:", err.message));

        res.json({ reply: alexReply });
    } catch (error) {
        console.error("Alex error:", error);
        res.status(500).json({ error: "Alex is offline." });
    }
});

// Safe Start
const startAlex = async () => {
    try {
        await bot.launch();
        console.log('✅ Alex connected to Telegram');
    } catch (err) {
        console.error('❌ Telegram failed:', err.message);
    }
    const PORT = process.env.PORT || 3000;
    app.listen(PORT, () => console.log(`🚀 Alex live on port ${PORT}`));
};

startAlex();