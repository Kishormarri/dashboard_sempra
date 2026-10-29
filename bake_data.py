"""
Reads the 6 Excel files from .bob, runs the same analysis logic as the
dashboard, and prints JSON for DM1/DM2/DM3 KPIs + compact table rows.
Output goes to baked_data.json — used to inject into index.html.
"""
import os, json, glob as globmod
from pathlib import Path

try:
    import openpyxl
except ImportError:
    import subprocess, sys
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'openpyxl', '-q'])
    import openpyxl

BOB = Path.home() / '.bob'

# ── Column candidates (mirrors _bgDirectAnalyse in index.html) ──────────────
DA_TABLE  = ['TABLE_NAME','TABLENAME','TABLE','OBJECT_NAME','OBJECT','NAME','FIELD','KEY','ID']
DA_SOURCE = ['SOURCE_COUNT','SOURCE_COUNT ','SOURCE','SRC_COUNT','SRC','SOURCE_RECORDS','SOURCE_ROWS']
DA_TARGET = ['TARGET_COUNT','TARGET_COUNT ','TARGET','TGT_COUNT','TGT','TARGET_RECORDS','TARGET_ROWS']
DA_COUNT  = [
    'NUMBER OF RECORDS','NUMBER_OF_RECORDS','NO OF RECORDS','NO_OF_RECORDS',
    'RECORD_COUNT','RECORD COUNT','RECORDS','COUNT','ROW_COUNT','ROW COUNT','ROWS','RECORD','VOLUME',
    'COUNT_OF_RECORDS','COUNT OF RECORDS','NO_RECORDS','NUM_RECORDS','TOTAL_RECORDS','TOTAL RECORDS',
    'TOTAL_ROWS','TOTAL_COUNT','NUMROWS','NUMRECORDS','ROWCOUNT','REC_COUNT',
    'RECCOUNT','RECORD_CNT','ROW_CNT','CNT','NBR_RECORDS','NBR_ROWS','QTY','QUANTITY','NUM','NUMBER'
]
TYPE_CANDS = ['TYPE','MIGTYPE','MIGRATION TYPE','MIGRATION_TYPE','MOVE_TYPE','MOVETYPE','TRANS_TYPE']

def find_col(hdrs, cands):
    hu = [h.upper() for h in hdrs]
    for c in cands:
        if c.upper() in hu:
            return hdrs[hu.index(c.upper())]
    return None

def find_table_col(hdrs):
    x = find_col(hdrs, DA_TABLE)
    if x: return x
    for h in hdrs:
        if 'TABLE' in h.upper(): return h
    for h in hdrs:
        if 'OBJECT' in h.upper(): return h
    return hdrs[0] if hdrs else None

def find_type_col(hdrs):
    for c in TYPE_CANDS:
        if c.upper() in [h.upper() for h in hdrs]:
            return hdrs[[h.upper() for h in hdrs].index(c.upper())]
    for h in hdrs:
        if 'TYPE' in h.upper(): return h
    return None

def to_num(v):
    if v is None or v == '': return None
    try: return float(str(v).replace(',',''))
    except: return None

def latest_file(folder, pattern='*.xlsx'):
    matches = globmod.glob(str(folder / pattern))
    matches = [m for m in matches if not Path(m).name.startswith('~$')]
    if not matches: return None
    return max(matches, key=os.path.getmtime)

def read_xlsx(path):
    if not path or not Path(path).exists():
        return [], []
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ws = wb.active
    rows = list(ws.iter_rows(values_only=True))
    wb.close()
    if not rows: return [], []
    hdrs = [str(c).strip() if c is not None else '' for c in rows[0]]
    data = []
    for row in rows[1:]:
        if all(c is None or c == '' for c in row): continue
        obj = {}
        for i, h in enumerate(hdrs):
            v = row[i] if i < len(row) else None
            obj[h] = v
        data.append(obj)
    return hdrs, data

