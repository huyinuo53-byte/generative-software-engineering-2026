import urllib.request,pathlib,concurrent.futures,json
sources={
'ralph':'https://ghuntley.com/ralph/',
'ci':'https://martinfowler.com/articles/originalContinuousIntegration.html',
'cd':'https://continuousdelivery.com/2010/08/continuous-delivery-vs-continuous-deployment/',
'github-protection':'https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches',
'harness':'https://openai.com/index/harness-engineering/',
'minions':'https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2',
'compiler':'https://www.anthropic.com/engineering/building-c-compiler',
'strongdm':'https://factory.strongdm.ai/',
'dtu':'https://factory.strongdm.ai/techniques/dtu',
'friendster':'https://mysqldba.blogspot.com/2006/11/unorthodox-approach-to-database-design.html',
'webvan':'https://www.sec.gov/Archives/edgar/data/1092657/000101287001001485/0001012870-01-001485.txt',
'quibi':'https://quibi-hq.medium.com/an-open-letter-from-quibi-8af6b415377f',
'git-hooks':'https://git-scm.com/docs/githooks',
'github-pages':'https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages',
'github-deployments':'https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/control-deployments',
}
p=pathlib.Path('/tmp/gse08-materials');(p/'source-urls.json').write_text(json.dumps(sources,ensure_ascii=False,indent=2))
def get(item):
 k,u=item
 try:
  req=urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'})
  with urllib.request.urlopen(req,timeout=40) as r:b=r.read(); final=r.url
  (p/(k+'.html')).write_bytes(b);return k,len(b),final
 except Exception as e:return k,str(e)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
 for r in ex.map(get,sources.items()):print(r)
