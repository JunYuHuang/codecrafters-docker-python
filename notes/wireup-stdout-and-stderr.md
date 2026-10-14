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
        - passes standard output stream (stdout) of program `argv[3]` to my (parent) program's process
        - passes standard error stream (stderr) of program `argv[3]` to my (parent) program's process
        - prints 1. standard output and 2. standard error stream of running executable program at path `argv[3]` with command-line argument(s) in `argv[4:]`
    - in my program, don't have any custom logging or printing statements
    - Linux / UNIX standard streams
        - standard input:
            - stdin
            - linked to file descriptor (integer) 0
            - redirection symbol: `<`
        - standard output:
            - stdout
            - linked to file descriptor (integer) 1
            - redirection symbol: `>`
        - standard error:
            - stderr
            - linked to file descriptor (integer) 2
            - redirection symbol: `2>`
        - Bash shell command to redirect both `stdout` + `stderr` to same file
            - `{command} > {file} 2>&1` OR
            - `{command} &> {file}` OR
            - `{command} >& {file}`
- PEDAC: Examples
    - ex.1
        - run program:
            ```
            ./your_program.sh run alpine:latest /usr/local/bin/docker-explorer echo hey
            ```
        - terminal output printed:
            ```
            hey
            ```
- PEDAC: Data Structures And Algorithms
    - run subprogram `argv[3]` with arguments `argv[4:]`
    - set subprogram `argv[3]` to pipe its `stdout` to the main running program process' `stdout`
    - set subprogram `argv[3]` to pipe its `stderr` to the main running program process' `stderr`
        - main running process prints `stdout` and `stderr` to terminal display output by default because
            - a process' `stdout` is connected terminal display output
            - a process' `stderr` is connected terminal display output