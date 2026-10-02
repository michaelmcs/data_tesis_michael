import zipfile, os, sys
src, out = sys.argv[1], sys.argv[2]
with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
    z.write(os.path.join(src, '[Content_Types].xml'), '[Content_Types].xml')
    for d, _, fs in os.walk(src):
        for f in fs:
            full = os.path.join(d, f); rel = os.path.relpath(full, src)
            if rel != '[Content_Types].xml': z.write(full, rel)
