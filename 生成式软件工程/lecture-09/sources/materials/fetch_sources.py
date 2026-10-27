import concurrent.futures,urllib.request,json,hashlib,time,pathlib
R=pathlib.Path('/tmp/gse09-materials/sources')
rows=[
('aws-idempotent','https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/'),
('fowler-event','https://martinfowler.com/eaaDev/EventSourcing.html'),
('mapreduce','https://usenix.org/legacy/events/osdi04/tech/full_papers/dean/dean_html/index.html'),
('spark-rdd','https://spark.apache.org/docs/latest/rdd-programming-guide.html'),
('flink-time','https://nightlies.apache.org/flink/flink-docs-stable/docs/concepts/time/'),
('flink-state','https://nightlies.apache.org/flink/flink-docs-stable/docs/concepts/stateful-stream-processing/'),
('java-gc','https://docs.oracle.com/en/java/javase/25/gctuning/ergonomics.html'),
('php-fpm','https://www.php.net/manual/en/install.fpm.configuration.php'),
('apache-websocket','https://httpd.apache.org/docs/2.4/mod/mod_proxy_wstunnel.html'),
('vba','https://learn.microsoft.com/en-us/office/vba/library-reference/concepts/getting-started-with-vba-in-office/'),
('nasa','https://llis.nasa.gov/lesson/641'),
('brooks','https://worrydream.com/refs/Brooks_1986_-_No_Silver_Bullet.pdf'),
('david','https://gwern.net/doc/economics/automation/1990-david.pdf'),
('ai-work-qje','https://academic.oup.com/qje/article/140/2/889/7990658'),
('denning','https://denninginstitute.com/pjd/PUBS/Workingsets.html'),
('kernel-cgroup','https://docs.kernel.org/admin-guide/cgroup-v2.html'),
('rdd-paper','https://www.usenix.org/conference/nsdi12/technical-sessions/presentation/zaharia'),
('pacioli','https://exhibits.lib.ku.edu/exhibits/show/keeping-the-books--the-rubinst/under-the-tuscan-sum---the-ita'),
('feature-interaction','https://www.sciencedirect.com/science/article/abs/pii/S1389128613001527'),
('toolkits','https://web.mit.edu/people/evhippel/papers/Toolkits%20JPIM%20final.pdf'),
('direct-manipulation','https://www.cs.umd.edu/~ben/papers/Shneiderman1983Direct.pdf'),
('dsh-bot-commit','https://api.github.com/repos/Nothing1024/dsh-bot/commits?per_page=1')]
def fetch(row):
 id,url=row
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
  with urllib.request.urlopen(req,timeout=35) as res:b=res.read();ct=res.headers.get('content-type','');final=res.url
  ext='.pdf' if b.startswith(b'%PDF') else '.json' if 'json' in ct else '.html';p=R/(id+ext);p.write_bytes(b)
  return {'id':id,'url':url,'final_url':final,'path':str(p),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b),'content_type':ct,'status':'retrieved'}
 except Exception as e:return {'id':id,'url':url,'status':'blocked','error':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:out=list(ex.map(fetch,rows))
(R/'retrieval.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
for x in out:print(x['id'],x['status'],x.get('bytes'),x.get('error'))
