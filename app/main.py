import subprocess
import sys

def main():
    command = sys.argv[3]
    args = sys.argv[4:]
    
    completed_subprocess: subprocess.CompletedProcess = subprocess.run(
        [command, *args],
        stdout=sys.stdout,
        stderr=sys.stderr
    )

if __name__ == "__main__":
    main()
