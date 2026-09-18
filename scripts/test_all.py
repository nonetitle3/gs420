import subprocess,sys
def main(): raise SystemExit(subprocess.call([sys.executable,"-m","pytest","-q","tests"]))
if __name__=="__main__": main()
