/* ============================================================
   Open Humana – Landing Page JS
   Handles: nav, scroll animations, dropdowns, mobile menu,
            hero canvas, lead CTA, and Alex chat widget
   ============================================================ */

(function () {
  'use strict';

  /* ---------- NAV SCROLL ---------- */
  const nav = document.querySelector('.nav');
  const navProgress = document.getElementById('navProgress');

  function onScroll() {
    const scrollY = window.scrollY;
    if (nav) nav.classList.toggle('scrolled', scrollY > 60);
    if (navProgress) {
      const docH = document.documentElement.scrollHeight - window.innerHeight;
      var progress = docH > 0 ? Math.min(scrollY / docH, 1) : 0;
      navProgress.style.transform = 'scaleX(' + progress + ')';
    }
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---------- MOBILE MENU ---------- */
  const navMobile = document.getElementById('navMobile');
  const navLinks = document.getElementById('navLinks');

  if (navMobile && navLinks) {
    navMobile.addEventListener('click', function () {
      navMobile.classList.toggle('active');
      navLinks.classList.toggle('open');
    });
  }

  /* ---------- NAV DROPDOWNS ---------- */
  document.querySelectorAll('.nav-dropdown').forEach(function (dd) {
    var trigger = dd.querySelector('.nav-dropdown-trigger');
    if (!trigger) return;

    trigger.addEventListener('click', function (e) {
      e.preventDefault();
      var wasActive = dd.classList.contains('active');
      // close all
      document.querySelectorAll('.nav-dropdown.active').forEach(function (d) { d.classList.remove('active'); });
      if (!wasActive) dd.classList.add('active');
    });

    // clicking a mega-item with data-target scrolls to that section
    dd.querySelectorAll('.mega-item[data-target]').forEach(function (item) {
      item.addEventListener('click', function () {
        var target = document.getElementById(item.dataset.target);
        if (target) target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        dd.classList.remove('active');
        if (navLinks) navLinks.classList.remove('open');
        if (navMobile) navMobile.classList.remove('active');
      });
    });
  });

  // close dropdowns on outside click
  document.addEventListener('click', function (e) {
    if (!e.target.closest('.nav-dropdown')) {
      document.querySelectorAll('.nav-dropdown.active').forEach(function (d) { d.classList.remove('active'); });
    }
  });

  /* ---------- SCROLL ANIMATIONS ---------- */
  var animEls = document.querySelectorAll('.anim-fade, .anim-up');

  if ('IntersectionObserver' in window && animEls.length) {
    // add initial hidden state
    animEls.forEach(function (el) { el.style.opacity = '0'; el.style.transform = el.classList.contains('anim-up') ? 'translateY(32px)' : 'translateY(0)'; el.style.transition = 'opacity .7s ease, transform .7s ease'; });

    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.style.opacity = '1';
          entry.target.style.transform = 'translateY(0)';
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

    animEls.forEach(function (el) { observer.observe(el); });
  }

  /* ---------- HERO TITLE WORD REVEAL ---------- */
  var titleWords = document.querySelectorAll('.title-word');
  if (titleWords.length) {
    // Reveal words with staggered delay once the hero is in view
    var heroObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          titleWords.forEach(function (w) { w.classList.add('revealed'); });
          heroObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.2 });
    var heroSection = document.querySelector('.hero');
    if (heroSection) heroObserver.observe(heroSection);
  }

  /* ---------- HERO CANVAS (subtle particle effect) ---------- */
  var canvas = document.getElementById('heroCanvas');
  if (canvas) {
    var ctx = canvas.getContext('2d');
    var particles = [];
    var particleCount = 50;
    var animId;

    function resizeCanvas() {
      canvas.width = canvas.parentElement.offsetWidth;
      canvas.height = canvas.parentElement.offsetHeight;
    }
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);

    for (var i = 0; i < particleCount; i++) {
      particles.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        vx: (Math.random() - 0.5) * 0.3,
        vy: (Math.random() - 0.5) * 0.3,
        r: Math.random() * 1.5 + 0.5,
        a: Math.random() * 0.3 + 0.05
      });
    }

    function drawParticles() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      for (var j = 0; j < particles.length; j++) {
        var p = particles[j];
        p.x += p.vx;
        p.y += p.vy;
        if (p.x < 0) p.x = canvas.width;
        if (p.x > canvas.width) p.x = 0;
        if (p.y < 0) p.y = canvas.height;
        if (p.y > canvas.height) p.y = 0;
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(255,255,255,' + p.a + ')';
        ctx.fill();
      }
      // draw subtle connecting lines
      for (var a = 0; a < particles.length; a++) {
        for (var b = a + 1; b < particles.length; b++) {
          var dx = particles[a].x - particles[b].x;
          var dy = particles[a].y - particles[b].y;
          var dist = Math.sqrt(dx * dx + dy * dy);
          if (dist < 120) {
            ctx.beginPath();
            ctx.moveTo(particles[a].x, particles[a].y);
            ctx.lineTo(particles[b].x, particles[b].y);
            ctx.strokeStyle = 'rgba(255,255,255,' + (0.06 * (1 - dist / 120)) + ')';
            ctx.lineWidth = 0.5;
            ctx.stroke();
          }
        }
      }
      animId = requestAnimationFrame(drawParticles);
    }
    drawParticles();
  }

  /* ---------- SMOOTH SCROLL FOR ANCHOR LINKS ---------- */
  document.querySelectorAll('a[href^="#"]').forEach(function (a) {
    a.addEventListener('click', function (e) {
      var href = a.getAttribute('href');
      if (href === '#') return; // handled by data-open-lead
      var target = document.querySelector(href);
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  /* ---------- ALEX CHAT WIDGET ---------- */
  // Build DOM
  var chatHTML = '' +
    '<div class="alex-chat-bubble" id="alexBubble">' +
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/></svg>' +
      '<div class="alex-badge"></div>' +
    '</div>' +
    '<div class="alex-chat-window" id="alexWindow">' +
      '<div class="alex-chat-header">' +
        '<div class="alex-chat-avatar">A</div>' +
        '<div class="alex-chat-header-info">' +
          '<div class="alex-chat-header-name">Alex — Digital BDR</div>' +
          '<div class="alex-chat-header-status">Online now</div>' +
        '</div>' +
        '<button class="alex-chat-close" id="alexClose"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg></button>' +
      '</div>' +
      '<div class="alex-chat-messages" id="alexMessages">' +
        '<div class="alex-msg bot">Hi! I\'m Alex, your Digital BDR at Open Humana. How can I help you scale your outbound today?</div>' +
      '</div>' +
      '<div class="alex-chat-input-area">' +
        '<input class="alex-chat-input" id="alexInput" type="text" placeholder="Type your message..." autocomplete="off">' +
        '<button class="alex-chat-send" id="alexSend"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg></button>' +
      '</div>' +
    '</div>';

  var chatContainer = document.createElement('div');
  chatContainer.innerHTML = chatHTML;
  document.body.appendChild(chatContainer);

  var bubble = document.getElementById('alexBubble');
  var chatWindow = document.getElementById('alexWindow');
  var closeBtn = document.getElementById('alexClose');
  var messagesEl = document.getElementById('alexMessages');
  var inputEl = document.getElementById('alexInput');
  var sendBtn = document.getElementById('alexSend');

  function toggleChat() {
    chatWindow.classList.toggle('open');
    if (chatWindow.classList.contains('open')) {
      inputEl.focus();
    }
  }

  if (bubble) bubble.addEventListener('click', toggleChat);
  if (closeBtn) closeBtn.addEventListener('click', toggleChat);

  // data-open-lead buttons open the chat
  document.querySelectorAll('[data-open-lead]').forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      if (!chatWindow.classList.contains('open')) toggleChat();
    });
  });

  function addMessage(text, type) {
    var msg = document.createElement('div');
    msg.className = 'alex-msg ' + type;
    msg.textContent = text;
    messagesEl.appendChild(msg);
    messagesEl.scrollTop = messagesEl.scrollHeight;
    return msg;
  }

  function addTyping() {
    var msg = document.createElement('div');
    msg.className = 'alex-msg bot';
    msg.innerHTML = '<div class="typing-indicator"><span></span><span></span><span></span></div>';
    messagesEl.appendChild(msg);
    messagesEl.scrollTop = messagesEl.scrollHeight;
    return msg;
  }

  async function sendMessage() {
    var text = inputEl.value.trim();
    if (!text) return;
    inputEl.value = '';
    sendBtn.disabled = true;

    addMessage(text, 'user');
    var typingEl = addTyping();

    try {
      var resp = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text })
      });
      var data = await resp.json();
      typingEl.remove();
      addMessage(data.reply || data.error || 'Sorry, something went wrong.', 'bot');
    } catch (err) {
      typingEl.remove();
      addMessage('Connection error. Please try again.', 'bot');
    }
    sendBtn.disabled = false;
    inputEl.focus();
  }

  if (sendBtn) sendBtn.addEventListener('click', sendMessage);
  if (inputEl) inputEl.addEventListener('keydown', function (e) { if (e.key === 'Enter') sendMessage(); });

  /* ---------- REDDIT VOTE BUTTONS ---------- */
  document.querySelectorAll('.vote-btn').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var parent = btn.closest('.reddit-votes');
      var countEl = parent.querySelector('.vote-count');
      var count = parseInt(countEl.textContent, 10);

      if (btn.classList.contains('upvote')) {
        if (btn.classList.contains('active')) {
          btn.classList.remove('active');
          countEl.textContent = count - 1;
        } else {
          btn.classList.add('active');
          parent.querySelector('.downvote').classList.remove('active');
          countEl.textContent = count + 1;
        }
      } else {
        if (btn.classList.contains('active')) {
          btn.classList.remove('active');
          countEl.textContent = count + 1;
        } else {
          btn.classList.add('active');
          var upBtn = parent.querySelector('.upvote');
          if (upBtn.classList.contains('active')) {
            upBtn.classList.remove('active');
            countEl.textContent = count - 2;
          } else {
            countEl.textContent = count - 1;
          }
        }
      }
    });
  });

})();
