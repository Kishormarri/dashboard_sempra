"""Replace the BAKED_DATA_PLACEHOLDER inside _bgSeedBakedData with real data."""
import json, re
from pathlib import Path

baked = json.loads(Path('baked_data.json').read_text(encoding='utf-8'))

lines = []
for cy, payload in baked.items():
    kpi_key   = f'sampra_cycle_{cy}'
    table_key = f'sampra_{cy}_tableData'
    kpi_json  = json.dumps(payload['kpi'],       ensure_ascii=False, separators=(',',':'))
    tbl_json  = json.dumps(payload['tableData'], ensure_ascii=False, separators=(',',':'))
    stamp     = payload['kpi']['_savedAt']
    lines.append(
        f'  (function(){{var k={json.dumps(kpi_key)};'
        f'var ex=null;try{{var r=localStorage.getItem(k);if(r)ex=JSON.parse(r);}}catch(e){{}}'
        f'if(!ex||!ex._savedAt||ex._savedAt<{stamp}){{'
        f'try{{localStorage.setItem(k,{json.dumps(kpi_json)});}}catch(e){{}}'
        f'try{{localStorage.setItem({json.dumps(table_key)},{json.dumps(tbl_json)});}}catch(e){{}}'
        f'}}}})(  ); /* {cy} */'
    )

replacement = '\n'.join(lines)

html = Path('index.html').read_text(encoding='utf-8')
html = html.replace('  /* BAKED_DATA_PLACEHOLDER */', replacement, 1)
Path('index.html').write_text(html, encoding='utf-8')

# verify
if 'BAKED_DATA_PLACEHOLDER' in html:
    print('ERROR: placeholder still present')
else:
    print('OK: placeholder replaced with real data')
    print(f'DM1 kTotal={baked["DM1"]["kpi"]["kTotal"]} kPct={baked["DM1"]["kpi"]["kPct"]}')
    print(f'DM2 kTotal={baked["DM2"]["kpi"]["kTotal"]} kPct={baked["DM2"]["kpi"]["kPct"]}')
    print(f'DM3 kTotal={baked["DM3"]["kpi"]["kTotal"]} kPct={baked["DM3"]["kpi"]["kPct"]}')
