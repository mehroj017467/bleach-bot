# Telegram Personaj Bot

Guruhda `/personajnomi` buyrug'iga javob qaytaruvchi Telegram bot.

---

## Fayllar

| Fayl | Maqsad |
|---|---|
| `main.py` | Bot logikasi |
| `characters.json` | Personajlar ma'lumotlari |
| `requirements.txt` | Python kutubxonalari |

---

## characters.json ni to'ldirish

```json
{
  "ikaku": {
    "image": "https://...",
    "text": "Bu yerga build + tavsif yozing"
  },
  "renji": {
    "image": "rasmlar/renji.jpg",
    "text": "Bu yerga build + tavsif yozing"
  }
}
```

- `image` — URL yoki lokal fayl yo'li (masalan `rasmlar/renji.jpg`)
- `text` — Markdown formatda matn (`*bold*`, `_italic_`)
- Yangi personaj qo'shish uchun faqat yangi kalit qo'shing — kod o'zgarmaydi

---

## Lokal ishga tushirish

```bash
pip install -r requirements.txt
export BOT_TOKEN="8622136588:AAFUjpf33Q62qKeP8FUT0Ruw1YWqlKXaZbw"
python main.py
```

Windows (CMD):
```cmd
set BOT_TOKEN=8622136588:AAFUjpf33Q62qKeP8FUT0Ruw1YWqlKXaZbw
python main.py
```

---

## Render.com ga deploy qilish

### 1. GitHub'ga yuklang

```bash
git init
git add .
git commit -m "telegram bot"
git remote add origin https://github.com/SIZNING_REPO
git push -u origin main
```

### 2. Render.com da yangi servis yarating

1. [render.com](https://render.com) ga kiring → **New → Web Service**
2. GitHub repo'yingizni tanlang
3. Quyidagi sozlamalarni kiriting:

| Maydon | Qiymat |
|---|---|
| **Runtime** | Python 3 |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `python main.py` |

### 3. Environment Variable qo'shing

Render dashboard → **Environment** bo'limi:

| Key | Value |
|---|---|
| `BOT_TOKEN` | `8622136588:AAFUjpf33Q62qKeP8FUT0Ruw1YWqlKXaZbw` |

### 4. Deploy bosing

Render avtomatik build qiladi va bot ishga tushadi.  
Health-check: `https://SIZNING_RENDER_URL/health`

---

## Guruhda botni faollashtirish

1. [@BotFather](https://t.me/BotFather) ga yozing → `/setprivacy` → botingizni tanlang → **Disable** qiling
2. Botni guruhga admin sifatida qo'shing (yoki oddiy a'zo sifatida — privacy o'chirilgandan keyin ishlaydi)
3. Guruhda `/ikaku` yoki boshqa personaj nomini yozing — bot javob beradi

---

## Yangi personaj qo'shish

`characters.json` fayliga yangi qator qo'shing:

```json
"zaraki": {
  "image": "https://example.com/zaraki.jpg",
  "text": "⚔️ *Zaraki — Build*\n\n• ATK: 2800+\n• Crit Rate: 55%+\n• Crit DMG: 180%+\n\n📌 *Tavsif:* ...",
}
```

Kodga hech narsa qo'shmasangiz ham `/zaraki` buyrug'i avtomatik ishlaydi.
