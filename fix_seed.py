"""
Regenerates the _bgSeedBakedData function in index.html with:
1. Force-write mode flag — always overwrites when called from button
2. Passes data objects directly to callback so _bgApplyFallback uses real data
"""
import json, re
from pathlib import Path

baked = json.loads(Path('baked_data.json').read_text(encoding='utf-8'))

# Build per-cycle KPI JSON strings
kpi = {}
tbl = {}
stamps = {}
for cy, payload in baked.items():
    kpi[cy]    = json.dumps(payload['kpi'],       ensure_ascii=False, separators=(',',':'))
    tbl[cy]    = json.dumps(payload['tableData'], ensure_ascii=False, separators=(',',':'))
    stamps[cy] = payload['kpi']['_savedAt']

# New _bgSeedBakedData — force=true always writes, force=false only writes if stale
new_fn = (
    'function _bgSeedBakedData(force) {\n'
    '  /* Writes real baked data to localStorage.\n'
    '     force=true  → always overwrite (button click)\n'
    '     force=false → only write if missing/stale (page load) */\n'
)
for cy in ['DM1','DM2','DM3']:
    kk = f'sampra_cycle_{cy}'
    tk = f'sampra_{cy}_tableData'
    new_fn += (
        f'  (function(){{var k={json.dumps(kk)};'
        f'var ok=force;'
        f'if(!ok){{var ex=null;try{{var r=localStorage.getItem(k);if(r)ex=JSON.parse(r);}}catch(e){{}}ok=!ex||!ex._savedAt||ex._savedAt<{stamps[cy]};}} '
        f'if(ok){{'
        f'try{{localStorage.setItem(k,{json.dumps(kpi[cy])});}}catch(e){{}}'
        f'try{{localStorage.setItem({json.dumps(tk)},{json.dumps(tbl[cy])});}}catch(e){{}}'
        f'}}}})(  ); /* {cy} */\n'
    )
new_fn += '}'

html = Path('index.html').read_text(encoding='utf-8')

# Replace old _bgSeedBakedData function
html = re.sub(
    r'function _bgSeedBakedData\(\) \{.*?\}(?=\n\nfunction startBgAutomation)',
    new_fn,
    html,
    count=1,
    flags=re.DOTALL
)

# In startBgAutomation GitHub Pages block: call _bgSeedBakedData(true) — force overwrite
html = html.replace(
    '    _bgSeedBakedData(); /* force-write latest data into localStorage */',
    '    _bgSeedBakedData(true); /* force-overwrite with latest baked data */'
)

# In page-load auto-seed: call _bgSeedBakedData(false) — only if stale
html = html.replace(
    'if (_IS_GITHUB_PAGES) { _bgSeedBakedData(); }',
    'if (_IS_GITHUB_PAGES) { _bgSeedBakedData(false); }'
)
# In auto-login block
html = html.replace(
    '    _bgSeedBakedData();\n    loadAll();',
    '    _bgSeedBakedData(false);\n    loadAll();'
)

Path('index.html').write_text(html, encoding='utf-8')

# Verify
if 'function _bgSeedBakedData(force)' in html:
    print('OK: _bgSeedBakedData(force) function replaced')
else:
    print('ERROR: replacement failed')

# Check _bgApplyFallback still reads from localStorage (it will find the force-written data)
print('DM1 stamp:', stamps['DM1'])
print('DM2 stamp:', stamps['DM2'])
print('DM3 stamp:', stamps['DM3'])
