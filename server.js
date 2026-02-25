require('dotenv').config();

const express = require('express');
const { Groq } = require('groq-sdk');
const { Telegraf } = require('telegraf');

// Debug: verify BOT_TOKEN is loaded (shows only first 5 chars)
console.log('🔑 BOT_TOKEN loaded:', process.env.BOT_TOKEN ? process.env.BOT_TOKEN.substring(0, 5) + '...' : 'MISSING');

const path = require('path');
const app = express();
app.use(express.json());
app.use('/static', express.static(path.join(__dirname, 'static'))); // Serve CSS, images, videos at /static/*
app.use('/templates', express.static(path.join(__dirname, 'templates'))); // Serve template assets

// Serve HTML pages
app.get('/', (req, res) => res.sendFile(path.join(__dirname, 'templates', 'landing.html')));
app.get('/login', (req, res) => res.sendFile(path.join(__dirname, 'templates', 'login.html')));
app.get('/about', (req, res) => res.sendFile(path.join(__dirname, 'templates', 'about.html')));
app.get('/contact', (req, res) => res.sendFile(path.join(__dirname, 'templates', 'contact.html')));
app.get('/help', (req, res) => res.sendFile(path.join(__dirname, 'templates', 'help.html')));
app.get('/privacy', (req, res) => res.sendFile(path.join(__dirname, 'templates', 'privacy.html')));
app.get('/terms', (req, res) => res.sendFile(path.join(__dirname, 'templates', 'terms.html')));
app.get('/compliance', (req, res) => res.sendFile(path.join(__dirname, 'templates', 'compliance.html')));
app.get('/blog', (req, res) => res.sendFile(path.join(__dirname, 'templates', 'blog_page.html')));
app.get('/verify-otp', (req, res) => res.sendFile(path.join(__dirname, 'templates', 'verify_otp.html')));
app.get('/profile-setup', (req, res) => res.sendFile(path.join(__dirname, 'templates', 'profile_setup.html')));
app.get('/super-admin', (req, res) => res.sendFile(path.join(__dirname, 'templates', 'super_admin.html')));
app.get('/index', (req, res) => res.sendFile(path.join(__dirname, 'templates', 'index.html')));

// 1. Initialize Alex's Brain (Groq) and Office Connection (Telegram)
// Guard against missing env vars so the server doesn't crash on startup
const GROQ_API_KEY = (process.env.GROQ_API_KEY || '').trim();
const BOT_TOKEN = (process.env.BOT_TOKEN || '').trim();
const ADMIN_CHAT_ID = (process.env.ADMIN_CHAT_ID || '').trim();

const groq = GROQ_API_KEY
    ? new Groq({ apiKey: GROQ_API_KEY })
    : null;

const bot = BOT_TOKEN
    ? new Telegraf(BOT_TOKEN)
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
        if (bot && ADMIN_CHAT_ID) {
            bot.telegram.sendMessage(ADMIN_CHAT_ID, 
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
            console.error('🔍 Check your BOT_TOKEN in Railway environment variables. Current token starts with:', BOT_TOKEN ? BOT_TOKEN.substring(0, 5) + '...' : 'MISSING');
        }
    }
    const PORT = process.env.PORT || 3000;
    const server = app.listen(PORT, () => console.log(`🚀 Alex: Sales Agent live on port ${PORT}`));
    server.on('error', (err) => {
        if (err.code === 'EADDRINUSE') {
            console.error(`❌ Port ${PORT} is already in use. Trying port ${PORT + 1}...`);
            app.listen(PORT + 1, () => console.log(`🚀 Alex: Sales Agent live on fallback port ${PORT + 1}`));
        } else {
            console.error('❌ Server error:', err.message);
            process.exit(1);
        }
    });
};

startAlex();