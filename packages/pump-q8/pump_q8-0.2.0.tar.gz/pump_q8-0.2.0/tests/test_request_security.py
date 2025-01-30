import asyncio
import unittest
import sys
import os

# إضافة مسار المشروع
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.request_manager.request_handler import (
    RequestOrchestrator, 
    RequestType, 
    RequestPriority, 
    RequestContext
)

class TestRequestSecurity(unittest.TestCase):
    def setUp(self):
        """
        إعداد بيئة الاختبار
        """
        self.orchestrator = RequestOrchestrator()
    
    async def test_request_context_creation(self):
        """
        اختبار إنشاء سياق الطلب بأمان
        """
        context = RequestContext(
            request_id='test_request',
            type=RequestType.TRADING,
            priority=RequestPriority.MEDIUM,
            metadata={
                'symbols': ['BTC/USDT'],
                'sensitive_data': 'should_be_filtered'
            }
        )
        
        # التحقق من خصائص السياق
        self.assertEqual(context.request_id, 'test_request')
        self.assertEqual(context.type, RequestType.TRADING)
        self.assertEqual(context.priority, RequestPriority.MEDIUM)
        
        # التأكد من تصفية البيانات الحساسة
        self.assertIn('symbols', context.metadata)
        self.assertNotIn('sensitive_data', context.metadata)
    
    async def test_request_priority_handling(self):
        """
        اختبار معالجة أولويات الطلبات
        """
        # إنشاء طلبات بأولويات مختلفة
        requests = [
            (RequestType.NFT, RequestPriority.LOW),
            (RequestType.TRADING, RequestPriority.HIGH),
            (RequestType.SECURITY, RequestPriority.CRITICAL)
        ]
        
        # تتبع الطلبات المنفذة
        executed_requests = []
        
        async def mock_handler(context):
            executed_requests.append((context.type, context.priority))
            return True
        
        # استبدال المعالجات الأصلية بمعالج وهمي
        self.orchestrator.handlers = {
            req_type: mock_handler for req_type, _ in requests
        }
        
        # تقديم الطلبات
        for req_type, priority in requests:
            await self.orchestrator.submit_request(
                req_type, 
                priority=priority
            )
        
        # انتظار معالجة الطلبات
        await self.orchestrator.request_queue.start()
        
        # التحقق من ترتيب التنفيذ
        # يجب أن تكون الطلبات مرتبة حسب الأولوية
        self.assertEqual(len(executed_requests), len(requests))
        self.assertEqual(
            executed_requests[0][1], 
            RequestPriority.CRITICAL
        )
    
    async def test_request_metadata_sanitization(self):
        """
        اختبار تنظيف بيانات الطلب
        """
        # بيانات طلب تحتوي على معلومات حساسة
        unsafe_metadata = {
            'api_key': 'secret_key_123',
            'password': 'admin_pass',
            'safe_data': ['BTC/USDT']
        }
        
        # إنشاء سياق الطلب
        context = RequestContext(
            request_id='sanitization_test',
            type=RequestType.TRADING,
            metadata=unsafe_metadata
        )
        
        # التحقق من تنظيف البيانات
        self.assertNotIn('api_key', context.metadata)
        self.assertNotIn('password', context.metadata)
        self.assertIn('safe_data', context.metadata)
    
    def test_request_type_validation(self):
        """
        اختبار التحقق من صحة نوع الطلب
        """
        with self.assertRaises(ValueError):
            # محاولة إرسال طلب بنوع غير موجود
            asyncio.run(
                self.orchestrator.submit_request(
                    'INVALID_REQUEST_TYPE',  # نوع غير صالح
                    priority=RequestPriority.MEDIUM
                )
            )

if __name__ == '__main__':
    unittest.main()
