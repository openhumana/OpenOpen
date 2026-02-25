const express = require('express');
const { Groq } = require('groq-sdk');
const { Telegraf } = require('telegraf');
require('dotenv').config();

const app = express();
app.use(express.json());
app.use(express.static('.')); 

// Use BOT_TOKEN to match your Railway Variable exactly
const groq = new Groq({ apiKey: process.env.GROQ_API_KEY });
const bot = new Telegraf(process.env.BOT_TOKEN);

app.post('/api/chat', async (req, res) => {
    const { message } = req.body;
    try {
        // JOB 1: THE SALES AGENT
        const completion = await groq.chat.completions.create({
            messages: [
                { role: "system", content: "You are Alex, a high-performance Digital BDR for Open Humana. You are professional and drive sales." },
                { role: "user", content: message }
            ],
            model: "llama3-8b-8192",
        });

        const alexReply = completion.choices[0].message.content;

        // JOB 2: THE REPORTER (Sends to your Telegram)
        bot.telegram.sendMessage(process.env.TELEGRAM_CHAT_ID, 
            `💼 **Alex Lead Report**\nUser: ${message}\nAlex: ${alexReply}`
        ).catch(e => console.error("Telegram Reporting Error:", e.message));

        res.json({ reply: alexReply });
    } catch (error) {
        console.error("Alex Error:", error);
        res.status(500).json({ error: "Alex is offline." });
    }
});

// Safe Start Logic: Don't crash if the token is wrong
const startAlex = async () => {
    try {
        await bot.launch();
        console.log('✅ Alex connected to Telegram');
    } catch (err) {
        console.error('❌ Telegram connection failed. Check your BOT_TOKEN variable!');
    }
    const PORT = process.env.PORT || 3000;
    app.listen(PORT, () => console.log(`🚀 Alex live on port ${PORT}`));
};

startAlex();