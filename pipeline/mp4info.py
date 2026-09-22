import struct, sys

CONTAINERS = {b'moov',b'trak',b'mdia',b'minf',b'stbl',b'udta',b'edts',b'meta',b'ilst',b'moof',b'traf',b'mvex',b'dinf',b'stsd'}

def walk(f, start, end, depth, out):
    f.seek(start)
    pos = start
    while pos < end - 7:
        f.seek(pos)
        hdr = f.read(8)
        if len(hdr) < 8: break
        size = struct.unpack('>I', hdr[:4])[0]
        typ = hdr[4:8]
        hsize = 8
        if size == 1:
            size = struct.unpack('>Q', f.read(8))[0]; hsize = 16
        elif size == 0:
            size = end - pos
        if size < hsize: break
        out.append(('  '*depth) + typ.decode('latin1','replace') + ' size=' + str(size))
        body = pos + hsize
        if typ in CONTAINERS:
            skip = 0
            if typ == b'meta': skip = 4
            if typ == b'stsd': skip = 8
            walk(f, body+skip, pos+size, depth+1, out)
        else:
            f.seek(body)
            data = f.read(min(size-hsize, 400))
            if typ == b'ftyp':
                out.append(('  '*(depth+1)) + 'brands: ' + repr(data[:24]))
            elif typ == b'mvhd':
                ver = data[0]
                if ver == 0:
                    ts, dur = struct.unpack('>II', data[12:20])
                else:
                    ts, dur = struct.unpack('>IQ', data[20:32])
                out.append(('  '*(depth+1)) + 'timescale=%d duration=%d -> %.2fs' % (ts, dur, dur/ts if ts else 0))
            elif typ == b'mdhd':
                ver = data[0]
                if ver == 0:
                    ts, dur = struct.unpack('>II', data[12:20])
                else:
                    ts, dur = struct.unpack('>IQ', data[20:32])
                out.append(('  '*(depth+1)) + 'timescale=%d duration=%d -> %.2fs' % (ts, dur, dur/ts if ts else 0))
            elif typ == b'hdlr':
                out.append(('  '*(depth+1)) + 'handler=' + repr(data[8:12]) + ' name=' + repr(data[24:60]))
            elif typ in (b'stts',b'stsz',b'stco',b'co64',b'stsc'):
                cnt = struct.unpack('>I', data[4:8])[0]
                out.append(('  '*(depth+1)) + 'entries=%d' % cnt)
            else:
                printable = bytes(c if 32 <= c < 127 else 46 for c in data[:120])
                out.append(('  '*(depth+1)) + printable.decode('latin1'))
        pos += size

for path in sys.argv[1:]:
    print('='*70); print(path)
    import os
    out = []
    with open(path,'rb') as f:
        walk(f, 0, os.path.getsize(path), 0, out)
    print('\n'.join(out))
