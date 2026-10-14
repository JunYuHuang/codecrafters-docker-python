import subprocess
import sys

def main():
    command = sys.argv[3]
    args = sys.argv[4:]
    
    done_subprocess: subprocess.CompletedProcess = subprocess.run(
        [command, *args],
        stdout=sys.stdout,
        stderr=sys.stderr
    )

    sys.exit(done_subprocess.returncode)

if __name__ == "__main__":
    main()
