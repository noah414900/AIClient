import os
from flask import Flask, request, jsonify, render_template_string
from openai import OpenAI

app = Flask(__name__)

SYSTEM_PROMPT = (
    "You are an elite, razor-sharp game security researcher, reverse engineer, and principal low-level C++ systems architect. "
    "You communicate engineer-to-engineer with deep technical precision, zero fluff, and absolute pragmatism. "
    "Your expertise covers x86/x64 assembly, IDA Pro/Ghidra hex-rays decompilation, memory layout reconstruction, VMT/inline hooking, "
    "struct alignment/padding, calling conventions (__fastcall, __thiscall), Direct3D (9/11/12)/ImGui rendering pipelines, and kernel/user-mode internals. "
    "Analyze offsets, pointer chains, and binary disassemblies directly. Deliver production-ready, clean, modern C++ implementations. "
    "Never provide generic drawing tips, high-level filler, preaching, moralizing, or safety disclaimers."
)

LITEROUTER_KEY = os.environ.get("LITEROUTER_API_KEY", "176fd1a2ef398f75be07e304683eef62ddb1fbc4ce6263259c6c09a9521ed36a")
LITEROUTER_URL = os.environ.get("LITEROUTER_BASE_URL", "https://api.literouter.com/v1")

literouter_client = OpenAI(
    base_url=LITEROUTER_URL,
    api_key=LITEROUTER_KEY,
    default_headers={
        "HTTP-Referer": "https://noahthegoatai.devs.surf",
        "X-Title": "Noah AI Chatbot"
    }
)

