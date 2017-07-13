import os,sys
frame = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(frame)

from core import main
if __name__ == '__main__':
    main.run()
