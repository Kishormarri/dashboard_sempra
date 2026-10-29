import os

OLD = """  var rows=_drillRows||[];
  var total=rows.length;
  if(!total){
    pnl.innerHTML='<div class="drill-nodata">No table data available for Source vs Target breakdown.</div>';
    return;
  }"""

NEW = """  /* use _drillAllRows (full section set) so a search filter never hides the pivot */
  var rows=_drillAllRows||_drillRows||[];
  var total=rows.length;
  if(!total){
    pnl.innerHTML='<div class="drill-nodata">No table data available for Source vs Target breakdown.</div>';
    return;
  }"""

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
    if OLD not in content:
        if '_drillAllRows||_drillRows' in content:
            print(f'SKIP (already patched): {fpath}')
        else:
            print(f'WARNING: anchor not found in {fpath}')
        continue
    content = content.replace(OLD, NEW, 1)
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'PATCHED: {fpath}')

print('Done.')
