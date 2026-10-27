from pathlib import Path
p=Path('/tmp/gse08-materials');imgs=sorted((p/'slides').glob('slide-*.jpg')); assert len(imgs)==24
objects=[None,b'<< /Type /Catalog /Pages 2 0 R >>',None]
pageids=[]
for f in imgs:
 i=len(objects);pageids.append(i);objects.extend([None,None,None]);data=f.read_bytes()
 objects[i]=f'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 961 772] /Resources << /XObject << /Im0 {i+1} 0 R >> >> /Contents {i+2} 0 R >>'.encode()
 objects[i+1]=f'<< /Type /XObject /Subtype /Image /Width 961 /Height 772 /ColorSpace /DeviceRGB /BitsPerComponent 8 /Filter /DCTDecode /Length {len(data)} >>\nstream\n'.encode()+data+b'\nendstream'
 c=b'q 961 0 0 772 0 0 cm /Im0 Do Q';objects[i+2]=f'<< /Length {len(c)} >>\nstream\n'.encode()+c+b'\nendstream'
objects[2]=f'<< /Type /Pages /Count 24 /Kids [{" ".join(str(i)+" 0 R" for i in pageids)}] >>'.encode()
b=bytearray(b'%PDF-1.4\n%\xe2\xe3\xcf\xd3\n'); offsets=[0]
for i,o in enumerate(objects[1:],1):offsets.append(len(b));b.extend(f'{i} 0 obj\n'.encode()+o+b'\nendobj\n')
x=len(b);b.extend(f'xref\n0 {len(objects)}\n0000000000 65535 f \n'.encode())
for o in offsets[1:]:b.extend(f'{o:010d} 00000 n \n'.encode())
b.extend(f'trailer\n<< /Size {len(objects)} /Root 1 0 R >>\nstartxref\n{x}\n%%EOF\n'.encode());(p/'source-slides.pdf').write_bytes(b);print('24 pages',len(b),'bytes')
