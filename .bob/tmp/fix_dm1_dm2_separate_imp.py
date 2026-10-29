import os

# The fix: remove the DM3-only condition so DM1+DM2 also fetch separate EXP and IMP files
# Replace the if(cycle==='DM3') branch + else branch with the DM3 pattern for all cycles

OLD = """        if(cycle === 'DM3') {
          _bgFetch(cycle, 'exp', function(expBuf) {
            try {
              var expKb = Math.round(expBuf.byteLength/1024);
              _bgLog(cycle, '\\u2714 EXP received (' + expKb + ' KB)');
              _bgAddFileChip(stepN, 'EXP', expKb);
              _bgFetch(cycle, 'imp', function(impBuf) {
                try {
                  var impKb = Math.round(impBuf.byteLength/1024);
                  _bgLog(cycle, '\\u2714 IMP received (' + impKb + ' KB)');
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
        } else {
          _bgFetch(cycle, 'exp', function(expBuf) {
            try {
              var expKb = Math.round(expBuf.byteLength/1024);
              _bgLog(cycle, '\\u2714 EXP received (' + expKb + ' KB)');
              _bgAddFileChip(stepN, 'EXP/IMP', expKb);
              _bgSetStep(stepN, 'fetched');
              _bgUpdateOverall((stepN-1)*33 + 11);
              _bgDirectAnalyse(cycle, stepN, refBuf, expBuf, cb);
            } catch(e) { _bgApplyFallback(cycle, stepN, cb); }
          }, function() {
            _bgApplyFallback(cycle, stepN, cb);
          });
        }"""

NEW = """        _bgFetch(cycle, 'exp', function(expBuf) {
            try {
              var expKb = Math.round(expBuf.byteLength/1024);
              _bgLog(cycle, '\\u2714 EXP received (' + expKb + ' KB)');
              _bgAddFileChip(stepN, 'EXP', expKb);
              _bgFetch(cycle, 'imp', function(impBuf) {
                try {
                  var impKb = Math.round(impBuf.byteLength/1024);
                  _bgLog(cycle, '\\u2714 IMP received (' + impKb + ' KB)');
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
          });"""

files = [
    'Sempra_CrossCycle_Summary_MASTER.html',
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
    if OLD not in content:
        # Already patched or different variant - check for the cycle===DM3 condition
        if "if(cycle === 'DM3')" not in content:
            print(f'SKIP (already patched): {fpath}')
        else:
            print(f'WARNING: anchor not matched in {fpath}')
        continue
    content = content.replace(OLD, NEW, 1)
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'PATCHED: {fpath}')

print('Done.')
