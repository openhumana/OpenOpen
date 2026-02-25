const express = require('express');
const { Groq } = require('groq-sdk');
const { Telegraf } = require('telegraf');
require('dotenv').config();

const app = express();
app.use(express.json());
app.use(express.static('.')); 

const groq = new Groq({ apiKey: process.env.GROQ_API_KEY });
const bot = new Telegraf(process.env.TELEGRAM_BOT_TOKEN);

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
            `💼 Alex Lead Report:\nUser: ${message}\nAlex: ${alexReply}`
        ).catch(e => console.error("Telegram Error", e));

        res.json({ reply: alexReply });
    } catch (error) {
        res.status(500).json({ error: "Offline" });
    }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Alex live on ${PORT}`));