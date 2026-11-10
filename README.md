# 🎬 Creator Script Coach · 创作者脚本教练

写完短视频稿先让它挑一轮毛病：**前三秒钩子、句子与段落、口播时长、模板词、结尾行动**。脚本按明确规则检查，再给出可以交给 Grok Bot 的修改提示词。

这是可运行的本地检查器，不需要API；不虚构“AI预测完播率”。

## Windows 10 上手

1. 安装 Python 3.10+，下载ZIP解压。
2. 用记事本打开 `examples/script.txt`，替换成自己的短视频脚本。
3. 双击 `启动工具.bat`，选择检查60秒脚本，阅读 `reports/script-report.md`。
4. 把报告里的修改要求交给 Grok Bot 让它出优化版，再回到本地做对照。

```bash
python -m creator_script_coach coach --file examples/script.txt --duration 60 --output reports
python -m creator_script_coach compare --before examples/script.txt --after examples/script-edited.txt --duration 60
python -m unittest discover -s tests -v
```

## 能力边界

- ✅ 可解释、可重复的脚本结构检查，文本时长粗估，修改前后指标对比。
- ✅ 导出 Markdown 报告+JSON结果，可交给不同AI修改。
- ❌ 不会自动生成新的视频或实际预测留存率。
- ❌ 100分是本地规则分，不表示爆款；不替代真人试读。
- ❌ 未接入 X/YouTube/TikTok 后台，不会从播放数据推断下一条真实成绩。

默认离线，不读取敏感账号。MIT · [@0xMulight](https://github.com/0xMulight)
