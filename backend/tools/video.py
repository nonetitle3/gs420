def extract_frames(path,out,every_n=30):
 import cv2,os
 os.makedirs(out,exist_ok=True);cap=cv2.VideoCapture(path);i=0;r=[]
 while True:
  ok,frame=cap.read()
  if not ok:break
  if i%every_n==0:
   p=f"{out}/frame_{i:06d}.jpg";cv2.imwrite(p,frame);r.append(p)
  i+=1
 cap.release();return r