def analyse(cycle, ref_path, exp_path):
    print(f'  Reading REF: {Path(ref_path).name if ref_path else "NOT FOUND"}')
    print(f'  Reading EXP: {Path(exp_path).name if exp_path else "NOT FOUND"}')

    ref_hdrs, ref_rows = read_xlsx(ref_path)
    exp_hdrs, exp_rows = read_xlsx(exp_path)

    if not ref_rows:
        print(f'  WARNING: No REF rows for {cycle}')
        return None, []

    tbl_c = find_table_col(ref_hdrs)
    src_c = find_col(ref_hdrs, DA_SOURCE)
    tgt_c = find_col(ref_hdrs, DA_TARGET)

    # Build ref map
    ref_map = {}
    for r in ref_rows:
        k = str(r.get(tbl_c) or '').strip().upper()
        if not k: continue
        if k not in ref_map:
            ref_map[k] = {'name': r.get(tbl_c), 'src': None, 'tgt': None}
        s = to_num(r.get(src_c)) if src_c else None
        t = to_num(r.get(tgt_c)) if tgt_c else None
        if s is not None: ref_map[k]['src'] = (ref_map[k]['src'] or 0) + s
        if t is not None: ref_map[k]['tgt'] = (ref_map[k]['tgt'] or 0) + t

    exp_map, imp_map = {}, {}
    if exp_rows:
        etc = find_table_col(exp_hdrs)
        ecc = find_col(exp_hdrs, DA_COUNT)
        type_c = find_type_col(exp_hdrs)
        print(f'  EXP cols: table={etc}, count={ecc}, type={type_c}')
        seen = {}
        for r in exp_rows:
            et = str(r.get(type_c) or '').strip().upper() if type_c else ''
            if type_c and et not in ('', 'EXP', 'IMP'): continue
            ek = str(r.get(etc) or '').strip().upper()
            if not ek: continue
            ev = to_num(r.get(ecc)) or 0 if ecc else 0
            dk = (et or 'EXP') + '|' + ek + '|' + str(ev)
            if dk in seen: continue
            seen[dk] = True
            if not type_c or et in ('', 'EXP'):
                exp_map[ek] = exp_map.get(ek, 0) + ev
            else:
                imp_map[ek] = imp_map.get(ek, 0) + ev

    ref_keys = list(ref_map.keys())
    rklen = len(ref_keys)
    compact = []
    tdata = []
    ei_seen = {}

    for k in ref_keys:
        ei_seen[k] = True
        ref = ref_map[k]
        e = exp_map.get(k)
        im = imp_map.get(k)
        st_d = (ref['src'] - ref['tgt']) if (ref['src'] is not None and ref['tgt'] is not None) else None
        ei_d = (e - im) if (e is not None and im is not None) else None
        st_ok = (st_d == 0) if st_d is not None else None
        ei_ok = (ei_d == 0) if ei_d is not None else None
        compact.append([ref['name'], k, ref['src'], ref['tgt'], e, im, 1])
        tdata.append({'stOk': st_ok, 'eiOk': ei_ok, 'exp': e, 'imp': im})

    # Extra (in EXP/IMP but not REF)
    exp_only_n = imp_only_n = 0
    x_seen = {}
    for xk in list(exp_map.keys()) + list(imp_map.keys()):
        if xk in x_seen: continue
        x_seen[xk] = True
        in_ref = xk in ref_map
        xe = exp_map.get(xk)
        xim = imp_map.get(xk)
        if not in_ref:
            if xe is not None: exp_only_n += 1
            if xim is not None: imp_only_n += 1
        if xk in ei_seen: continue
        ei_seen[xk] = True
        xei_d = (xe - xim) if (xe is not None and xim is not None) else None
        xei_ok = (xei_d == 0) if xei_d is not None else None
        tdata.append({'stOk': None, 'eiOk': xei_ok, 'exp': xe, 'imp': xim})
        if not in_ref:
            compact.append([xk, xk, None, None, xe, xim, 0])

    st_ok_n = st_fa_n = ei_ok_n = ei_fa_n = recon_n = 0
    for r in tdata:
        if r['stOk'] is True: st_ok_n += 1
        elif r['stOk'] is False: st_fa_n += 1
        if r['eiOk'] is True: ei_ok_n += 1
        elif r['eiOk'] is False: ei_fa_n += 1

    has_exp = bool(exp_rows)
    has_imp = bool(imp_map)
    if has_exp and has_imp:
        for r in tdata:
            overall = 'PARTIAL'
            if r['stOk'] is True and r['eiOk'] is True: overall = 'ALL_OK'
            elif r['eiOk'] is True and r['stOk'] is None: overall = 'EI_OK'
            if overall in ('ALL_OK', 'EI_OK'): recon_n += 1
    else:
        recon_n = 0

    n = len(tdata)
    pct = round((recon_n / n) * 100) if n > 0 and has_exp and has_imp else 0

    exp_tot = sum(exp_map.values())
    imp_tot = sum(imp_map.values())
    src_tot = sum((ref_map[k]['src'] or 0) for k in ref_keys)
    tgt_tot = sum((ref_map[k]['tgt'] or 0) for k in ref_keys)

    cv_se_ok = cv_ti_ok = 0
    for k in ref_keys:
        r = ref_map[k]
        e = exp_map.get(k)
        im = imp_map.get(k)
        if r['src'] is not None and e is not None and r['src'] == e: cv_se_ok += 1
        if r['tgt'] is not None and im is not None and r['tgt'] == im: cv_ti_ok += 1

    ref_in_exp = sum(1 for k in ref_keys if k in exp_map)
    ref_in_imp = sum(1 for k in ref_keys if k in imp_map)

    from datetime import datetime
    ts = datetime.now().strftime('%m/%d/%Y, %I:%M:%S %p')

    kpi = {
        'kTotal': rklen, 'kPct': str(pct) + '%',
        'kExp': len(exp_map), 'kImp': len(imp_map),
        'kExpOnly': exp_only_n, 'kImpOnly': imp_only_n,
        'kSTok': st_ok_n, 'kSTfail': st_fa_n,
        'kEIok': ei_ok_n, 'kEIfail': ei_fa_n,
        'cvSeOk': cv_se_ok, 'cvSeTot': rklen,
        'cvTiOk': cv_ti_ok, 'cvTiTot': rklen,
        'refInExp': ref_in_exp, 'refInImp': ref_in_imp,
        'refMissExp': rklen - ref_in_exp, 'refMissImp': rklen - ref_in_imp,
        'expTotalRec': exp_tot, 'impTotalRec': imp_tot,
        'srcTotalRec': src_tot, 'tgtTotalRec': tgt_tot,
        'reconN': recon_n, 'tableN': n,
        '_refOnly': not has_exp and not has_imp,
        '_cycle': cycle,
        '_savedAt': int(__import__('time').time() * 1000),
        'runStamp': ts
    }
    print(f'  -> kTotal={rklen}, kPct={pct}%, reconN={recon_n}, expTot={exp_tot:,}, impTot={imp_tot:,}')
    return kpi, compact


