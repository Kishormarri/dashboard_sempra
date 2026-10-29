import os

OLD = (
    "+'Open the '+c.name+' dashboard, upload files and click <strong>Run '+dmLabel+' Analysis</strong>,<br>'\n"
    "      +'then return here and click Refresh.</div>';"
)

NEW = (
    "+'Click the <strong>Automation</strong> button above, open the Advanced Panel,<br>'\n"
    "      +'upload the Reference List + EXP/IMP files for <strong>'+dmLabel+'</strong>, then click <strong>Run '+dmLabel+' Analysis</strong>.</div>';"
)

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
        print(f'SKIP (anchor not found): {fpath}')
        continue
    content = content.replace(OLD, NEW, 1)
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'PATCHED: {fpath}')

print('Done.')
