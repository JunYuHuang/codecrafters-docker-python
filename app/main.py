import subprocess
import sys
import os
import os.path
import shutil
import random
import urllib.request
import urllib.response
import urllib.parse
import http.client
import json
import io
import gzip
from tarfile import TarFile

DOCKER_AUTH_URL = "https://auth.docker.io/token"
DOCKER_REGISTRY_URL = "https://registry.hub.docker.com/v2/library"

def get_bearer_token(image: str) -> str:
    if not image:
        print("[Error] Docker image name cannot be blank")
        return "INVALID_BEARER_TOKEN"

    query_params_str = urllib.parse.urlencode([
        ("service", "registry.docker.io"),
        ("scope", f"repository:library/{image}:pull")
    ])
    url = f"{DOCKER_AUTH_URL}?{query_params_str}"
    request = urllib.request.Request(url, method="GET")
    response: urllib.response.addinfourl = urllib.request.urlopen(request)
    
    if not response or response.status != 200:
        print(f"[Error] Fail to get Docker Registry bearer token from {url}")
        return "INVALID_BEARER_TOKEN"

    return json.loads(response.read())["token"]

def get_blob(params: dict) -> bytes:
    if (
        "bearer_token" not in params or
        "image" not in params or
        "digest" not in params
    ):
        print((
            "[Error] Image blob missing API bearer token, image" +
            " and/or hash digest (in hexadecimal)"
        ))
        return b''

    url = (
        f"{DOCKER_REGISTRY_URL}/{params["image"]}/blobs/{params["digest"]}"
    )
    headers = {
        "Authorization": f"Bearer {params["bearer_token"]}",
        "Accept": "application/vnd.oci.image.manifest.v1+json"
    }
    request = urllib.request.Request(url, headers=headers, method="GET")
    response: urllib.response.addinfourl = urllib.request.urlopen(request)
    
    if not response:
        print(f"[Error] Fail to HTTP Response from {url}")
        return b''
    if response.status == 401:
        params["bearer_token"] = get_bearer_token(params["image"])
    if response.status == 404:
        print((
            f"[Error] No blob for image '{params["image"]}'" +
            f"with hash digest '{params["digest"]}'"
        ))
        return b''
    if response.status != 200:
        print(f"[Error] Fail getting blob with HTTP status {response.status}")
        return b''

    return response.read()

def get_manifest(params: dict) -> dict:
    if (
        "bearer_token" not in params or
        "image" not in params or
        "tag" not in params
    ):
        print(f"[Error] Image manifest missing API bearer token, image, and/or tag")
        return {}

    url = (
        f"{DOCKER_REGISTRY_URL}/{params["image"]}/manifests/{params["tag"]}"
    )
    headers = {
        "Authorization": f"Bearer {params["bearer_token"]}",
        "Accept": "application/vnd.oci.image.manifest.v1+json"
    }
    request = urllib.request.Request(url, headers=headers, method="GET")
    response: urllib.response.addinfourl = urllib.request.urlopen(request)
    
    if not response:
        print(f"[Error] Fail to HTTP Response from {url}")
        return {}
    if response.status == 401:
        params["bearer_token"] = get_bearer_token(params["image"])
    if response.status == 404:
        print((
            f"[Error] No manifest for image '{params["image"]}'" +
            f"with tag '{params["tag"]}'"
        ))
        return {}
    if response.status != 200:
        print(f"[Error] Fail getting manifest with HTTP status {response.status}")
        return {}
    
    # Assumes each manifest pointer JSON object has `mediaType` value
    # `application/vnd.oci.image.manifest.v1+json`
    manifests = json.loads(response.read())["manifests"]
    manifest_pointer = next(
        filter(
            lambda manifest: manifest["platform"]["architecture"] == "amd64",
            manifests
        )
    )

    # Get JSON of actual manifest blob
    params["digest"] = manifest_pointer["digest"]
    manifest = get_blob(params)
    return json.loads(manifest)

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

    # Fetch Docker image manifest based on Docker Registry HTTP API V2:
    # - https://distribution.github.io/distribution/spec/api/
    # - https://distribution.github.io/distribution/spec/auth/token/
    docker_image_details = sys.argv[2].split(":")
    image = docker_image_details[0]
    tag = docker_image_details[1]
    bearer_token = get_bearer_token(image)
    manifest_params = { "bearer_token": bearer_token, "image": image, "tag": tag }
    manifest = get_manifest(manifest_params)

    # Create temp root dir for running `command`
    command_root_dir = make_temp_root_dir(command)

    # TODO: Download each Docker image layer + apply it locally
    IMAGE_LAYERS_LEN = len(manifest["layers"])
    for layer_pos in range(IMAGE_LAYERS_LEN):
        manifest_params["digest"] = manifest["layers"]["digest"]
        layer_bytes = get_blob(manifest_params)

        # TODO: create parent dir for layer via mkdir
        
        # Save layer's byte stream as `.tar.gzip` file
        compressed_layer_path = (
            f"{command_root_dir}{os.sep}layer_{layer_pos}.tar.gzip"
        )
        with open(compressed_layer_path, "wb") as compressed_layer_file:
            compressed_layer_file.write(layer_bytes)

        # Decompress layer bytes via `gzip`
        decompressed_layer_path = (
            f"{command_root_dir}{os.sep}layer_{layer_pos}.tar"
        )
        with open(decompressed_layer_path, "wb") as decompressed_layer_file:
            decompressed_layer_bytes = gzip.decompress(layer_bytes)
            decompressed_layer_file.write(decompressed_layer_bytes)
        
        # Unarchive contents of `.tar` file via `tar`
        layer_tarfile = TarFile(name=decompressed_layer_path, mode='r')


    # Create a new PID + user namespace via `unshare()` Linux syscall
    # (https://man7.org/linux/man-pages/man2/unshare.2.html).
    # First process (e.g., `command`) spawned by this main process will
    # be the `init` process (i.e., have PID 1) in the new namespace.
    os.unshare(os.CLONE_NEWPID | os.CLONE_NEWUSER)

    # Create "chroot jail" from isolated temp root dir for running `command`
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
