# Prompt

## Your Task

Your docker implementation can now execute a program with a fair degree of isolation - it can't modify files or interact with processes running on the host.

In this stage, you'll use the [Docker registry API](https://distribution.github.io/distribution/spec/api) to fetch the contents of a public image on [Docker Hub](https://hub.docker.com/) and then execute a command within it.

You'll need to:
- Do a small [authentication dance](https://distribution.github.io/distribution/spec/auth/token/)
- Fetch the [image manifest](https://distribution.github.io/distribution/spec/api/#pulling-an-image-manifest)
- [Pull layers](https://distribution.github.io/distribution/spec/api/#pulling-a-layer) of an image and extract them to the chroot directory

The base URL for Docker Hub's public registry is `registry.hub.docker.com`.

The tester will run your program like this:
```
mydocker run alpine:latest /bin/echo hey
```

The image used will be an [official image](https://docs.docker.com/docker-hub/repos/manage/trusted-content/official-images/) from Docker Hub. For example: [`alpine:latest`](https://hub.docker.com/_/alpine), [`alpine:latest`](https://hub.docker.com/_/alpine), [`busyboy:latest`](https://hub.docker.com/_/busybox). When interacting with the Registry API, you'll need to prepend `library/` to the image names.

## How to pass this stage

### 1. Write code to pass this stage

Head over to your editor / IDE and implement your solution.

If you want a quick look at what functions to use or how to structure your code, we recommend looking at [Code Examples](https://app.codecrafters.io/courses/docker/stages/hs1/code-examples).

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
        - downloads the Docker (Linux) image `argv[2]` to the host machine running this program
        - runs a live Docker container of the image `argv[2]`
        - live container runs the program `argv[3]` with argument(s) `argv[4:]`
    - questions
        - how to know which manifest type a Docker image uses?
            - check HTTP GET Response's `Content-Type` field value
            - types (2):
                - OCI image manifest / v1
                - image manifest v2 ?
        - order of image layers to download and apply to client program's local file system?
            - order in which they appear in the HTTP GET Response array of JSON objects?
        - how to download a Docker image layer?
            - send HTTP GET Request with params?
            - what if download takes unusually long?
        - how to check with a certain Docker image with a tag exists in the Docker Registry?
            - get bearer token from `auth.docker.io/token` first
            - send HTTP `GET /v2/<name>/manifests/<reference>` to Docker Registry HTTP API v2 endpoint at `registry.hub.docker.com`
                - Docker server returns HTTP Response 404 if image `<name>` doesn't exist
                - Docker server returns HTTP Response 404 if image `<name>` with tag `<reference>` doesn't exist
        - Docker Registry appears to only have image manifests of type `application/vnd.oci.image.manifest.v1+json`?
            - test for Docker images `Alpine`, `Busybox`, `Ubuntu`
        - how to read and apply a Docker image layer?
            - TODO
- PEDAC: Examples
    - ex.1 program execution
        - run program:
            ```
            ./your_docker.sh run alpine:latest /bin/echo hey
            ./your_docker.sh run alpine:latest /usr/local/bin/docker-explorer mypid
            ```
            OR
            ```
            mydocker run alpine:latest /usr/local/bin/echo hey
            ```
        - terminal output printed:
            ```
            hey
            ``` 
    - ex.2 HTTP exchange flow between program and Docker registry (for OCI image manifest)
        - program -> registry: send HTTP Request to get bearer token
            ```
            GET /token?service=registry.docker.io&scope=repository%3Alibrary%2Falpine%3Apull HTTP/2
            Host: auth.docker.io
            User-Agent: yaak
            Accept: */*
            - query params:
                - `service` = `registry.docker.io`
                - `scope` = `repository:library/alpine:pull`
            ```
        - registry -> program: send HTTP Response with bearer token
            ```
            HTTP/2 200 OK
            Content-Type: application/json
            Date: Fri, 23 Oct 2026 15:17:09 GMT
            Server: cloudflare
            Strict-Transport-Security: max-age=31536000

            {
                "token": "...",
                "access_token": "...",
                "expires_in": 300,
                "issued_at": "2026-10-23T14:17:53.720163163Z"
            }
            ```
        - program -> registry: send HTTP Request to get Docker image manifest
            ```
            GET /v2/library/alpine/manifest/latest HTTP/2
            Host: registry.hub.docker.com
            User-Agent: yaak
            Accept: application/vnd.docker.distribution.manifest.v2+json
            Authorization: Bearer <bearer_token>
            ```
        - registry -> program: send HTTP Response with Docker image manifest(s)
            ```
            HTTP/2 200 OK
            Content-Type: application/vnd.oci.image.index.v1+json
            Date: Fri, 23 Oct 2026 15:17:10 GMT
            Strict-Transport-Security: max-age=31536000
            Content-Length: 9218
            Docker-Content_Digest: sha256:be2656061b536c1883c4034790e21d0a09c5aaaf51968b89368a3c0371ea2c9a
            docker-distribution-api-version: registry/2.0

            {
                "manifests": [
                    {
                        "annotations": {
                            "com.docker.official-images.bashbrew.arch": "amd64",
                            "org.opencontainers.image.base.name": "scratch",
                            "org.opencontainers.image.created": "2026-10-21T22:37:09Z",
                            "org.opencontainers.image.revision": "5aec467fb81238bae9441eea2edb000655d7044f",
                            "org.opencontainers.image.source": "https://github.com/alpinelinux/docker-alpine.git#5aec467fb81238bae9441eea2edb000655d7044f:x86_64",
                            "org.opencontainers.image.url": "https://hub.docker.com/_/alpine",
                            "org.opencontainers.image.version": "3.24.3"
                        },
                        "digest": "sha256:c26612752c78b18faacd63c7d50f4592c2e7b0f25e0e20e82bd74e465c57ab0d",
                        "mediaType": "application/vnd.oci.image.manifest.v1+json",
                        "platform": {
                            "architecture": "amd64",
                            "os": "linux"
                        },
                        "size": 1022
                    },
                    {
                        "annotations": {
                            "com.docker.official-images.bashbrew.arch": "amd64",
                            "vnd.docker.reference.digest": "sha256:c26612752c78b18faacd63c7d50f4592c2e7b0f25e0e20e82bd74e465c57ab0d",
                            "vnd.docker.reference.type": "attestation-manifest"
                        },
                        "digest": "sha256:964745728d174226819257152a79b34561fe7321472eb9c8e32f461cbc7969c2",
                        "mediaType": "application/vnd.oci.image.manifest.v1+json",
                        "platform": {
                            "architecture": "unknown",
                            "os": "unknown"
                        },
                        "size": 838
                        },
                        {
                        "annotations": {
                            "com.docker.official-images.bashbrew.arch": "arm32v6",
                            "org.opencontainers.image.base.name": "scratch",
                            "org.opencontainers.image.created": "2026-10-21T22:58:55Z",
                            "org.opencontainers.image.revision": "5aec467fb81238bae9441eea2edb000655d7044f",
                            "org.opencontainers.image.source": "https://github.com/alpinelinux/docker-alpine.git#5aec467fb81238bae9441eea2edb000655d7044f:armhf",
                            "org.opencontainers.image.url": "https://hub.docker.com/_/alpine",
                            "org.opencontainers.image.version": "3.24.3"
                        },
                        "digest": "sha256:2b8ed0bd9e82c247a3817b867718404f020ab8f701bda09642ddfaa7b4f1578d",
                        "mediaType": "application/vnd.oci.image.manifest.v1+json",
                        "platform": {
                            "architecture": "arm",
                            "os": "linux",
                            "variant": "v6"
                        },
                        "size": 1023
                    },
                    ...
                ]
            }
            ```
        - program -> registry: send HTTP Request to get a Docker image layer
            ```
            GET /v2/library/alpine/manifest/blobs/sha256:c26612752c78b18faacd63c7d50f4592c2e7b0f25e0e20e82bd74e465c57ab0d HTTP/2
            Host: registry.hub.docker.com
            User-Agent: yaak
            Accept: application/vnd.docker.distribution.manifest.v2+json
            Authorization: Bearer <bearer_token>
            ```
        - registry -> program: send HTTP Response with Docker image layer
            ```
            HTTP/2 200 OK
            Accept-Ranges: bytes
            Age: 108
            Alt-Svc: h3=":443"; ma=86400
            Content-Length: 1022
            Content-Type: application/octet-stream
            Date: Fri, 23 Oct 2026 15:26:11 GMT
            Etag: "376628418cae8d6685b2f1f3e0fe2eb9"
            Last-Modified: Wed, 21 Oct 2026 22:37:29 GMT
            Server: AmazonS3
            Via: 1.1 b48378f7d3a68543df5ad0976fffbfa2.cloudfront.net (CloudFront)
            x-amz-cf-id: 226FdJgZ-lHM80GfEOma-b3GHHqU_F_4OKklxWFN1k03WliuwmDo0w==
            x-amz-cf-pop: YVR52-P2
            x-amz-server-side-encryption: AES256
            x-amz-version-id: UGSWX99wUc1ScWIxQLNIh4Pg59Yn030P
            x-cache: Hit from cloudfront

            {
                "schemaVersion": 2,
                "mediaType": "application/vnd.oci.image.manifest.v1+json",
                "config": {
                    "mediaType": "application/vnd.oci.image.config.v1+json",
                    "digest": "sha256:b92841763c5c2140a20eeb2a44e94ebb0e80fd51d9d6b5895ea72fa999525d68",
                    "size": 611
                },
                "layers": [
                    {
                    "mediaType": "application/vnd.oci.image.layer.v1.tar+gzip",
                    "digest": "sha256:7b229517ed222597277036d94892173207d01a731ab3a88eeb1de2e963a2c788",
                    "size": 3853109
                    }
                ],
                "annotations": {
                    "com.docker.official-images.bashbrew.arch": "amd64",
                    "org.opencontainers.image.base.name": "scratch",
                    "org.opencontainers.image.created": "2026-10-21T22:37:09Z",
                    "org.opencontainers.image.revision": "5aec467fb81238bae9441eea2edb000655d7044f",
                    "org.opencontainers.image.source": "https://github.com/alpinelinux/docker-alpine.git#5aec467fb81238bae9441eea2edb000655d7044f:x86_64",
                    "org.opencontainers.image.url": "https://hub.docker.com/_/alpine",
                    "org.opencontainers.image.version": "3.24.3"
                }
            }
            ```
- PEDAC: Data Structures And Algorithms
    - high-level overview
        - contact Docker Hub
        - read image manifest
        - download and extract layers from the image manifest
        - run program `argv[3]` with arguments `argv[4:]` as a new process
        - ...
    - Docker Registry HTTP API V2 helper functions
        - `get_bearer_token(params: hashmap[string -> string]) -> string`:
            - TODO
        - `get_manifest(params: hashmap[string -> string]) -> hashmap`:
            - TODO
        - `get_blob(params: hashmap[string -> string]) -> bytes`:
            - TODO
    - contact Docker Hub
        - get bearer token from Docker Registry HTTP API V2
            - send HTTP GET Request to `auth.docker.io/token`
                - query params fields & example values
                    - `service` = `registry.docker.io`
                    - `scope` = `repository:library/<image>:pull`
                        - e.g., `repository:library/alpine:pull`
            - get HTTP GET Response
                - if response is not 200 OK, exit program with error
                - set string `api_token` to response's `token` field value
    - read image manifest
        - send HTTP GET Request to: `registry.hub.docker.com/v2/library/<image>/manifest/<tag>`
            - `<image>` is set from `argv[2]`'s 1st part before `:` char separator
            - `<tag>` is set from `argv[2]`'s 2nd part after `:` char separator
            - e.g., `registry.hub.docker.com/v2/library/alpine/manifest/latest`
            - set header `Authorization` to `Bearer <api_token>`
                `<api_token>` is set from local variable `api_token`
            - optional: set header `Accept` to `application/vnd.oci.image.manifest.v1+json`
        - get HTTP GET Response
            - if response is 401 unauthorized,
                - get bearer token from Docker Registry again
                - update `api_token` and try GET Request again
            - if response is 404 not found,
                - if JSON response `errors.code` is `MANIFEST_UNKNOWN`,
                    - exit program with error that indicates supplied image `<tag>` is invalid
                - if JSON respnose `errors.code` is ?,
                    - exit program with error that indicates supplie image `<name>` is invalid
            - if response is not 200 OK,
                - exit program with error that indicates unknown error
            - HTTP Response field `content-type` should be `application/vnd.oci.image.index.v1+json`
            - from Response payload (JSON format), get first `amd64` CPU architecture based image manifest from array
                - usually the first item in JSON array (i.e., at index 0)
                - assumes all items in JSON array `manifests` have:
                    - `digest`: value is prefixed with `sha256:`
                    - `mediaType`: `application/vnd.oci.image.index.v1+json`
                    - `platform` property with properties:
                        - `architecture`
                        - `os`
                    - `size`
                - set string `manifest_hash` to response payload's `manifests[0].digest`
        - send HTTP GET Request to: `registry.hub.docker.com/v2/library/<image>/blobs/<manifest_hash>`
            - `<image>` is set from `argv[2]`'s 1st part before `:` char separator
            - `<manifest_hash>` is set from `manifest_hash`
            - e.g., `registry.hub.docker.com/v2/library/alpine/blobs/sha256:c26612752c78b18faacd63c7d50f4592c2e7b0f25e0e20e82bd74e465c57ab0d`
            - set header `Authorization` to `Bearer <api_token>`
                `<api_token>` is set from local variable `api_token`
            - optional: set header `Accept` to `application/vnd.oci.image.manifest.v1+json`
        - get HTTP GET Response
            - if response is 401 unauthorized,
                - get bearer token from Docker Registry again
                - update `api_token` and try GET Request again
            - if response is not 200 OK,
                - exit program with error that indicates unknown error
            - set array `image_layers` to response (JSON) payload's `layers` array property
    - download and extract layers from the image manifest
        - for each layer object / hashmap `layer` in `image_layers`,
            - send HTTP GET Request to: `registry.hub.docker.com/v2/library/<image>/blobs/<layer_hash>`
                - `<image>` is set from `argv[2]`'s 1st part before `:` char separator
                - `<layer_hash>` is set from string `layer.digest`
                - e.g., `registry.hub.docker.com/v2/library/alpine/blobs/sha256:c26612752c78b18faacd63c7d50f4592c2e7b0f25e0e20e82bd74e465c57ab0d`
                - set header `Authorization` to `Bearer <api_token>`
                    `<api_token>` is set from local variable `api_token`
                - optional: set header `Accept` to `application/vnd.oci.image.manifest.v1+json`
            - get / download HTTP GET Response
                - if response is 401 unauthorized,
                    - get bearer token from Docker Registry again
                    - update `api_token` and try GET Request again
                - if response is not 200 OK,
                    - exit program with error that indicates unknown error
            - decompress downloaded file with `gzip`
            - unarchive downloaded file with `tar`
            - somehow apply download layer to local filesystem at directory root?