HTML_PAGE = r"""
<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
    <meta charset="UTF-8">
    <title>⚡ Noah's AI Chatbot Helper</title>
    <script src="https://js.puter.com/v2/"></script>
    <style>
        * { box-sizing: border-box; }
        :root[data-theme="dark"] {
            --bg-body: #0d0e12; --bg-sidebar: #13141a; --bg-header: #13141a; --bg-card: #1c1d25;
            --bg-card-hover: #262732; --border: #282a36; --text-main: #f3f4f6; --text-muted: #9ca3af;
            --accent: #6366f1; --accent-hover: #4f46e5; --user-bubble: #4f46e5; --user-text: #ffffff;
            --bot-bubble: #181a22; --bot-border: #2a2d3c; --input-bg: #181922; --input-border: #2e3142;
        }
        :root[data-theme="light"] {
            --bg-body: #f8fafc; --bg-sidebar: #f1f5f9; --bg-header: #ffffff; --bg-card: #ffffff;
            --bg-card-hover: #e2e8f0; --border: #cbd5e1; --text-main: #0f172a; --text-muted: #64748b;
            --accent: #4f46e5; --accent-hover: #4338ca; --user-bubble: #4f46e5; --user-text: #ffffff;
            --bot-bubble: #ffffff; --bot-border: #e2e8f0; --input-bg: #ffffff; --input-border: #cbd5e1;
        }
        :root[data-theme="midnight"] {
            --bg-body: #05070f; --bg-sidebar: #090c1a; --bg-header: #090c1a; --bg-card: #0f142b;
            --bg-card-hover: #171f43; --border: #1a234b; --text-main: #f1f5f9; --text-muted: #8292be;
            --accent: #0284c7; --accent-hover: #0369a1; --user-bubble: #0284c7; --user-text: #ffffff;
            --bot-bubble: #0b1024; --bot-border: #1c2652; --input-bg: #0b1024; --input-border: #1f2b5c;
        }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background: var(--bg-body); color: var(--text-main); margin: 0; display: flex; flex-direction: column; height: 100vh; overflow: hidden; }
        #header { height: 58px; background: var(--bg-header); border-bottom: 1px solid var(--border); display: flex; justify-content: space-between; align-items: center; padding: 0 20px; position: relative; flex-shrink: 0; box-shadow: 0 2px 10px rgba(0,0,0,0.15); }
        #header-title { position: absolute; left: 50%; transform: translateX(-50%); font-weight: 700; font-size: 1.15rem; letter-spacing: -0.01em; pointer-events: none; display: flex; align-items: center; gap: 8px; }
        #sidebar-toggle-title { font-weight: 600; font-size: 0.9rem; color: var(--text-muted); display: flex; align-items: center; gap: 6px; }
        .header-controls { display: flex; align-items: center; gap: 10px; }
        select { background: var(--bg-card); color: var(--text-main); border: 1px solid var(--border); padding: 7px 12px; border-radius: 8px; outline: none; font-size: 0.85rem; font-weight: 500; cursor: pointer; transition: all 0.2s; }
        select:hover { background: var(--bg-card-hover); }
        #puterBtn { background: var(--accent); color: #fff; border: none; padding: 7px 14px; border-radius: 8px; font-weight: 600; font-size: 0.85rem; cursor: pointer; transition: background 0.2s; }
        #puterBtn:hover { background: var(--accent-hover); }
        #app-body { display: flex; flex: 1; min-height: 0; overflow: hidden; }
        #sidebar { width: 260px; background: var(--bg-sidebar); border-right: 1px solid var(--border); display: flex; flex-direction: column; padding: 14px; gap: 10px; flex-shrink: 0; }
        .new-chat-btn { background: var(--bg-card); color: var(--text-main); border: 1px solid var(--border); border-radius: 8px; padding: 10px 14px; font-weight: 600; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 8px; font-size: 0.9rem; transition: background 0.2s, border-color 0.2s; }
        .new-chat-btn:hover { background: var(--bg-card-hover); border-color: var(--accent); }
        #chat-list { flex: 1; overflow-y: auto; display: flex; flex-direction: column; gap: 4px; padding-right: 4px; }
        .chat-item { padding: 10px 12px; border-radius: 8px; cursor: pointer; font-size: 0.88rem; color: var(--text-muted); display: flex; justify-content: space-between; align-items: center; transition: 0.15s; }
        .chat-item:hover { background: var(--bg-card-hover); color: var(--text-main); }
        .chat-item.active { background: var(--bg-card); color: var(--text-main); font-weight: 600; border-left: 3px solid var(--accent); }
        .chat-item-title { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; flex: 1; margin-right: 8px; }
        .del-btn { opacity: 0; background: none; border: none; color: #ef4444; font-size: 0.85rem; cursor: pointer; padding: 2px 6px; border-radius: 4px; }
        .chat-item:hover .del-btn { opacity: 1; }
        .del-btn:hover { background: rgba(239, 68, 68, 0.15); }
        #main-chat-area { flex: 1; display: flex; flex-direction: column; height: 100%; min-height: 0; background: var(--bg-body); position: relative; }
        #chat { flex: 1; overflow-y: auto; padding: 24px 20px; display: flex; flex-direction: column; align-items: center; gap: 18px; min-height: 0; }
        .chat-container { width: 100%; max-width: 860px; display: flex; flex-direction: column; gap: 16px; }
        .msg-wrapper { display: flex; flex-direction: column; width: 100%; }
        .msg-wrapper.user { align-items: flex-end; }
        .msg-wrapper.bot { align-items: flex-start; }
        .msg-header { display: flex; align-items: center; gap: 6px; margin-bottom: 4px; padding: 0 4px; }
        .copy-btn { background: transparent; border: none; color: var(--text-muted); cursor: pointer; padding: 2px 4px; border-radius: 4px; display: inline-flex; align-items: center; justify-content: center; opacity: 0.6; transition: opacity 0.2s, color 0.2s; }
        .copy-btn:hover { opacity: 1; color: var(--text-main); }
        .msg { max-width: 85%; padding: 14px 20px; border-radius: 12px; line-height: 1.55; font-size: 0.95rem; white-space: pre-wrap; font-family: inherit; word-break: break-word; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
        .msg.user { background: var(--user-bubble); color: var(--user-text); border-bottom-right-radius: 3px; }
        .msg.bot { background: var(--bot-bubble); color: var(--text-main); border: 1px solid var(--bot-border); border-bottom-left-radius: 3px; }
        .msg-sender { font-size: 0.72rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em; font-weight: bold; }
        #input-area { padding: 14px 20px 22px 20px; background: var(--bg-body); display: flex; justify-content: center; flex-shrink: 0; border-top: 1px solid var(--border); }
        .input-card { width: 100%; max-width: 860px; background: var(--input-bg); border: 1px solid var(--input-border); border-radius: 12px; display: flex; align-items: flex-end; padding: 8px 12px; gap: 10px; box-shadow: 0 4px 18px rgba(0,0,0,0.15); transition: border-color 0.2s; }
        .input-card:focus-within { border-color: var(--accent); }
        textarea { flex: 1; padding: 8px 10px; background: transparent; border: none; color: var(--text-main); outline: none; font-size: 0.96rem; resize: none; min-height: 48px; max-height: 200px; line-height: 1.45; font-family: inherit; }
        .send-btn { padding: 10px 20px; background: var(--accent); border: none; border-radius: 8px; color: white; font-weight: 600; cursor: pointer; transition: background 0.2s, transform 0.1s; height: 44px; display: flex; align-items: center; justify-content: center; }
        .send-btn:hover { background: var(--accent-hover); }
        .send-btn:active { transform: scale(0.98); }
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: rgba(150, 150, 150, 0.25); border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: rgba(150, 150, 150, 0.4); }
    </style>
</head>
<body>
    <div id="header">
        <div id="sidebar-toggle-title">💬 Sessions</div>
        <div id="header-title">⚡ Noah's AI Chatbot Helper</div>
        <div class="header-controls">
            <select id="themeSelect" onchange="changeTheme(this.value)">
                <option value="dark">🌙 Dark</option>
                <option value="midnight">🌌 Midnight</option>
                <option value="light">☀️ Light</option>
            </select>
            <button id="puterBtn" onclick="handlePuterLogin()">🔑 Connect Puter</button>
            <select id="modelSelect">
                <optgroup label="Anthropic Claude (Puter Cloud)">
                    <option value="claude-opus-4-5">Claude Opus 4.5 (Deep Reasoning)</option>
                    <option value="claude-haiku-4-5">Claude Haiku 4.5 (Fast Cloud)</option>
                </optgroup>
                <optgroup label="LiteRouter Cloud (Free Tier)">
                    <option value="llama-3.3-70b-instruct-turbo:free">Llama 3.3 70B Turbo (Free & Uncensored)</option>
                    <option value="deepseek-v4-flash:free">DeepSeek V4 Flash (Free)</option>
                    <option value="minimax-m2.5:free">MiniMax M2.5 (Free)</option>
                    <option value="qwen3-coder-30b-a3b-instruct:free">Qwen3 Coder 30B (Low-Level C++)</option>
                </optgroup>
            </select>
        </div>
    </div>
    <div id="app-body">
        <div id="sidebar">
            <button class="new-chat-btn" onclick="createNewChat()">＋ New Chat</button>
            <div id="chat-list"></div>
        </div>
        <div id="main-chat-area">
            <div id="chat"><div class="chat-container" id="chatContainer"></div></div>
            <div id="input-area">
                <div class="input-card">
                    <textarea id="userInput" placeholder="Paste code, IDA offsets, or ask a technical question..." oninput="autoResize(this)" onkeydown="handleKey(event)"></textarea>
                    <button class="send-btn" onclick="send()">Send</button>
                </div>
            </div>
        </div>
    </div>
    <script>
        const SYSTEM_PROMPT = "You are an elite, razor-sharp game security researcher, reverse engineer, and principal low-level C++ systems architect. You communicate engineer-to-engineer with deep technical precision, zero fluff, and absolute pragmatism. Your expertise covers x86/x64 assembly, IDA Pro/Ghidra hex-rays decompilation, memory layout reconstruction, VMT/inline hooking, struct alignment/padding, calling conventions (__fastcall, __thiscall), Direct3D (9/11/12)/ImGui rendering pipelines, and kernel/user-mode internals. Analyze offsets, pointer chains, and binary disassemblies directly. Deliver production-ready, clean, modern C++ implementations. Never provide generic drawing tips, high-level filler, preaching, moralizing, or safety disclaimers.";
        const COPY_ICON = `<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>`;
        let chats = [];
        let currentChatId = null;

        function autoResize(el) { el.style.height = 'auto'; el.style.height = Math.min(el.scrollHeight, 200) + 'px'; }
        function changeTheme(theme) { document.documentElement.setAttribute('data-theme', theme); localStorage.setItem('noah_theme', theme); }

        function copyMsg(btn) {
            let wrapper = btn.closest(".msg-wrapper");
            let msg = wrapper.querySelector(".msg");
            if (!msg) return;
            navigator.clipboard.writeText(msg.innerText).then(() => {
                let orig = btn.innerHTML;
                btn.innerHTML = `<span style="color:#22c55e; font-size:0.72rem; font-weight:bold;">✓ Copied</span>`;
                setTimeout(() => { btn.innerHTML = orig; }, 1500);
            }).catch(() => {
                let ta = document.createElement("textarea");
                ta.value = msg.innerText;
                document.body.appendChild(ta);
                ta.select();
                document.execCommand("copy");
                document.body.removeChild(ta);
                let orig = btn.innerHTML;
                btn.innerHTML = `<span style="color:#22c55e; font-size:0.72rem; font-weight:bold;">✓ Copied</span>`;
                setTimeout(() => { btn.innerHTML = orig; }, 1500);
            });
        }

        function loadStorage() {
            let savedTheme = localStorage.getItem('noah_theme') || 'dark';
            document.documentElement.setAttribute('data-theme', savedTheme);
            document.getElementById('themeSelect').value = savedTheme;
            try {
                let saved = localStorage.getItem("noah_chats");
                chats = saved ? JSON.parse(saved) : [];
                currentChatId = localStorage.getItem("noah_active_chat");
            } catch(e) { chats = []; currentChatId = null; }
            if (!chats || chats.length === 0) { createNewChat(); }
            else {
                if (!chats.find(c => c.id === currentChatId)) { currentChatId = chats[0].id; }
                saveStorage(); renderSidebar(); renderActiveChat();
            }
        }
        function saveStorage() { localStorage.setItem("noah_chats", JSON.stringify(chats)); localStorage.setItem("noah_active_chat", currentChatId); }

        function createNewChat() {
            let newId = "chat_" + Date.now();
            chats.unshift({ id: newId, title: "New Conversation", messages: [] });
            currentChatId = newId; saveStorage(); renderSidebar(); renderActiveChat();
        }
        function deleteChat(e, id) {
            e.stopPropagation(); chats = chats.filter(c => c.id !== id);
            if (chats.length === 0) { createNewChat(); }
            else { if (currentChatId === id) { currentChatId = chats[0].id; } saveStorage(); renderSidebar(); renderActiveChat(); }
        }
        function selectChat(id) { currentChatId = id; saveStorage(); renderSidebar(); renderActiveChat(); }

        function renderSidebar() {
            let list = document.getElementById("chat-list"); list.innerHTML = "";
            chats.forEach(c => {
                let item = document.createElement("div");
                item.className = "chat-item" + (c.id === currentChatId ? " active" : "");
                item.onclick = () => selectChat(c.id);
                let title = document.createElement("div"); title.className = "chat-item-title"; title.innerText = c.title || "New Conversation";
                let del = document.createElement("button"); del.className = "del-btn"; del.innerText = "✕"; del.onclick = (e) => deleteChat(e, c.id);
                item.appendChild(title); item.appendChild(del); list.appendChild(item);
            });
        }

        function renderActiveChat() {
            let container = document.getElementById("chatContainer"); container.innerHTML = "";
            let chat = chats.find(c => c.id === currentChatId);
            if (!chat || chat.messages.length === 0) {
                container.innerHTML = `<div class="msg-wrapper bot"><div class="msg-header"><div class="msg-sender">SYSTEM</div><button class="copy-btn" title="Copy message" onclick="copyMsg(this)">${COPY_ICON}</button></div><div class="msg bot">System online. Connect Puter at top right for Claude, or select Llama 3.3 / LiteRouter models to chat instantly.</div></div>`;
                return;
            }
            chat.messages.forEach(m => {
                let wrapper = document.createElement("div"); wrapper.className = "msg-wrapper " + (m.role === "user" ? "user" : "bot");
                let header = document.createElement("div"); header.className = "msg-header";
                let sender = document.createElement("div"); sender.className = "msg-sender"; sender.innerText = m.role === "user" ? "YOU" : (m.model || "AI");
                let copyBtn = document.createElement("button"); copyBtn.className = "copy-btn"; copyBtn.title = "Copy message"; copyBtn.innerHTML = COPY_ICON; copyBtn.onclick = () => copyMsg(copyBtn);
                header.appendChild(sender); header.appendChild(copyBtn);

                let bubble = document.createElement("div"); bubble.className = "msg " + (m.role === "user" ? "user" : "bot"); bubble.innerText = m.text;
                wrapper.appendChild(header); wrapper.appendChild(bubble); container.appendChild(wrapper);
            });
            document.getElementById("chat").scrollTop = document.getElementById("chat").scrollHeight;
        }

        async function checkPuterStatus() {
            try {
                if (puter.auth.isSignedIn()) {
                    let user = await puter.auth.getUser();
                    let btn = document.getElementById("puterBtn");
                    btn.innerText = "✅ " + (user.username || "Puter Connected");
                    btn.style.background = "#15803d";
                }
            } catch(e) {}
        }
        async function handlePuterLogin() {
            try { await puter.auth.signIn(); await checkPuterStatus(); }
            catch (err) { alert("Login closed or cancelled: " + (err.message || JSON.stringify(err))); }
        }

        function handleKey(e) { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send(); } }

        async function send() {
            let input = document.getElementById("userInput");
            let container = document.getElementById("chatContainer");
            let scrollArea = document.getElementById("chat");
            let model = document.getElementById("modelSelect").value;
            let text = input.value.trim();
            if(!text) return;

            input.value = ""; input.style.height = "48px";
            let active = chats.find(c => c.id === currentChatId);
            if (!active) { createNewChat(); active = chats.find(c => c.id === currentChatId); }
            if (active.messages.length === 0) {
                container.innerHTML = "";
                active.title = text.length > 25 ? text.substring(0, 25) + "..." : text;
                renderSidebar();
            }

            active.messages.push({ role: "user", text: text }); saveStorage();
            let userWrapper = document.createElement("div"); userWrapper.className = "msg-wrapper user";
            userWrapper.innerHTML = `<div class="msg-header"><div class="msg-sender">YOU</div><button class="copy-btn" title="Copy message" onclick="copyMsg(this)">${COPY_ICON}</button></div><div class="msg user">${escapeHtml(text)}</div>`;
            container.appendChild(userWrapper); scrollArea.scrollTop = scrollArea.scrollHeight;

            let botWrapper = document.createElement("div"); botWrapper.className = "msg-wrapper bot";
            let shortModel = model.replace("claude-", "Claude ").replace(":free", "");
            botWrapper.innerHTML = `<div class="msg-header"><div class="msg-sender">${escapeHtml(shortModel)}</div><button class="copy-btn" title="Copy message" onclick="copyMsg(this)">${COPY_ICON}</button></div><div class="msg bot">Thinking...</div>`;
            container.appendChild(botWrapper); scrollArea.scrollTop = scrollArea.scrollHeight;

            let botMsg = botWrapper.querySelector(".msg.bot");
            let replyText = "";

            if (model.startsWith("claude-")) {
                try {
                    if (!puter.auth.isSignedIn()) {
                        replyText = "⚠️ Please click '🔑 Connect Puter' at the top right to sign in first!";
                        botMsg.innerText = replyText;
                        active.messages.push({ role: "bot", text: replyText, model: shortModel });
                        saveStorage(); return;
                    }
                    let promptWithSys = SYSTEM_PROMPT + "\n\nUser Request:\n" + text;
                    let resp = await puter.ai.chat(promptWithSys, { model: model });
                    if (typeof resp === 'string') replyText = resp;
                    else if (resp?.message?.content) replyText = resp.message.content[0].text;
                    else if (resp?.text) replyText = resp.text;
                    else replyText = JSON.stringify(resp, null, 2);
                    botMsg.innerText = replyText;
                } catch(err) {
                    replyText = `${shortModel} Error: ` + (err.message || JSON.stringify(err));
                    botMsg.innerText = replyText;
                }
            } else {
                try {
                    let res = await fetch("/chat", {
                        method: "POST",
                        headers: {"Content-Type": "application/json"},
                        body: JSON.stringify({prompt: text, model: model})
                    });
                    let data = await res.json();
                    replyText = data.reply;
                    botMsg.innerText = replyText;
                } catch(err) {
                    replyText = "Error contacting server backend. Check Render deployment logs.";
                    botMsg.innerText = replyText;
                }
            }

            active.messages.push({ role: "bot", text: replyText, model: shortModel });
            saveStorage(); scrollArea.scrollTop = scrollArea.scrollHeight;
        }

        function escapeHtml(text) { return text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }
        window.addEventListener('load', () => { loadStorage(); checkPuterStatus(); });
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_PAGE)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json or {}
    prompt = data.get("prompt", "")
    chosen_model = data.get("model", "llama-3.3-70b-instruct-turbo:free")

    try:
        response = literouter_client.chat.completions.create(
            model=chosen_model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            temperature=0.6
        )
        return jsonify({"reply": response.choices[0].message.content})
    except Exception as e:
        return jsonify({"reply": f"API Error ({chosen_model}): {str(e)}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