results = {}
for cycle in ['DM1', 'DM2', 'DM3']:
    print(f'\n=== {cycle} ===')
    ref_f = latest_file(BOB / cycle, '*.xlsx')
    exp_f = None
    # pick REF vs EXP by keyword
    all_files = [f for f in globmod.glob(str(BOB / cycle / '*.xlsx'))
                 if not Path(f).name.startswith('~$')]
    ref_kw = ['ref', 'reference', 'reflist', 'master', 'table', 'list']
    exp_kw = ['exp', 'imp', 'export', 'import', 'snp', 'count', 'transition', 'log']
    ref_candidates = [f for f in all_files if any(k in Path(f).name.lower() for k in ref_kw)]
    exp_candidates = [f for f in all_files if any(k in Path(f).name.lower() for k in exp_kw)]
    if not ref_candidates:
        ref_candidates = [f for f in all_files if not any(k in Path(f).name.lower() for k in exp_kw)]
    ref_f = max(ref_candidates, key=os.path.getmtime) if ref_candidates else None
    exp_f = max(exp_candidates, key=os.path.getmtime) if exp_candidates else None

    kpi, compact = analyse(cycle, ref_f, exp_f)
    if kpi:
        results[cycle] = {'kpi': kpi, 'tableData': compact}

with open('baked_data.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False)

print(f'\nWrote baked_data.json — {len(results)} cycles')
