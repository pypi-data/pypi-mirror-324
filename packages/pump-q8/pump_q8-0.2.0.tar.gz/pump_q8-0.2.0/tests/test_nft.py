import unittest
import pandas as pd
from datetime import timedelta
from src.nft.nft_market_analyzer import NFTMarketAnalyzer

class TestNFTMarketAnalyzer(unittest.TestCase):
    def setUp(self):
        self.nft_analyzer = NFTMarketAnalyzer()
    
    def test_fetch_nft_collections(self):
        """اختبار جلب مجموعات NFT"""
        for platform in ['opensea', 'rarible', 'magiceden']:
            collections = self.nft_analyzer.fetch_nft_collections(platform)
            
            self.assertIsInstance(collections, pd.DataFrame)
            self.assertTrue(len(collections) > 0)
    
    def test_collection_performance(self):
        """اختبار تحليل أداء مجموعة NFT"""
        test_collection = 'test-collection'
        test_platform = 'opensea'
        
        performance = self.nft_analyzer.analyze_collection_performance(
            test_collection, 
            test_platform
        )
        
        self.assertIn('floor_price', performance)
        self.assertIn('total_volume', performance)
        self.assertIn('total_sales', performance)
    
    def test_trending_nfts(self):
        """اختبار اكتشاف NFTs الرائجة"""
        trending_nfts = self.nft_analyzer.detect_trending_nfts(
            time_range=timedelta(days=1)
        )
        
        self.assertIsInstance(trending_nfts, list)
        
        if trending_nfts:
            first_nft = trending_nfts[0]
            self.assertIn('platform', first_nft)
            self.assertIn('collection_name', first_nft)
            self.assertIn('performance', first_nft)
    
    def test_nft_report_generation(self):
        """اختبار توليد تقرير NFT"""
        nft_report = self.nft_analyzer.generate_nft_report()
        
        self.assertIn('report_timestamp', nft_report)
        self.assertIn('trending_nfts', nft_report)
        self.assertIn('market_summary', nft_report)

if __name__ == '__main__':
    unittest.main()
