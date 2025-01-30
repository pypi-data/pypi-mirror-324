import unittest
import time
import psutil
import memory_profiler

from src.main import PumpQ8Application
from src.trading.automated_trading_system import AutomatedTradingSystem
from src.nft.nft_market_analyzer import NFTMarketAnalyzer

class TestPumpQ8Performance(unittest.TestCase):
    def setUp(self):
        """
        إعداد بيئة الاختبار
        """
        self.app = PumpQ8Application()
    
    def test_trading_system_performance(self):
        """
        اختبار أداء نظام التداول
        """
        start_time = time.time()
        start_memory = memory_profiler.memory_usage()[0]
        
        # تشغيل استراتيجية التداول
        self.app.trading_system.run_trading_strategy(['BTC/USDT'])
        
        end_time = time.time()
        end_memory = memory_profiler.memory_usage()[0]
        
        # قياس الأداء
        execution_time = end_time - start_time
        memory_usage = end_memory - start_memory
        
        print(f"\nوقت تنفيذ التداول: {execution_time:.2f} ثانية")
        print(f"استهلاك الذاكرة: {memory_usage:.2f} ميجابايت")
        
        # التأكد من أن الأداء ضمن المعايير
        self.assertLess(execution_time, 10)  # أقل من 10 ثواني
        self.assertLess(memory_usage, 500)   # أقل من 500 ميجابايت
    
    def test_nft_analyzer_performance(self):
        """
        اختبار أداء محلل NFT
        """
        start_time = time.time()
        start_memory = memory_profiler.memory_usage()[0]
        
        # توليد تقرير NFT
        nft_report = self.app.nft_analyzer.generate_nft_report()
        
        end_time = time.time()
        end_memory = memory_profiler.memory_usage()[0]
        
        # قياس الأداء
        execution_time = end_time - start_time
        memory_usage = end_memory - start_memory
        
        print(f"\nوقت توليد تقرير NFT: {execution_time:.2f} ثانية")
        print(f"استهلاك الذاكرة: {memory_usage:.2f} ميجابايت")
        
        # التأكد من أن الأداء ضمن المعايير
        self.assertLess(execution_time, 5)   # أقل من 5 ثواني
        self.assertLess(memory_usage, 300)   # أقل من 300 ميجابايت
        
        # التحقق من محتوى التقرير
        self.assertIn('trending_nfts', nft_report)
        self.assertIn('market_summary', nft_report)
    
    def test_cpu_usage(self):
        """
        اختبار استخدام وحدة المعالجة المركزية
        """
        # تشغيل عمليات متعددة
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = [
                executor.submit(self.app.trading_system.run_trading_strategy, ['BTC/USDT']),
                executor.submit(self.app.nft_analyzer.generate_nft_report)
            ]
            
            # انتظار اكتمال العمليات
            wait(futures)
        
        # قياس استخدام وحدة المعالجة المركزية
        cpu_percent = psutil.cpu_percent(interval=1)
        print(f"\nاستخدام وحدة المعالجة المركزية: {cpu_percent}%")
        
        # التأكد من أن استخدام وحدة المعالجة المركزية معقول
        self.assertLess(cpu_percent, 80)  # أقل من 80%

if __name__ == '__main__':
    unittest.main()
