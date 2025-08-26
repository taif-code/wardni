(function(){
  // alerts toggle is in dashboard template
  // Chatbot demo
  const toggle = document.getElementById('chatbot-toggle');
  const box = document.getElementById('chatbot');
  const close = document.getElementById('chat-close');
  const input = document.getElementById('chat-input');
  const send = document.getElementById('chat-send');
  const msgs = document.getElementById('chat-messages');
  if(!toggle) return;
  toggle.onclick = ()=> box.classList.toggle('hidden');
  close.onclick = ()=> box.classList.add('hidden');
  function push(who, text){
    const div = document.createElement('div');
    div.className = who === 'me' ? 'me' : 'bot';
    div.textContent = text;
    const wrap = document.createElement('div');
    wrap.appendChild(div);
    msgs.appendChild(wrap);
    msgs.scrollTop = msgs.scrollHeight;
  }
  function reply(q){
    const known = ['T-10234','T-10235','T-10236','T-10237'];
    if(known.includes(q.trim())){
      push('bot', q + ': حالة تجريبية — في الطريق • 10°C');
    }else if(/supplier|مورد|مزرعة/i.test(q)){
      push('bot', 'مزارع ورد الطائف – الهدا\nمزرعة الورود الحديثة – الشفا\nورد الطائف العضوي – السيل');
    }else{
      push('bot','رسالة تجريبية: أرسل رقم شحنة مثل T-10234');
    }
  }
  function sendMsg(){
    const v = (input.value || '').trim();
    if(!v) return;
    push('me', v);
    input.value='';
    setTimeout(()=>reply(v), 300);
  }
  send.onclick = sendMsg;
  input.addEventListener('keydown', e=>{ if(e.key==='Enter') sendMsg(); });
})();
document.addEventListener("DOMContentLoaded", function () {
  const langBtn = document.getElementById("lang-toggle");
  if (langBtn) {
    langBtn.addEventListener("click", () => {
      const html = document.documentElement;
      if (html.getAttribute("lang") === "ar") {
        // غيّر إلى الإنجليزية
        html.setAttribute("lang", "en");
        html.setAttribute("dir", "ltr");
        langBtn.textContent = "🌐 AR";

        // ترجمة سريعة (واجهة فقط)
        translateUI("en");
      } else {
        // غيّر إلى العربية
        html.setAttribute("lang", "ar");
        html.setAttribute("dir", "rtl");
        langBtn.textContent = "🌐 EN";

        // ترجمة سريعة (واجهة فقط)
        translateUI("ar");
      }
    });
  }
});

function translateUI(lang) {
  const dict = {
    ar: {
      "dashboard": "لوحة التحكم",
      "shipments": "الشحنات",
      "suppliers": "الموردون",
      "track": "تتبّع شحنة",
      "users": "المستخدمون",
      "login": "تسجيل الدخول",
      "manageShipments": "إدارة الشحنات",
      "trackShipment": "تتبّع الشحنة",
    },
    en: {
      "dashboard": "Dashboard",
      "shipments": "Shipments",
      "suppliers": "Suppliers",
      "track": "Track",
      "users": "Users",
      "login": "Login",
      "manageShipments": "Manage Shipments",
      "trackShipment": "Track Shipment",
    }
  };

  const t = dict[lang];
  if (!t) return;

  // عدّل النصوص حسب id
  const ids = Object.keys(t);
  ids.forEach(id => {
    const el = document.getElementById(id);
    if (el) el.textContent = t[id];
  });
}
