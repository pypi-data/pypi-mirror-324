# Pump Q8 🚀

## نظام تداول العملات الرقمية المتقدم

### 🌟 الميزات الرئيسية
- تداول تلقائي متقدم
- تحليل سوق NFT
- نظام تنبيهات ذكي
- إدارة محفظة آمنة
- نماذج تنبؤ باستخدام التعلم الآلي

### 🔧 المتطلبات
- Python 3.9+
- مفاتيح API (Binance, Telegram)

### 🚀 التثبيت
```bash
# استنساخ المشروع
git clone https://github.com/yourusername/pump_q8.git

# إنشاء بيئة افتراضية
python -m venv venv
source venv/bin/activate  # على Linux/macOS
venv\Scripts\activate     # على Windows

# تثبيت التبعيات
pip install -r requirements.txt
pip install -e .
```

### 🔐 الإعداد
1. إنشاء ملف `.env`
2. إضافة مفاتيح API
```
BINANCE_API_KEY=your_key
BINANCE_API_SECRET=your_secret
TELEGRAM_BOT_TOKEN=your_token
```

### 🧪 الاختبار
```bash
pytest tests/
coverage run -m pytest
```

### 🤖 التشغيل
```bash
python -m src.main
```

### 🤝 المساهمة
1. إنشاء fork للمشروع
2. إنشاء branch جديد
3. تقديم Pull Request

### 📜 الترخيص
MIT License
