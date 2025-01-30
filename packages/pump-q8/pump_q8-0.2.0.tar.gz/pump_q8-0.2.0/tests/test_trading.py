import unittest
import pandas as pd
import numpy as np
from src.trading.automated_trading_system import AutomatedTradingSystem

class TestAutomatedTradingSystem(unittest.TestCase):
    def setUp(self):
        # إعداد نظام التداول للاختبار
        self.trading_system = AutomatedTradingSystem(
            exchange_name='binance',
            api_key='TEST_KEY',
            api_secret='TEST_SECRET'
        )
    
    def test_fetch_market_data(self):
        """اختبار جلب بيانات السوق"""
        market_data = self.trading_system.fetch_market_data('BTC/USDT')
        
        self.assertIsInstance(market_data, pd.DataFrame)
        self.assertTrue(len(market_data) > 0)
        self.assertTrue('timestamp' in market_data.columns)
    
    def test_market_analysis(self):
        """اختبار تحليل السوق"""
        # إنشاء بيانات مزيفة للاختبار
        test_data = pd.DataFrame({
            'close': np.random.random(100) * 10000,
            'volume': np.random.random(100) * 1000000
        })
        
        analysis = self.trading_system.analyze_market(test_data)
        
        self.assertIn('trend', analysis)
        self.assertIn('volatility', analysis)
        self.assertIn('momentum', analysis)
    
    def test_trade_signal_generation(self):
        """اختبار توليد إشارات التداول"""
        test_analysis = {
            'trend': 'bullish',
            'momentum': 0.05,
            'volatility': 0.03
        }
        
        signal = self.trading_system.generate_trade_signal(test_analysis)
        
        self.assertIn('action', signal)
        self.assertIn('confidence', signal)
        self.assertTrue(0 <= signal['confidence'] <= 1)

if __name__ == '__main__':
    unittest.main()
