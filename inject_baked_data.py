"""
Injects the baked_data.json into index.html as a <script> block that
pre-seeds localStorage on GitHub Pages so data shows without any bridge.
Only writes if the key is missing or older than the baked stamp — never
overwrites data that was just loaded by the live bridge.
"""
import json, re
from pathlib import Path

baked = json.loads(Path('baked_data.json').read_text(encoding='utf-8'))

# Build the injection script
lines = ['/* ── BAKED DATA BOOTSTRAP — pre-seeds localStorage for GitHub Pages ── */']
lines.append('(function(){')
lines.append('  try{')

for cy, payload in baked.items():
    kpi_key   = f'sampra_cycle_{cy}'
    table_key = f'sampra_{cy}_tableData'
    kpi_json  = json.dumps(payload['kpi'],       ensure_ascii=False, separators=(',',':'))
    tbl_json  = json.dumps(payload['tableData'], ensure_ascii=False, separators=(',',':'))
    stamp     = payload['kpi']['_savedAt']
    lines.append(f'  /* {cy} */')
    lines.append(f'  (function(){{')
    lines.append(f'    var k={json.dumps(kpi_key)};')
    lines.append(f'    var existing=null;try{{var r=localStorage.getItem(k);if(r)existing=JSON.parse(r);}}catch(e){{}}')
    lines.append(f'    if(!existing||!existing._savedAt||existing._savedAt<{stamp}){{')
    lines.append(f'      try{{localStorage.setItem(k,{json.dumps(kpi_json)});}}catch(e){{}}')
    lines.append(f'      try{{localStorage.setItem({json.dumps(table_key)},{json.dumps(tbl_json)});}}catch(e){{}}')
    lines.append(f'    }}')
    lines.append(f'  }})();')

lines.append('  }catch(e){}')
lines.append('})();')

inject_script = '\n'.join(lines)

# Insert before the closing </script> of the first <script> block that has loadAll()
html = Path('index.html').read_text(encoding='utf-8')

# Remove any previously injected block
html = re.sub(
    r'/\* ── BAKED DATA BOOTSTRAP.*?}\)\);\s*',
    '',
    html,
    flags=re.DOTALL
)

# Insert right before the first occurrence of "loadAll();"
target = 'loadAll();'
idx = html.find(target)
if idx == -1:
    print('ERROR: could not find loadAll() in index.html')
    exit(1)

html = html[:idx] + inject_script + '\n\n' + html[idx:]
Path('index.html').write_text(html, encoding='utf-8')
print(f'Injected bootstrap into index.html ({len(inject_script):,} chars)')
print(f'DM1: kTotal={baked["DM1"]["kpi"]["kTotal"]} kPct={baked["DM1"]["kpi"]["kPct"]}')
print(f'DM2: kTotal={baked["DM2"]["kpi"]["kTotal"]} kPct={baked["DM2"]["kpi"]["kPct"]}')
print(f'DM3: kTotal={baked["DM3"]["kpi"]["kTotal"]} kPct={baked["DM3"]["kpi"]["kPct"]}')
