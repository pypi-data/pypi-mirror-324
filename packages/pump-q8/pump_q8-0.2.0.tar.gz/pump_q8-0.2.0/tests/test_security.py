import os
import unittest
import tempfile
from unittest.mock import patch, MagicMock

# إضافة مسار المشروع
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.security.api_key_manager import APIKeyManager

class TestAPIKeyManager(unittest.TestCase):
    def setUp(self):
        """
        إعداد بيئة اختبار لمدير المفاتيح
        """
        # إنشاء مجلد مؤقت للمفاتيح
        self.temp_dir = tempfile.mkdtemp()
        self.key_file = os.path.join(self.temp_dir, 'test_secret.key')
    
    def test_key_generation(self):
        """
        اختبار توليد المفتاح السري
        """
        # إنشاء مدير المفاتيح
        key_manager = APIKeyManager(key_file=self.key_file)
        
        # التأكد من وجود الملف
        self.assertTrue(os.path.exists(self.key_file))
        
        # التأكد من أن المفتاح له طول صحيح
        with open(self.key_file, 'rb') as f:
            key = f.read()
        
        self.assertEqual(len(key), 44)  # طول مفتاح Fernet القياسي
    
    def test_encryption_decryption(self):
        """
        اختبار تشفير وفك تشفير المفاتيح
        """
        key_manager = APIKeyManager(key_file=self.key_file)
        
        # مفتاح اختباري
        test_api_key = "test_api_key_12345"
        
        # التشفير
        encrypted_key = key_manager.encrypt_api_key(test_api_key)
        
        # فك التشفير
        decrypted_key = key_manager.decrypt_api_key(encrypted_key)
        
        # المقارنة
        self.assertEqual(test_api_key, decrypted_key)
    
    @patch.dict(os.environ, {
        'BINANCE_API_KEY': 'test_binance_key',
        'BINANCE_API_SECRET': 'test_binance_secret',
        'BINANCE_API_ENABLED': 'true'
    })
    def test_get_binance_credentials(self):
        """
        اختبار استرداد بيانات اعتماد Binance
        """
        key_manager = APIKeyManager(key_file=self.key_file)
        
        # استرداد بيانات الاعتماد
        credentials = key_manager.get_binance_credentials()
        
        # التحقق
        self.assertIsNotNone(credentials)
        self.assertIn('api_key', credentials)
        self.assertIn('api_secret', credentials)
    
    @patch.dict(os.environ, {
        'BINANCE_API_ENABLED': 'false'
    })
    def test_disabled_api_key(self):
        """
        اختبار حالة تعطيل المفاتيح
        """
        key_manager = APIKeyManager(key_file=self.key_file)
        
        # استرداد بيانات الاعتماد
        credentials = key_manager.get_binance_credentials()
        
        # التأكد من أن النتيجة None
        self.assertIsNone(credentials)
    
    def test_key_validation(self):
        """
        اختبار التحقق من صحة المفاتيح
        """
        key_manager = APIKeyManager(key_file=self.key_file)
        
        # مفاتيح اختبارية
        test_api_key = "test_key"
        test_api_secret = "test_secret"
        
        # التحقق
        result = key_manager.validate_api_key(test_api_key, test_api_secret)
        
        # المقارنة
        self.assertTrue(result)
    
    def test_invalid_decryption(self):
        """
        اختبار محاولة فك تشفير مفتاح غير صالح
        """
        key_manager = APIKeyManager(key_file=self.key_file)
        
        # محاولة فك تشفير مفتاح غير صالح
        invalid_key = b'invalid_encrypted_key'
        decrypted_key = key_manager.decrypt_api_key(invalid_key)
        
        # التأكد من أن النتيجة None
        self.assertIsNone(decrypted_key)
    
    def tearDown(self):
        """
        تنظيف الملفات المؤقتة
        """
        # حذف المجلد المؤقت وملفاته
        for file in os.listdir(self.temp_dir):
            os.unlink(os.path.join(self.temp_dir, file))
        os.rmdir(self.temp_dir)

# اختبارات إضافية للأمان
class TestSecurityFeatures(unittest.TestCase):
    def test_environment_variable_security(self):
        """
        التأكد من عدم تسرب المتغيرات الحساسة
        """
        # قائمة المتغيرات الممنوعة
        sensitive_vars = [
            'BINANCE_API_KEY', 
            'BINANCE_API_SECRET', 
            'TELEGRAM_BOT_TOKEN'
        ]
        
        # التأكد من عدم وجود المتغيرات في الكود المصدري
        def check_file_for_sensitive_data(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                for var in sensitive_vars:
                    self.assertNotIn(var, content, 
                        f"تم العثور على متغير حساس {var} في {file_path}")
        
        # فحص جميع ملفات Python
        for root, _, files in os.walk(os.path.join(os.path.dirname(__file__), '..')):
            for file in files:
                if file.endswith('.py'):
                    check_file_for_sensitive_data(os.path.join(root, file))

if __name__ == '__main__':
    unittest.main()
