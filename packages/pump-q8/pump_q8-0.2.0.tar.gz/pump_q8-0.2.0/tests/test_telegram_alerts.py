import os
import asyncio
import unittest
from unittest.mock import AsyncMock, patch

# إضافة مسار المشروع
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.notifications.telegram_alert_system import TelegramAlertSystem

class TestTelegramAlertSystem(unittest.TestCase):
    def setUp(self):
        """
        إعداد بيئة الاختبار
        """
        # إعداد متغيرات بيئية للاختبار
        os.environ['TELEGRAM_BOT_TOKEN'] = 'test_token'
        os.environ['TELEGRAM_CHAT_ID'] = 'test_chat_id'
        
        self.alert_system = TelegramAlertSystem()
    
    @patch('telegram.Bot')
    @patch('telegram.ext.Application')
    async def test_initialization(self, mock_application, mock_bot):
        """
        اختبار تهيئة نظام التنبيهات
        """
        # تهيئة البوت
        result = await self.alert_system.initialize()
        
        # التحقق من النتيجة
        self.assertTrue(result)
        mock_bot.assert_called_once_with(token='test_token')
        mock_application.builder().token().build.assert_called_once()
    
    @patch('telegram.Bot.send_message')
    async def test_send_alert(self, mock_send_message):
        """
        اختبار إرسال التنبيهات
        """
        # إعداد البوت المزيف
        mock_send_message.return_value = AsyncMock()
        
        # تهيئة البوت
        await self.alert_system.initialize()
        
        # إرسال تنبيه
        result = await self.alert_system.send_alert(
            "اختبار التنبيه", 
            alert_type='TEST'
        )
        
        # التحقق من النتيجة
        self.assertTrue(result)
        mock_send_message.assert_called_once()
    
    @patch('telegram.Bot.send_message')
    async def test_send_alert_without_initialization(self, mock_send_message):
        """
        اختبار محاولة إرسال تنبيه قبل التهيئة
        """
        # محاولة إرسال تنبيه دون تهيئة
        result = await self.alert_system.send_alert("تنبيه غير مهيأ")
        
        # التحقق من النتيجة
        self.assertFalse(result)
        mock_send_message.assert_not_called()
    
    async def test_multiple_alerts(self):
        """
        اختبار إرسال عدة تنبيهات
        """
        # تهيئة البوت
        await self.alert_system.initialize()
        
        # قائمة التنبيهات للاختبار
        alerts = [
            {"message": "تنبيه 1", "type": "INFO"},
            {"message": "تنبيه 2", "type": "WARNING"},
            {"message": "تنبيه 3", "type": "CRITICAL"}
        ]
        
        # إرسال التنبيهات
        results = []
        for alert in alerts:
            result = await self.alert_system.send_alert(
                alert['message'], 
                alert_type=alert['type']
            )
            results.append(result)
        
        # التحقق من النتائج
        self.assertTrue(all(results))
    
    def tearDown(self):
        """
        تنظيف بيئة الاختبار
        """
        # إزالة المتغيرات البيئية
        del os.environ['TELEGRAM_BOT_TOKEN']
        del os.environ['TELEGRAM_CHAT_ID']

if __name__ == '__main__':
    unittest.main()
