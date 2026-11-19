# Building My Own Docker: What I Learned

- Docker basics
    - popular implementation of the concept of software containers
    - container = isolated environment for running a program or progress
    - like running a program inside a jail room
    - running process in container:
        - thinks its has full visibility of everything on the host computer
            - visibility limited by namespaces, a Linux kernel feature via (OS) system calls
            - e.g., it thinks it's the first process running on the host computer
                - thinks it has PID (Process ID) 1
                - tricked by PID namespaces, a Linux kernel feature via system calls
        - thinks it has full control over the host computer's hardware resources
            - process' resource access is limited by cgroups, a Linux kernel feature via (OS) system calls
- Docker containers vs VMs
    - diff is in scope or layer of isolation and virtualization
    - container = OS libs + userspace libs + user program
    - VM = hardware + OS kernel + OS libs + userspace libs + user program
    - ASCII visualization:
        ```
        user program        ---------\ -------------\
        userspace libraries          |-> container  |
        system libraries    ---------/              |-> virtual machine
        system kernel                               |
        computer hardware   ------------------------/
        ```
- my toy Docker
    - simplified clone of most critical + basic feature of Docker: run a containerized program
    - scope of included replicated Docker features:
        - supports stripped down `docker run <IMAGE>[:<TAG>] [COMMAND] [ARGUMENTS...]` CLI command only
        - supports Linux containers only
        - containerized process passes its stdout and stderr to its parent process (i.e., my Docker Python program) that spawned it
        - uses PID namespace for limiting containerized program's process ID visiblity
        - fetches a given Linux (distribution) image (manifest) and its individual layers from the Docker Registry Hub HTTP API endpoint
        - downloads, decompresses, and extracts each layer from a Docker (Linux) image to a temp directory on the host computer that is running my Docker program
        - uses `chroot` Linux syscall to change the containerized process' root directory
    - excluded Docker features / scope:
        - namespace isolation for everything outside of PID and user namespaces (e.g., network, file system, etc.)
        - separate programs / processes / daemons as specified in the official Docker system architecture design
        - performance, security, and stress-tested production features
        - no persistent storage / volumes
        - containerized program's app lib / package dependencies in the container
        - Dockerfile
        - etc.
- high level overview of my Docker's logic flow
    - get access / bearer token from Docker Auth HTTP API endpoint
    - create temp root folder for containerized program in `/tmp/`
    - use bearer token to fetch Docker image manifest `.json` from Docker Hub HTTP API endpoint
    - for each layer in the Docker image,
        - download the layer blob (bytes) to the temp root folder from Docker Hub HTTP API endpoint with the bearer token
        - decompress the layer (via `gzip`)
        - extract / unroll the contents from the layer's `tar` archive
        - delete the downloaded `.tar.gz` archive
    - copy the (executable binary) program and its enclosing folders (if any) we want containerized to the temp root directory's `/tmp` folder
    - make `unshare()` Linux syscall to create a new PID and user namespace for my running Docker program and its to-be-containerized program
    - make `chroot()` Linux syscall to change the root directory for my running Docker program and its to-be-containerized program
    - spawn a new process from the copy of the program
        - passing any optional CLI arguments to it if needed
        - route spawned process's stdin and stderr to the parent running (my) Docker program
    - pass containerized process' exit code to parent program before new process exits
    - parent / my Docker program exits
