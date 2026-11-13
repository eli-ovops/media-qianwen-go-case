from pathlib import Path
import struct,json,hashlib
r=Path(__file__).resolve().parent
source=r/'public/heiti.ttc';b=source.read_bytes();face=struct.unpack_from('>I',b,16)[0];n=struct.unpack_from('>H',b,face+4)[0]
out=bytearray(b[face:face+12]+b'\0'*(16*n));head_offset=0
for i in range(n):
 tag,_,off,length=struct.unpack_from('>4sIII',b,face+12+16*i);part=bytearray(b[off:off+length]);new_off=len(out)
 if tag==b'head':part[8:12]=b'\0'*4;head_offset=new_off
 padded=part+b'\0'*((-len(part))%4);checksum=sum(struct.unpack('>'+str(len(padded)//4)+'I',padded))&0xffffffff
 struct.pack_into('>4sIII',out,12+16*i,tag,checksum,new_off,length);out.extend(padded)
adj=(0xB1B0AFBA-sum(struct.unpack('>'+str(len(out)//4)+'I',out)))&0xffffffff
struct.pack_into('>I',out,head_offset+8,adj)
p=r/'public/heiti-sc-v2.ttf';p.write_bytes(out)
(r.parent/'evidence/sample-v2/font-provenance.json').write_text(json.dumps({'source':str(source),'source_sha256':hashlib.sha256(b).hexdigest(),'face_index':1,'family':'Heiti SC','output':str(p),'sha256':hashlib.sha256(out).hexdigest(),'method':'copy TTC face tables into SFNT, rebase offsets and recalculate checksums; no font outlines changed'},indent=2))
