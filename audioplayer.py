from playsound import playsound
import sys

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <filepath>")
    sys.exit()
playsound(sys.argv[1])
