import re
t = open(".bob/tmp/m5.txt", encoding="utf-8").read()
pages = t.split("=====PAGE ")[1:]
out = open(".bob/tmp/m5_compact.txt", "w", encoding="utf-8")
for pg in pages:
    num, _, body = pg.partition("=====")
    n = int(num)
    if n < 58:
        continue
    lines = [l.strip() for l in body.splitlines() if l.strip()]
    lines = [l for l in lines if not l.startswith("©") and l not in ("▪", "•", "−", "✓")]
    txt = " | ".join(lines)
    out.write(f"[{n}] {txt[:900]}\n")
out.close()
