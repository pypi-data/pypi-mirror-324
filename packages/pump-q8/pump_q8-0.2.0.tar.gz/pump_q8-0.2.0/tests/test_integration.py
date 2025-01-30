import unittest
import sys
import os
import logging
from unittest.mock import patch, MagicMock

# إضافة مسار المشروع
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.main import PumpQ8Application
from src.trading.automated_trading_system import AutomatedTradingSystem
from src.nft.nft_market_analyzer import NFTMarketAnalyzer
from src.notifications.advanced_alert_system import AdvancedAlertSystem
from src.ml_prediction.market_prediction_model import MarketPredictionModel

class TestPumpQ8Integration(unittest.TestCase):
    def setUp(self):
        """
        إعداد بيئة الاختبار
        """
        # إنشاء نسخة من التطبيق باستخدام ملف تكوين اختباري
        self.test_config_path = os.path.join(
            os.path.dirname(__file__), 
            'test_config.yaml'
        )
        self.app = PumpQ8Application(config_path=self.test_config_path)
    
    def test_configuration_loading(self):
        """
        اختبار تحميل التكوينات
        """
        self.assertIsNotNone(self.app.config)
        self.assertIn('trading', self.app.config)
        self.assertIn('nft', self.app.config)
        self.assertIn('notifications', self.app.config)
    
    def test_component_initialization(self):
        """
        اختبار تهيئة المكونات
        """
        # اختبار نظام التداول
        self.assertIsInstance(
            self.app.trading_system, 
            AutomatedTradingSystem
        )
        
        # اختبار محلل NFT
        self.assertIsInstance(
            self.app.nft_analyzer, 
            NFTMarketAnalyzer
        )
        
        # اختبار نظام التنبيهات
        self.assertIsInstance(
            self.app.alert_system, 
            AdvancedAlertSystem
        )
        
        # اختبار نموذج التنبؤ
        self.assertIsInstance(
            self.app.prediction_model, 
            MarketPredictionModel
        )
    
    @patch('src.trading.automated_trading_system.AutomatedTradingSystem.run_trading_strategy')
    def test_trading_strategy_execution(self, mock_run_strategy):
        """
        اختبار تنفيذ استراتيجية التداول
        """
        self.app.run_trading_strategy()
        mock_run_strategy.assert_called_once()
    
    @patch('src.nft.nft_market_analyzer.NFTMarketAnalyzer.generate_nft_report')
    def test_nft_report_generation(self, mock_generate_report):
        """
        اختبار توليد تقرير NFT
        """
        mock_report = {
            'trending_nfts': [
                {'collection_name': 'Test Collection', 'platform': 'opensea'}
            ]
        }
        mock_generate_report.return_value = mock_report
        
        report = self.app.generate_nft_report()
        
        self.assertEqual(len(report['trending_nfts']), 1)
        self.assertEqual(
            report['trending_nfts'][0]['collection_name'], 
            'Test Collection'
        )
    
    @patch('src.notifications.advanced_alert_system.AdvancedAlertSystem.send_risk_alert')
    def test_risk_alert_system(self, mock_send_alert):
        """
        اختبار نظام التنبيهات
        """
        test_risky_assets = ['BTC', 'ETH']
        
        self.app.alert_system.send_risk_alert(
            portfolio_risk=0.7, 
            risky_assets=test_risky_assets
        )
        
        mock_send_alert.assert_called_once_with(
            portfolio_risk=0.7, 
            risky_assets=test_risky_assets
        )
    
    def test_logging_configuration(self):
        """
        اختبار تكوين التسجيل
        """
        logger = logging.getLogger()
        self.assertIsNotNone(logger)
        self.assertEqual(logger.level, logging.INFO)
    
    def tearDown(self):
        """
        تنظيف بيئة الاختبار
        """
        # إغلاق أي موارد مفتوحة
        pass

if __name__ == '__main__':
    unittest.main()
