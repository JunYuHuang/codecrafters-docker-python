import subprocess
import sys
import os
import os.path
import shutil
import random

def make_temp_root_dir(binary_path: str) -> str:
    dir_name = f"container-{random.randint(0, 999_999_999)}"
    if len(binary_path) > 0:
        binary_name = binary_path.split(os.sep)[-1]
        dir_name = f"container-{binary_name}"
    
    temp_root_dir = f"{os.sep}tmp{os.sep}{dir_name}"
    if not os.path.exists(temp_root_dir):
        os.mkdir(temp_root_dir)

    return temp_root_dir

def main():
    command = sys.argv[3]
    args = sys.argv[4:]

    # Create isolated temp root dir "chroot jail" for running `command`
    command_root_dir = make_temp_root_dir(command)
    shutil.copy(command, command_root_dir)
    os.chdir(command_root_dir)
    os.chroot(command_root_dir)
    command_copy_path = f".{os.sep}{command.split(os.sep)[-1]}"

    done_subprocess: subprocess.CompletedProcess = subprocess.run(
        [command_copy_path, *args],
        stdout=sys.stdout,
        stderr=sys.stderr
    )

    sys.exit(done_subprocess.returncode)

if __name__ == "__main__":
    main()
