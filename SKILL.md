---
name: creator-script-coach
description: Evaluate short video scripts locally for opening hook, pacing, speech duration and editable weaknesses; return transparent feedback and revisions prompt, without fake performance predictions.
license: MIT
compatibility: Python 3.10+; Windows 10/macOS/Linux; local command execution only
metadata:
  author: "0xMulight"
  version: "1.0.0"
---

# Creator Script Coach

## 使用时机

当用户提供短视频脚本，希望检查钩子、语速、结构、重复句、容易读不通顺的地方，并做人工确认之后的修改。

## 步骤

1. 收集脚本正文，明确目标平台/时长；只使用作者授权素材。
2. 在可运行Python3.10+的环境里，从仓库根目录执行：
   `python -m creator_script_coach coach --file examples/script.txt --duration 60 --output reports`
3. 读取 `reports/script-report.md`；指出具体规则触发项。一定说明分数是编辑启发式，不是播放量或留存预测。
4. 先给出3条具体修改建议，再在用户许可下提供保留原文语气的修改稿。数字和事实不确定时注明待核实。
5. 用 `python -m creator_script_coach compare --before examples/script.txt --after examples/script-edited.txt --duration 60` 核查规则变化。
6. 真人试看、确认音乐/图片版权和完成度后，才允许交付发布。

## 验收和限制

- 报告的时长必须注明是粗估，不能根据本地文本推测用户真实粉丝表现。
- 没有文件执行权限时，直接按同一检查清单做文字审校，不宣称脚本已执行。
- 不自动发布、不要求账号权限。

