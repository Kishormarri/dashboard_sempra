"""
Removes the wrongly-placed BAKED DATA BOOTSTRAP from inside _bgFinish,
restores _bgFinish cleanly, and re-injects the bootstrap right before
the standalone loadAll(); at the bottom of the script.
"""
import re, json
from pathlib import Path

html = Path('index.html').read_text(encoding='utf-8')

# ── Step 1: Remove the bootstrap block from inside _bgFinish ──────────────
# The block starts with the log line ending and ends with loadAll(); inside the function
# Original _bgFinish log line:
#   _bgLog('DONE',(allOk?'...')+'...');
# Then immediately the bootstrap was inserted, then loadAll() inside the function

# Remove the bootstrap block (between the log line and loadAll(); inside _bgFinish)
html = re.sub(
    r"(  _bgLog\('DONE',\(allOk\?'[^']*':'[^']*'\)\+'[^']*'\);)\s*"
    r"/\* ── BAKED DATA BOOTSTRAP.*?loadAll\(\);\n",
    r"\1\n",
    html,
    count=1,
    flags=re.DOTALL
)

# ── Step 2: verify _bgFinish is now clean ─────────────────────────────────
if 'BAKED DATA BOOTSTRAP' in html:
    # fallback: strip any remaining bootstrap block
    html = re.sub(
        r'\s*/\* ── BAKED DATA BOOTSTRAP — pre-seeds localStorage for GitHub Pages ── \*/\n'
        r'\(function\(\)\{.*?\}\)\(\);\n',
        '\n',
        html,
        flags=re.DOTALL
    )

# ── Step 3: Rebuild bootstrap from baked_data.json ────────────────────────
baked = json.loads(Path('baked_data.json').read_text(encoding='utf-8'))

lines = ['/* ── BAKED DATA BOOTSTRAP — pre-seeds localStorage for GitHub Pages ── */']
lines.append('(function(){')
lines.append('  try{')
for cy, payload in baked.items():
    kpi_key   = f'sampra_cycle_{cy}'
    table_key = f'sampra_{cy}_tableData'
    kpi_json  = json.dumps(payload['kpi'],       ensure_ascii=False, separators=(',',':'))
    tbl_json  = json.dumps(payload['tableData'], ensure_ascii=False, separators=(',',':'))
    stamp     = payload['kpi']['_savedAt']
    lines.append(f'  (function(){{var k={json.dumps(kpi_key)};var existing=null;try{{var r=localStorage.getItem(k);if(r)existing=JSON.parse(r);}}catch(e){{}}if(!existing||!existing._savedAt||existing._savedAt<{stamp}){{try{{localStorage.setItem(k,{json.dumps(kpi_json)});}}catch(e){{}}try{{localStorage.setItem({json.dumps(table_key)},{json.dumps(tbl_json)});}}catch(e){{}}}}}})(  ); /* {cy} */')
lines.append('  }catch(e){}')
lines.append('})();')
lines.append('')
inject = '\n'.join(lines)

# ── Step 4: Insert BEFORE the standalone loadAll(); (not inside any function)
# Find the standalone loadAll(); — it sits at column 0 after the tech panel function
# We target the pattern: newline + "loadAll();" + newline + newline + "/* Check if full"
target = '\nloadAll();\n\n/* Check if full 3-cycle automation just completed successfully */'
replacement = '\n' + inject + '\nloadAll();\n\n/* Check if full 3-cycle automation just completed successfully */'

if target in html:
    html = html.replace(target, replacement, 1)
    print('Injected bootstrap at correct position (before standalone loadAll)')
else:
    # fallback: find loadAll(); that is at line start and followed by check
    idx = html.find('\nloadAll();\n')
    # find the LAST occurrence (the standalone one at bottom)
    idx = html.rfind('\nloadAll();\n')
    if idx == -1:
        print('ERROR: could not find standalone loadAll()')
        exit(1)
    html = html[:idx] + '\n' + inject + html[idx:]
    print(f'Injected bootstrap at line-start loadAll() position (offset {idx})')

Path('index.html').write_text(html, encoding='utf-8')

# Verify
if 'BAKED DATA BOOTSTRAP' in html:
    # Check it's NOT inside _bgFinish
    bg_finish_start = html.find('function _bgFinish(allOk){')
    bg_finish_end   = html.find('\nfunction _bgFlashBadges')
    bootstrap_pos   = html.find('BAKED DATA BOOTSTRAP')
    if bg_finish_start < bootstrap_pos < bg_finish_end:
        print('ERROR: bootstrap is STILL inside _bgFinish!')
    else:
        print(f'OK: bootstrap is outside _bgFinish (pos={bootstrap_pos}, bgFinish={bg_finish_start}-{bg_finish_end})')
else:
    print('ERROR: bootstrap not found in output')

print(f'DM1 kTotal={baked["DM1"]["kpi"]["kTotal"]} kPct={baked["DM1"]["kpi"]["kPct"]}')
print(f'DM2 kTotal={baked["DM2"]["kpi"]["kTotal"]} kPct={baked["DM2"]["kpi"]["kPct"]}')
print(f'DM3 kTotal={baked["DM3"]["kpi"]["kTotal"]} kPct={baked["DM3"]["kpi"]["kPct"]}')
