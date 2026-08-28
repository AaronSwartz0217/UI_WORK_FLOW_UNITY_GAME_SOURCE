from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageOps


PROJECT=Path(r"C:\Users\Administrator\Desktop\UIWorkflow\04_Projects\EquipmentUI")
SOURCE=PROJECT/"FullUI"/"EquipmentUI_FullUI_Review03_1024x1536.png"
CANDIDATES=PROJECT/"into"/"Candidates"/"SplitV01"
PREVIEWS=PROJECT/"into"/"ReassemblyPreview"
FORMAL=PROJECT/"Components"/"out"/"EquipmentUI"
TEMPLATES=PROJECT/"Templates"; QA=PROJECT/"QA"; PREFIX="Equipment"
for folder in (CANDIDATES,PREVIEWS,FORMAL,TEMPLATES,QA): folder.mkdir(parents=True,exist_ok=True)


def crop(box): return Image.open(SOURCE).convert("RGB").crop(box).convert("RGBA")


def chamfer(size,cut):
    w,h=size;cut=max(2,min(cut,w//4,h//4));m=Image.new("L",size,0)
    ImageDraw.Draw(m).polygon([(cut,0),(w-cut-1,0),(w-1,cut),(w-1,h-cut-1),(w-cut-1,h-1),(cut,h-1),(0,h-cut-1),(0,cut)],fill=255)
    return m


def masked(im,cut):
    out=im.convert("RGBA");out.putalpha(chamfer(out.size,cut));return out


def clean_interior(im,texture,region):
    out=im.convert("RGBA");x0,y0,x1,y1=region
    fill=ImageOps.fit(texture.convert("RGB"),(x1-x0,y1-y0),method=Image.Resampling.LANCZOS).convert("RGBA");fill.putalpha(255)
    out.alpha_composite(fill,(x0,y0));return out


def save(role,state,im):
    w,h=im.size;p=CANDIDATES/f"{PREFIX}_{role}_{state}_{w}x{h}.png";im.save(p);return p


def states(normal):
    rgba=normal.convert("RGBA");a=rgba.getchannel("A");rgb=rgba.convert("RGB")
    variants={"Normal":rgb,"Hover":ImageEnhance.Brightness(ImageEnhance.Color(rgb).enhance(1.08)).enhance(1.14),
              "Pressed":ImageEnhance.Brightness(ImageEnhance.Color(rgb).enhance(.94)).enhance(.80),
              "Disabled":ImageEnhance.Brightness(ImageOps.grayscale(rgb).convert("RGB")).enhance(.50)}
    out={}
    for state,base in variants.items(): im=base.convert("RGBA");im.putalpha(a);out[state]=im
    return out


def checkerboard(size,cell=24):
    out=Image.new("RGBA",size,(255,255,255,255));d=ImageDraw.Draw(out)
    for y in range(0,size[1],cell):
        for x in range(0,size[0],cell):
            c=180 if (x//cell+y//cell)%2==0 else 235;d.rectangle((x,y,min(x+cell-1,size[0]-1),min(y+cell-1,size[1]-1)),fill=(c,c,c,255))
    return out


def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()


outer=(17,111,1005,1504)
content_box=(55,238,968,1468)
tab_box=(67,157,253,225)
tab2_pos=(264,157)
close_display=(898,160,62,60)
regular_source_box=(76,768,219,914)
weapon_pos=(402,688)
regular_positions=[
    (76,768),(803,768),
    (70,944),(219,944),(661,944),(812,944),
    (70,1115),(219,1115),(369,1115),(518,1115),(664,1115),(813,1115),
    (70,1288),(219,1288),(369,1288),(518,1288),(664,1288),(813,1288),
]

source=Image.open(SOURCE).convert("RGB")
body_texture=source.crop((250,340,800,650))
main=masked(clean_interior(crop(outer),body_texture,(25,27,963,1365)),25)
content=masked(clean_interior(crop(content_box),body_texture,(14,14,899,1216)),14)
tab=masked(crop(tab_box),12)

# Standardize the generated near-square source into exact square production slots.
regular_rgb=ImageOps.fit(crop(regular_source_box).convert("RGB"),(143,143),method=Image.Resampling.LANCZOS)
regular=masked(regular_rgb.convert("RGBA"),12)
weapon=regular.resize((220,220),Image.Resampling.LANCZOS)
weapon.putalpha(chamfer(weapon.size,18))

saved=[save("MainPanelBase","Empty",main),save("EquipmentContentPanel","Empty",content),
       save("EquipmentSlot","Empty",regular),save("WeaponSlot","Empty",weapon)]
for state,im in states(tab).items(): saved.append(save("TabButton",state,im))

close_paths={}
for state in ("Normal","Hover","Pressed","Disabled"):
    src=PROJECT/"in"/"StylePrimary_Cook"/f"Cook_CloseButton_{state}_52x50.png"
    dst=CANDIDATES/f"{PREFIX}_CloseButton_{state}_52x50.png";dst.write_bytes(src.read_bytes());close_paths[state]=dst;saved.append(dst)

canvas=Image.new("RGBA",(1024,1536),(0,0,0,0));canvas.alpha_composite(main,outer[:2]);canvas.alpha_composite(content,content_box[:2])
canvas.alpha_composite(tab,tab_box[:2]);canvas.alpha_composite(tab,tab2_pos)
canvas.alpha_composite(weapon,weapon_pos)
for pos in regular_positions: canvas.alpha_composite(regular,pos)
close=Image.open(close_paths["Normal"]).convert("RGBA").resize((62,60),Image.Resampling.LANCZOS);canvas.alpha_composite(close,close_display[:2])
preview=PREVIEWS/"Equipment_Reassembled_SplitV01_1024x1536.png";canvas.save(preview)
cb=checkerboard(canvas.size);cb.alpha_composite(canvas);checker_path=PREVIEWS/"Equipment_Reassembled_SplitV01_Checkerboard_1024x1536.png";cb.save(checker_path)

for name,im in (("EquipmentSlot",regular),("WeaponSlot",weapon),("TabButton",tab)):
    im.resize((im.width*4,im.height*4),Image.Resampling.NEAREST).save(PREVIEWS/f"Equipment_{name}_SplitV01_400Percent.png")
strip=Image.new("RGBA",(tab.width*4+18,tab.height),(0,0,0,0));tab_states=states(tab)
for i,state in enumerate(("Normal","Hover","Pressed","Disabled")): strip.alpha_composite(tab_states[state],(i*tab.width+i*6,0))
strip.save(PREVIEWS/"Equipment_TabButton_SplitV01_FourStates.png")
main.save(TEMPLATES/"Equipment_CleanTemplate_Empty_988x1393.png")
manifest={"projectId":"EquipmentUI","splitVersion":"SplitV01","candidateCount":len(saved),"source":str(SOURCE),
          "sourceBounds":{"MainPanelBase":outer,"EquipmentContentPanel":content_box,"TabButtonLeft":tab_box,
                          "TabButtonRight":(*tab2_pos,tab.width,tab.height),"WeaponSlot":(*weapon_pos,weapon.width,weapon.height),
                          "EquipmentSlotSource":regular_source_box,"EquipmentSlotPositions":[(*p,regular.width,regular.height) for p in regular_positions],
                          "CloseButtonDisplay":close_display},
          "files":[{"name":p.name,"sha256":sha(p)} for p in sorted(saved)]}
(QA/"split_v01_manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps({"candidateCount":len(saved),"candidateFolder":str(CANDIDATES),"preview":str(preview),"checkerboard":str(checker_path)},indent=2))
