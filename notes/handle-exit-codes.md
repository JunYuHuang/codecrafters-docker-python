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
        - passes (sub) program `argv[3]`'s exit code to my (parent) program's process
    - in my program, don't have any custom logging or printing statements
- PEDAC: Examples
    - ex.1
        - run program:
            ```
            ./your_docker.sh run alpine:latest /usr/local/bin/docker-explorer exit 1
            ```
            OR
            ```
            mydocker run alpine:latest /usr/local/bin/docker-explorer exit 1
            ```
        - terminal output printed (empty)
            ```
            ```
- PEDAC: Data Structures And Algorithms
    - get (sub) program `argv[3]`'s exit code
    - set program `argv[3]`'s exit code to its parent process' exit code