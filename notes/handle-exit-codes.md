# Your Task

In this stage, you'll need to relay the program's exit code to the parent process.

If the program you're executing exits with exit code 1, your program should exit with exit code 1 too.

To test this behaviour locally, you could use the `exit` command that `docker-explorer` exposes. Run `docker-explorer --help` to view usage.

Just like the previous stage, the tester will run your program like this:
```
mydocker run alpine:latest /usr/local/bin/docker-explorer exit 1
```

## How to pass this stage

### 1. Write code to pass this stage

Head over to your editor / IDE and implement your solution.

If you want a quick look at what functions to use or how to structure your code, we recommend looking at [**Code Examples**](https://app.codecrafters.io/courses/docker/stages/cn8/code-examples).

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