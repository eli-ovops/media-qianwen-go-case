import subprocess,json,pathlib
P='/Users/USER/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
S='/Users/USER/.codex/skills/fred-remotion-output/scripts/references.py'
D=pathlib.Path(__file__).parent
for name,q in [('fees','商品 优惠 费用 多项汇合 总价 计算'),('reminder','界面 点击 开关 反馈'),('fees-installed','费用 汇合 总结')]:
 args=[P,S,'--query',q,'--limit','3','--full']
 if name.endswith('installed'): args+=['--access','installed']
 data=json.loads(subprocess.check_output(args))
 (D/f'{name}-top3.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
 print(name,q)
 for e in data['entries']:
  print(e['candidateId'],e['title'],e.get('sourceAvailability'),[s['path'] for s in e.get('sourceFiles',[])][:2],e['previews'][0].get('keyframes'))
