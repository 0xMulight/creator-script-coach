import unittest
from creator_script_coach.__main__ import analyze,report,compare
class CoachTests(unittest.TestCase):
 def test_report(self):
  a=analyze('这个工具能省掉几步？\n\n第一步准备素材。\n\n试试后告诉我。',60)
  self.assertGreaterEqual(a['score'],0);self.assertLessEqual(a['score'],100)
  self.assertIn('不能预测留存率',report(a))
 def test_overlong(self):
  a=analyze('这是一个很长的脚本。'*100,10)
  self.assertTrue(any(o['check']=='预计时长' for o in a['issues']))
 def test_compare(self):
  self.assertIn('修改前',compare('你好！','你好，试试吧。',60))
 def test_invalid(self):
  with self.assertRaises(ValueError):analyze('',60)

if __name__=='__main__':unittest.main()
