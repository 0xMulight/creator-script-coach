"""Local transparent heuristic short-video script coach. No LLM, no fabricated retention."""
import argparse
import json
from pathlib import Path
import re

PUNCT=re.compile(r'[。！？!?；;]')
HAN=re.compile(r'[\u4e00-\u9fff]')
TOKEN=re.compile(r'[\u4e00-\u9fff]|[A-Za-z0-9]+')
BANNED=['旨在','赋能','打造','范式','说白了','值得一提的是','综上所述']


def load_text(path):
    p=Path(path)
    if not p.is_file():raise ValueError('找不到脚本文件：'+str(path))
    if p.stat().st_size>2*1024*1024:raise ValueError('脚本文件不得超过2MB')
    return p.read_text(encoding='utf-8-sig').strip()

def n_units(text):return len(TOKEN.findall(text))

def analyze(text,duration=60,platform='short-video'):
    if not 10<=duration<=3600:raise ValueError('duration需在10至3600秒之间')
    if not text.strip():raise ValueError('脚本不能为空')
    paras=[s.strip() for s in re.split(r'\n+',text) if s.strip()]
    first=paras[0]
    sentences=[s.strip() for s in PUNCT.split(text) if s.strip()]
    units=n_units(text)
    han=len(HAN.findall(text));latin=units-han
    # 粗估：中文朗读3.5汉字/秒、英文2.5词/秒，忽略沉默和镜头停顿
    estimate=round(han/3.5+latin/2.5,1)
    checks=[];score=100
    def check(name,issue,penalty,action):
        nonlocal score
        if issue:
            score-=penalty;checks.append({'check':name,'points_lost':penalty,'suggestion':action})
    check('首句钩子',n_units(first)>45,12,'首句超过45字词单位，试着把最值得关注的问题提到第一句。')
    check('首句信息',not any(k in first for k in '？?！!0123456789') and n_units(first)<10,8,'首句较短且信息少：加入明确对象或具体问题，不硬编数据。')
    check('预计时长',estimate>duration*1.15,18,f'粗估口播{estimate}秒，超过目标{duration}秒。优先删重复段落或重新确定时长。')
    check('内容太短',estimate<duration*0.35,10,f'粗估口播{estimate}秒，可能明显短于目标{duration}秒；检查是否缺关键步骤。')
    check('长句',any(n_units(s)>65 for s in sentences),12,'发现很长的句子，可以拆句并安排镜头转折。')
    check('长段落',any(n_units(p)>120 for p in paras),10,'段落过长，建议拆成镜头/字幕可读的短段。')
    cliché=[w for w in BANNED if w in text]
    check('模板词',bool(cliché),6,f'出现：{"、".join(cliché)}。仅建议按自己的口吻检查。')
    check('结尾动作',not any(k in text[-90:] for k in ['收藏','关注','评论','试试','告诉我','你觉得','你们','下一步','怎么做','检查','注意']),5,'结尾可以给明确的下一步，避免强行求关注。')
    return {'platform':platform,'duration_seconds':duration,'estimated_spoken_seconds':estimate,'note':'非预测分数；本地启发式文本检查，未测真实播放/留存',
      'score':max(0,score),'units':units,'paragraphs':len(paras),'issues':checks,
      'opening':first[:90],'cliches':cliché,'sentence_count':len(sentences)}

def report(a):
    s=['# 脚本教练 · 本地诊断报告','',f'**规则检查分数：{a["score"]}/100**（仅内部编辑参考，不是爆款概率）','',
       f'- 平台：{a["platform"]}，目标时长：{a["duration_seconds"]}秒',
       f'- 文本字词单位：{a["units"]}；段落：{a["paragraphs"]}；句子：{a["sentence_count"]}',
       f'- 粗估口播时长：{a["estimated_spoken_seconds"]}秒（不同语言、语速、停顿会有偏差）','',
       '## 优先检查']
    if a['issues']:
        s += [f'{i}. **{o["check"]}**（规则扣{o["points_lost"]}分）：{o["suggestion"]}' for i,o in enumerate(a['issues'],1)]
    else:s.append('未发现本地规则问题；还需人工审稿、试听、事实核对。')
    s += ['','## 给AI的修改提示词','',
      '下面是我的脚本和机械检查报告。只修正已发现的缺点，保持我的用词和真实材料，不要编造数据、案例、经历或来源。请先给3条具体修改建议，再提供一份优化稿；如需更改事实，先问我。','',
      '## 发布前仍需人工检查','',
      '- 钩子是否真正有效，不能只看规则分；给真人试看并记录反馈。',
      '- 素材版权、口播节奏、画面可实现性与信息准确性必须人工确认。',
      '- 这份报告没有读取任何平台后台，不能预测留存率或播放量。','']
    return '\n'.join(s)

def compare(before,after,duration):
    a=analyze(before,duration);b=analyze(after,duration)
    return '# 脚本修改前后对照\n\n| 指标 | 修改前 | 修改后 |\n|---|---:|---:|\n'+f'| 编辑规则分 | {a["score"]} | {b["score"]} |\n| 粗估口播秒数 | {a["estimated_spoken_seconds"]} | {b["estimated_spoken_seconds"]} |\n| 触发问题数 | {len(a["issues"])} | {len(b["issues"])} |\n\n> 分数变化不代表观众留存或视频表现。\n'

def main(argv=None):
    p=argparse.ArgumentParser(description='Creator Script Coach - 可解释的脚本质检')
    sub=p.add_subparsers(dest='cmd',required=True)
    q=sub.add_parser('coach');q.add_argument('--file',required=True);q.add_argument('--duration',type=int,default=60);q.add_argument('--platform',choices=['short-video','youtube','x','podcast'],default='short-video');q.add_argument('--output',default='reports')
    q=sub.add_parser('compare');q.add_argument('--before',required=True);q.add_argument('--after',required=True);q.add_argument('--duration',type=int,default=60);q.add_argument('--output',default='reports/compare.md')
    a=p.parse_args(argv)
    if a.cmd=='coach':
        r=analyze(load_text(a.file),a.duration,a.platform);out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
        (out/'script-report.md').write_text(report(r),encoding='utf-8');(out/'script-analysis.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
        print('生成：',out/'script-report.md','、',out/'script-analysis.json','，规则分：',r['score'])
    else:
        out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(compare(load_text(a.before),load_text(a.after),a.duration),encoding='utf-8');print('生成：',out)

if __name__=='__main__':
    try:main()
    except (ValueError,OSError) as e:raise SystemExit(f'错误：{e}')
