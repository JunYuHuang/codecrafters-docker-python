# Your Task

In the previous stage, we executed a program that existed locally on our machine. This program had write access to the whole filesystem, which means that it could do **dangerous** things!

In this stage, you'll use [**chroot**](https://en.wikipedia.org/wiki/Chroot) to ensure that the program you execute doesn't have access to any files on the host machine. Create an empty temporary directory and `chroot` into it when executing the command. You'll need to copy the binary being executed too.

Just like the previous stage, the tester will run your program like this:
```
mydocker run alpine:latest /usr/local/bin/docker-explorer ls /some_dir
```

## How to pass this stage

### 1. Write code to pass this stage

Head over to your editor / IDE and implement your solution.

If you want a quick look at what functions to use or how to structure your code, we recommend looking at [**Code Examples**](https://app.codecrafters.io/courses/docker/stages/if6/code-examples).

### 2. Submit code

To run tests, make changes to your code and run the submit command:
```
codecrafters submit # Visit https://codecrafters.io/cli to install
```

To run tests, make changes to your code and run the following commands:
```
git add .
git commit --allow-empty -m "[any message]"
git push origin master
```

# Notes:

- PEDAC: Problem
    - input:
        - `argv`: string array of command line arguments
            - `argv[0]`: name of program
                - i.e., `./your_docker.sh`, `your_docker.sh`, or `mydocker`
            - `argv[1]`: command e.g., `run`
            - `argv[2]`: Docker (Linux) image to use e.g., `alpine:latest`
            - `argv[3]`: path to executable (binary) program to run in the container
                - e.g., `/usr/local/bin/docker-explorer`
            - `argv[4:]`: command-line argument(s) passed to `argv[3]` (the executable)
                - e.g., `echo hey`
    - output:
        - none
    - side effects:
        - creates a new temp directory
        - copies program binary `argv[3]` to temp directory
        - limits program `argv[3]`'s access to only any folders and files in the temp directory
        - runs program `argv[3]` inside temp directory
    - Linux `chroot` command
        - must be `root` user to run `chroot` command
            - e.g., change to `root` user first by running `sudo -s` or something first
        - changes root dir for running process and its children processes
- PEDAC: Examples
    - ex.1
        - run program:
            ```
            ./your_docker.sh run alpine:latest /usr/local/bin/docker-explorer ls /some_dir
            ```
            OR
            ```
            mydocker run alpine:latest /usr/local/bin/docker-explorer ls /some_dir
            ```
        - terminal output printed:
            - TODO
- PEDAC: Data Structures And Algorithms
    - create a temp directory `temp_dir` at `/tmp/isolated_program_root`
    - copy program binary `argv[3]` directly inside `temp_dir`
    - run program `argv[3]` with arguments `argv[4:]`
    - ...