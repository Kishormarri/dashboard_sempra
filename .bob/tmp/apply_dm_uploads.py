import re, os

# Read MASTER as source of truth
with open('Sempra_CrossCycle_Summary_MASTER.html', 'r', encoding='utf-8') as f:
    master = f.read()

# ── Extract blocks from master ──────────────────────────────────────────────

# 1. HTML block to insert (DM1 + DM2 + DM3 upload sections)
dm_html_start = master.find('<!-- \u2500\u2500 Step 1B: DM1 EXP / IMP manual upload \u2500\u2500 -->')
step1btn_anchor = '<button id="apStep1Btn" class="ap-btn-primary" onclick="apGoStep(2)"'
step1btn_pos = master.find(step1btn_anchor)
dm_html_block = master[dm_html_start:step1btn_pos]   # includes trailing newline+spaces

# 2. JS block to insert (DM1 + DM2 functions)
dm1_js_anchor = '/* \u2500\u2500 DM1: separate EXP / IMP manual upload (Step 1B) \u2500\u2500 */'
dm3_new_js_anchor = '/* \u2500\u2500 DM3: separate EXP / IMP manual upload (Step 1D) \u2500\u2500 */'
dm1_js_start = master.find(dm1_js_anchor)
dm3_new_js_start = master.find(dm3_new_js_anchor)
dm12_js_block = master[dm1_js_start:dm3_new_js_start]

# 3. Reset block to insert (DM1 + DM2 reset)
reset_dm1_anchor = '/* reset Step 1B \u2014 DM1 separate EXP/IMP */'
reset_dm3_anchor = '/* reset Step 1D \u2014 DM3 separate EXP/IMP */'
reset_dm1_start = master.find(reset_dm1_anchor)
reset_dm3_start = master.find(reset_dm3_anchor)
dm12_reset_block = master[reset_dm1_start:reset_dm3_start]

print(f'HTML block: {len(dm_html_block)} chars')
print(f'JS block:   {len(dm12_js_block)} chars')
print(f'Reset block:{len(dm12_reset_block)} chars')

# ── Files to patch ───────────────────────────────────────────────────────────
files = [
    'Sempra_CrossCycle_Summary_PROD_RELEASE_v1.0.html',
    'Sempra_CrossCycle_Summary_SHAREPOINT.html',
    'Sempra_CrossCycle_Summary_SHAREPOINT_PROD_RELEASE_v1.0.html',
    r'Sempra_DM_Dashboard_PROD_v1.0_RELEASE\Sempra_CrossCycle_Summary_MASTER.html',
    r'Sempra_DM_Dashboard_PROD_v1.0_RELEASE\Sempra_CrossCycle_Summary_SHAREPOINT.html',
    'index.html',
]

for fpath in files:
    if not os.path.exists(fpath):
        print(f'SKIP (not found): {fpath}')
        continue
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip if already patched
    if 'apDm1ExpDz' in content:
        print(f'SKIP (already patched): {fpath}')
        continue

    changed = False

    # ── PATCH 1: Insert DM1/DM2/DM3 HTML before the apStep1Btn ──────────────
    if step1btn_anchor in content:
        content = content.replace(step1btn_anchor, dm_html_block + step1btn_anchor, 1)
        changed = True
    else:
        print(f'  WARNING: HTML anchor not found in {fpath}')

    # ── PATCH 2: Insert DM1+DM2 JS before DM3 JS section ────────────────────
    # The old DM3 comment varies; detect both variants
    dm3_old_comment_1c = '/* \u2500\u2500 DM3: separate EXP / IMP manual upload (Step 1C) \u2500\u2500 */'
    dm3_old_comment = None
    if dm3_old_comment_1c in content:
        dm3_old_comment = dm3_old_comment_1c
    # also try common variant without Step label
    dm3_plain = '/* \u2500\u2500 DM3: separate EXP / IMP manual upload'
    if dm3_old_comment is None:
        idx = content.find(dm3_plain)
        if idx != -1:
            end = content.find('*/', idx) + 2
            dm3_old_comment = content[idx:end]

    if dm3_old_comment:
        content = content.replace(dm3_old_comment, dm12_js_block + dm3_new_js_anchor + '\n', 1)
        changed = True
    else:
        print(f'  WARNING: DM3 JS anchor not found in {fpath}')

    # ── PATCH 3: Insert DM1+DM2 reset before DM3 reset section ──────────────
    dm3_reset_old_1c = '/* reset Step 1C \u2014 DM3 separate EXP/IMP */'
    dm3_reset_old = None
    if dm3_reset_old_1c in content:
        dm3_reset_old = dm3_reset_old_1c
    # try without step label
    dm3_reset_plain = '/* reset Step 1'
    if dm3_reset_old is None:
        idx = content.find(dm3_reset_plain)
        if idx != -1:
            end = content.find('*/', idx) + 2
            candidate = content[idx:end]
            if 'DM3' in candidate:
                dm3_reset_old = candidate

    if dm3_reset_old:
        content = content.replace(dm3_reset_old, dm12_reset_block + reset_dm3_anchor, 1)
        changed = True
    else:
        print(f'  WARNING: DM3 reset anchor not found in {fpath}')

    if changed:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'PATCHED: {fpath}')
    else:
        print(f'NO CHANGES: {fpath}')

print('Done.')
