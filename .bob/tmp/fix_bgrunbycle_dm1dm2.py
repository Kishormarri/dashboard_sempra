import os

# Fix 1: _bgRunCycle - make DM1/DM2 also fetch separate EXP and IMP files (same as DM3)
# This is a text replacement; must use exact bytes from the files

# We'll read each file and do the replacement programmatically
CYCLE_OLD_MARKER = "if(cycle === 'DM3') {"
CYCLE_NEW_MARKER = "_bgFetch(cycle, 'exp', function(expBuf) {"  # starts the unified branch

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

    # Check if already patched (no DM3-only condition)
    if CYCLE_OLD_MARKER not in content:
        print(f'SKIP (already patched or different): {fpath}')
        continue

    # Find the block: from "if(cycle === 'DM3') {" to end of the else branch
    # The pattern ends with the closing "}" of the else and then the outer catch
    # We look for the specific structure

    # Find start of the if(cycle==='DM3') block
    start_idx = content.find("        if(cycle === 'DM3') {")
    if start_idx == -1:
        start_idx = content.find("        if(cycle==='DM3'){")
    if start_idx == -1:
        print(f'WARNING: could not find DM3 condition in {fpath}')
        continue

    # Find the closing "} else {" then the else block end
    # The else block ends at the matching "        }" (8 spaces + })
    # We need to find the outer structure
    # Strategy: find "} else {" after start, then count braces to find end of else block
    else_marker = "        } else {"
    else_idx = content.find(else_marker, start_idx)
    if else_idx == -1:
        print(f'WARNING: could not find else block in {fpath}')
        continue

    # Find end of else block - it ends at "        }" (8 spaces) after else_idx
    # but we need the matching one. Count from else_idx+len(else_marker)
    # The else block contains one _bgFetch call with nested callbacks
    # We look for the "        }" that closes the else block (before the outer "      } catch(e)")
    outer_catch = "      } catch(e) { _bgApplyFallback(cycle, stepN, cb); }"
    outer_catch_idx = content.find(outer_catch, else_idx)
    if outer_catch_idx == -1:
        print(f'WARNING: could not find outer catch after else in {fpath}')
        continue

    # The block to replace is from start_idx to outer_catch_idx (exclusive)
    old_block = content[start_idx:outer_catch_idx]

    # Build the new block - same as what's in MASTER after the fix
    new_block = """        _bgFetch(cycle, 'exp', function(expBuf) {
            try {
              var expKb = Math.round(expBuf.byteLength/1024);
              _bgLog(cycle, '\u2714 EXP received (' + expKb + ' KB)');
              _bgAddFileChip(stepN, 'EXP', expKb);
              _bgFetch(cycle, 'imp', function(impBuf) {
                try {
                  var impKb = Math.round(impBuf.byteLength/1024);
                  _bgLog(cycle, '\u2714 IMP received (' + impKb + ' KB)');
                  _bgAddFileChip(stepN, 'IMP', impKb);
                  _bgSetStep(stepN, 'fetched');
                  _bgUpdateOverall((stepN-1)*33 + 11);
                  _bgDirectAnalyse(cycle, stepN, refBuf, expBuf, cb, impBuf);
                } catch(e) { _bgApplyFallback(cycle, stepN, cb); }
              }, function() {
                _bgDirectAnalyse(cycle, stepN, refBuf, expBuf, cb, null);
              });
            } catch(e) { _bgApplyFallback(cycle, stepN, cb); }
          }, function() {
            _bgDirectAnalyse(cycle, stepN, refBuf, null, cb, null);
          });
        """

    content = content[:start_idx] + new_block + content[outer_catch_idx:]
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'PATCHED: {fpath}')

print('Done.')
