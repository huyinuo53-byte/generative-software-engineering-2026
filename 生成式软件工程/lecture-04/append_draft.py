import json,sys
from pathlib import Path
p=Path(__file__).parent/'content-draft.json';d=json.loads(p.read_text());new=json.load(sys.stdin);d['sections'].append(new);p.write_text(json.dumps(d,ensure_ascii=False,indent=2))
