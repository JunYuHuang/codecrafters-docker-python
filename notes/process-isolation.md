# Prompt

## Your Task

In the previous stage, we guarded against malicious activity by restricting an executable's access to the filesystem.

There's another resource that needs to be guarded: the process tree. The process you're executing is currently capable of viewing all other processes running on the host system, and sending signals to them.

In this stage, you'll use [PID namespaces](http://man7.org/linux/man-pages/man7/pid_namespaces.7.html) to ensure that the program you execute has its own isolated process tree. The process being executed must see itself as PID 1.

Just like the previous stage, the tester will run your program like this:
```
mydocker run alpine:latest /usr/local/bin/docker-explorer mypid
```

## How to pass this stage

### 1. Write code to pass this stage

Head over to your editor / IDE and implement your solution.

If you want a quick look at what functions to use or how to structure your code, we recommend looking at [Code Examples](https://app.codecrafters.io/courses/docker/stages/lu7/code-examples).

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
            - `argv[3]`: path to executable (binary) program (command) to run in the container
                - e.g., `/usr/local/bin/docker-explorer`
            - `argv[4:]`: command-line argument(s) passed to `argv[3]` (the executable)
                - e.g., `echo hey`
    - output:
        - N/A
    - side effects:
        - program `argv[3]` is run in its own isolated process tree via Linux PID namespaces
            - sees itself as having PID 1
            - cannot see processes outside of its own PID namespace
    - questions
        - use Linux PID namespaces and cgroups to do this?
        - how does a PID namespace exist?
            - exists as a pseudofile e.g., `/proc/<pid>/ns`
        - how to create a PID namespace?
            - do `clone()` syscall with extra flags e.g., `CLONE_NEWPID`
        - how to make a process join a PID namespace?
            - do `setns()` syscall
        - how to ensure a process in a PID namespace has PID 1?
    - Linux namespaces + PID namespaces
        - namespace = creates isolated group of resources that limits group's access or visibility to outside resources
            - like namespaces in programming
            - OS system call API:
                - `clone()`: call with 1+ flags
                - `setns()`: calling process joins namespace
                - `unshare()`: calling process moves to new namespace
            - destroyed when last process of a namespace exits
        - PID namespaces:
            - isolate process IDs (PIDs)
            - flag: `CLONE_NEWPID`
            - a
    - Linux cgroups
        - TODO
- PEDAC: Examples
    - ex.1
        - run program:
            ```
            ./your_docker.sh run alpine:latest /usr/local/bin/docker-explorer mypid
            ```
            OR
            ```
            mydocker run alpine:latest /usr/local/bin/docker-explorer mypid
            ```
        - terminal output printed:
            ```
            1
            ``` 
- PEDAC: Data Structures And Algorithms
    - create a new PID namespace for program `argv[3]`
    - join that new PID namespace (as the running Python program process)
    - run program `argv[3]` with arguments `argv[4:]` as a new process in the new PID namespace
    - ...