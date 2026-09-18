"""Lightweight video utilities."""
from pathlib import Path
def extract_frames(video_path,output_dir,interval=1):
    if interval<1:raise ValueError("interval must be >= 1")
    try:
        import cv2
    except ImportError as e:raise RuntimeError("OpenCV is required") from e
    cap=cv2.VideoCapture(str(video_path))
    if not cap.isOpened():raise ValueError("Unable to open video")
    out=Path(output_dir);out.mkdir(parents=True,exist_ok=True)
    frames=[];i=0
    while True:
        ok,frame=cap.read()
        if not ok:break
        if i%interval==0:
            p=out/f"frame_{i:06d}.jpg";cv2.imwrite(str(p),frame);frames.append(str(p))
        i+=1
    cap.release()
    return {"frames":frames,"count":len(frames)}
