"""
Patches _bgSeedBakedData so force=true stamps _savedAt + runStamp to current time.
"""
import json, re
from pathlib import Path

baked = json.loads(Path('baked_data.json').read_text(encoding='utf-8'))

lines = [
    'function _bgSeedBakedData(force) {',
    '  /* force=true: overwrite + stamp current time (button click)',
    '     force=false: only write if missing/stale (page load) */',
    '  var _now=Date.now();',
    '  var _stamp=new Date().toLocaleString();',
]

for cy, payload in baked.items():
    kpi_key   = f'sampra_cycle_{cy}'
    table_key = f'sampra_{cy}_tableData'
    kpi       = dict(payload['kpi'])
    tbl_json  = json.dumps(payload['tableData'], ensure_ascii=False, separators=(',',':'))
    old_stamp = kpi['_savedAt']

    # KPI base without _savedAt and runStamp — these get injected at runtime
    kpi_base = {k: v for k, v in kpi.items() if k not in ('_savedAt', 'runStamp')}
    kpi_base_json = json.dumps(kpi_base, ensure_ascii=False, separators=(',',':'))
    # Strip trailing } to append dynamic fields
    kpi_prefix = kpi_base_json[:-1]  # everything except closing }

    kk = json.dumps(kpi_key)
    tk = json.dumps(table_key)
    tj = json.dumps(tbl_json)

    block = (
        '  (function(){'
        'var k=' + kk + ';'
        'var ok=force;'
        'if(!ok){var ex=null;try{var r=localStorage.getItem(k);if(r)ex=JSON.parse(r);}catch(e){}ok=!ex||!ex._savedAt||ex._savedAt<' + str(old_stamp) + ';}'
        'if(ok){'
        'try{var kj=' + json.dumps(kpi_prefix) + '+\',"_savedAt":\'+_now+\',"runStamp":"\'+_stamp+\'"}\';localStorage.setItem(k,kj);}catch(e){}'
        'try{localStorage.setItem(' + tk + ',' + tj + ');}catch(e){}'
        '}'
        '})();  /* ' + cy + ' */'
    )
    lines.append(block)

lines.append('}')
new_fn = '\n'.join(lines)

html = Path('index.html').read_text(encoding='utf-8')

html = re.sub(
    r'function _bgSeedBakedData\(force\) \{.*?\}(?=\n\nfunction startBgAutomation)',
    new_fn,
    html,
    count=1,
    flags=re.DOTALL
)

Path('index.html').write_text(html, encoding='utf-8')

if 'function _bgSeedBakedData(force)' in html and '_now' in html and '_stamp' in html:
    print('OK: timestamp patch applied')
else:
    print('ERROR: patch failed')
    print('Has _bgSeedBakedData(force):', 'function _bgSeedBakedData(force)' in html)
    print('Has _now:', '_now' in html)
