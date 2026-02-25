require('dotenv').config();

const express = require('express');
const nunjucks = require('nunjucks');
const { Groq } = require('groq-sdk');
const { Telegraf } = require('telegraf');

// Debug: verify BOT_TOKEN is loaded (shows only first 5 chars)
console.log('🔑 BOT_TOKEN loaded:', process.env.BOT_TOKEN ? process.env.BOT_TOKEN.trim().substring(0, 5) + '...' : 'MISSING');

const path = require('path');
const app = express();
app.use(express.json());

// Absolute static pathing – serves CSS/JS/images with correct MIME types
app.use('/static', express.static(path.join(__dirname, 'static'), {
    setHeaders(res, filePath) {
        if (filePath.endsWith('.css'))  res.setHeader('Content-Type', 'text/css');
        if (filePath.endsWith('.js'))   res.setHeader('Content-Type', 'application/javascript');
    }
}));
app.use('/templates', express.static(path.join(__dirname, 'templates')));

// Configure Nunjucks with absolute template path (Jinja2-compatible)
nunjucks.configure(path.join(__dirname, 'templates'), {
    autoescape: true,
    express: app,
    watch: false,
    noCache: process.env.NODE_ENV !== 'production'
});
app.set('view engine', 'html');

// Serve HTML pages – every route uses res.render with a context object
app.get('/', (req, res) => res.render('landing.html', {}));
app.get('/login', (req, res) => res.render('login.html', { signup: false, error: null, info_message: null, google_oauth: false, app_password_set: false }));
app.get('/about', (req, res) => res.render('about.html', {}));
app.get('/contact', (req, res) => res.render('contact.html', {}));
app.get('/help', (req, res) => res.render('help.html', {}));
app.get('/privacy', (req, res) => res.render('privacy.html', {}));
app.get('/terms', (req, res) => res.render('terms.html', {}));
app.get('/compliance', (req, res) => res.render('compliance.html', {}));
app.get('/blog', (req, res) => res.render('blog_page.html', {}));
app.get('/verify-otp', (req, res) => res.render('verify_otp.html', { email: '', error: null }));
app.get('/profile-setup', (req, res) => res.render('profile_setup.html', { user: { profile_image_url: null, profile_name: '' } }));
app.get('/super-admin', (req, res) => res.render('super_admin.html', {}));
app.get('/index', (req, res) => res.render('index.html', { user: null, telnyx_from: '' }));

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

// 2. Lead Form Submission (Email + Telegram)
const nodemailer = require('nodemailer');
const SMTP_USER = (process.env.SMTP_USER || '').trim();
const SMTP_PASS = (process.env.SMTP_PASS || '').trim();

const mailTransporter = (SMTP_USER && SMTP_PASS)
    ? nodemailer.createTransport({
        service: 'gmail',
        auth: { user: SMTP_USER, pass: SMTP_PASS }
    })
    : null;

if (!mailTransporter) console.warn('⚠️  SMTP_USER/SMTP_PASS missing – lead emails disabled.');

app.post('/api/lead', async (req, res) => {
    const { name, phone, email, company } = req.body;
    if (!name || !email) {
        return res.status(400).json({ error: 'Name and email are required.' });
    }

    // Send Telegram notification to admin
    if (bot && ADMIN_CHAT_ID) {
        bot.telegram.sendMessage(ADMIN_CHAT_ID,
            `🔥 **New Lead Captured**\n\nName: ${name}\nPhone: ${phone || 'N/A'}\nEmail: ${email}\nCompany: ${company || 'N/A'}`
        ).catch(err => console.error('Telegram lead error:', err.message));
    }

    // Send welcome email with Alex Resume PDF
    if (mailTransporter) {
        try {
            const alexResumePath = path.join(__dirname, 'static', 'Alex_Resume.pdf');
            const fs = require('fs');
            const attachments = fs.existsSync(alexResumePath)
                ? [{ filename: 'Alex_Resume.pdf', path: alexResumePath }]
                : [];

            await mailTransporter.sendMail({
                from: `"Open Humana" <${SMTP_USER}>`,
                to: email,
                subject: 'Welcome to Open Humana — Meet Alex, Your Digital BDR',
                html: `
                    <div style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto;padding:32px;background:#0a0a1a;color:#fff;border-radius:12px;">
                        <h1 style="font-size:24px;margin-bottom:16px;">Hey ${name}! 👋</h1>
                        <p style="color:rgba(255,255,255,0.7);line-height:1.7;">Thanks for your interest in Open Humana. Attached is Alex's resume — your future Digital BDR who works 24/7, never takes a sick day, and dials 3,000+ numbers per day.</p>
                        <p style="color:rgba(255,255,255,0.7);line-height:1.7;">Our team will reach out within 15 minutes to get you set up.</p>
                        <div style="margin-top:24px;padding:16px;background:rgba(255,255,255,0.05);border-radius:8px;border:1px solid rgba(255,255,255,0.1);">
                            <p style="margin:0;color:rgba(255,255,255,0.5);font-size:13px;">Company: ${company || 'N/A'} | Phone: ${phone || 'N/A'}</p>
                        </div>
                        <p style="margin-top:24px;color:rgba(255,255,255,0.4);font-size:12px;">— The Open Humana Team</p>
                    </div>
                `,
                attachments
            });
            console.log(`📧 Welcome email sent to ${email}`);
        } catch (err) {
            console.error('Email send error:', err.message);
        }
    }

    res.json({ success: true, message: 'Thanks! We\'ll be in touch within 15 minutes.' });
});

// 3. Alex's Sales Job (Website Chat)
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
            model: "llama-3.1-8b-instant",
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

// 3. Safe Start: Web server starts FIRST, then Telegram bot connects in background
const PORT = process.env.PORT || 3000;
const server = app.listen(PORT, '0.0.0.0', () => {
    console.log(`🚀 Alex: Sales Agent live on port ${PORT}`);

    // Launch Telegram bot in background (non-blocking) after server is up
    if (bot) {
        bot.launch()
            .then(() => console.log('✅ Alex: Connected to Telegram Digital Office'))
            .catch(err => {
                console.error('❌ Alex: Telegram connection failed. Error:', err.message);
                console.error('🔍 Check your BOT_TOKEN in Railway environment variables. Current token starts with:', BOT_TOKEN ? BOT_TOKEN.substring(0, 5) + '...' : 'MISSING');
            });
    }
});

server.on('error', (err) => {
    if (err.code === 'EADDRINUSE') {
        console.error(`❌ Port ${PORT} is already in use. Trying port ${PORT + 1}...`);
        app.listen(PORT + 1, '0.0.0.0', () => console.log(`🚀 Alex: Sales Agent live on fallback port ${PORT + 1}`));
    } else {
        console.error('❌ Server error:', err.message);
        process.exit(1);
    }
});

// Graceful shutdown
process.once('SIGINT', () => { if (bot) bot.stop('SIGINT'); process.exit(0); });
process.once('SIGTERM', () => { if (bot) bot.stop('SIGTERM'); process.exit(0); });