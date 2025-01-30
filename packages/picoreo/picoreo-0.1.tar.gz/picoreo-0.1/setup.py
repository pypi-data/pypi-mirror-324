import os
import platform
from setuptools import setup, find_packages


# If you store version in a file named VERSION
# we can read it dynamically, otherwise replace this logic with a hard-coded version.
def read_version():
    with open("VERSION", encoding="utf-8") as f:
        return f.read().strip()


# If you have a README.md that you want to use as your long description
def read_long_description():
    with open("README.md", encoding="utf-8") as f:
        return f.read()


def cuda_is_available():
    """
    Naive check to see if CUDA might be installed.
    This is not foolproof! You could refine checks:
      - Searching PATH
      - Checking nvcc, nvidia-smi, etc.
    """
    # Example: check for 'CUDA_PATH' or if 'nvcc' is in PATH
    if "CUDA_PATH" in os.environ:
        return True
    # Alternatively, check if 'nvcc' is somewhere in PATH
    for p in os.environ.get("PATH", "").split(os.pathsep):
        nvcc_path = os.path.join(p, "nvcc")
        if os.path.exists(nvcc_path) or os.path.exists(nvcc_path + ".exe"):
            return True
    return False


def get_pytorch_gpu_extras():
    """
    Returns a list of dependencies (and possibly a link or extra index URL)
    for installing PyTorch GPU wheels. This logic tries to guess the right
    package based on OS and CUDA availability, but it's only an example.

    For real-world usage, you might prefer simpler patterns like:
      extras_require={"pytorch-gpu": ["torch==...+cu118", "-f https://..."]}
    to let users pick their own environment.
    """
    # If we detect no CUDA, just return an empty list or fallback to CPU.
    if not cuda_is_available():
        return []

    system = platform.system().lower()

    # Feel free to update versions/URLs to match the latest wheels
    if system == "windows":
        # Example: CUDA 12.4 for Windows
        return [
            "torch==2.0.1+cu124",
            "torchvision==0.15.2+cu124",
            "torchaudio==2.0.2+cu124",
            # The '-f' in requirements is usually done on the command line,
            # but you can specify it as a dependency link. (This is a bit hacky.)
            "-f https://download.pytorch.org/whl/cu124"
        ]
    elif system == "linux":
        # Example: CUDA 12.4 for Linux
        return [
            "torch==2.0.1+cu124",
            "torchvision==0.15.2+cu124",
            "torchaudio==2.0.2+cu124",
            "-f https://download.pytorch.org/whl/cu124"
        ]
    elif system == "darwin":
        # macOS generally uses a different approach.
        # Official CUDA-based wheels for macOS are often not available.
        # Some users rely on conda or custom builds.
        # For Apple Silicon, you might rely on MPS or CPU.
        return [
            "torch>=2.0.0"  # Possibly a CPU or MPS version.
        ]

    # Fallback if OS is unrecognized
    return []


###############################################################################
# Extras definition
###############################################################################
extras_require = {
    # If someone wants scikit-learn
    "sklearn": ["scikit-learn>=1.0.0"],

    # PyTorch CPU
    # This is a generic placeholder; pinning versions or adding -f with
    # a PyTorch index can be done similarly to the GPU approach.
    "pytorch-cpu": [
        "torch>=2.0.0",
        "torchvision>=0.15.0",
        "torchaudio>=2.0.0",
        # Optionally, for official CPU wheels:
        # "-f https://download.pytorch.org/whl/cpu"
    ],

    # PyTorch GPU: attempt to pick the wheel based on OS + environment
    # If we detect no CUDA, this might just return an empty list.
    "pytorch-gpu": get_pytorch_gpu_extras(),
}


setup(
    name="picoreo",
    version=read_version(),  # or replace with a string like "0.1.0"
    author="samy khelifi",
    author_email="samy.khelifi@ign.fr",
    description="spatial diversity sampling for machine learning or statistical study applied to geographic domain",
    long_description=read_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/IGNF/picoreo",
    project_urls={
        "Bug Tracker": "https://github.com/IGNF/picoreo/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "picoreo"},
    packages=find_packages(where="picoreo"),
    python_requires=">=3.12",
    install_requires=[
        "numpy>=1.19",
        "pandas>=1",
        "geopandas>=0.10",
        "rasterio>=1.1.5",
    ],
    include_package_data=True,  # allows non-.py files listed in MANIFEST.in or package_data
    package_data={
        # This replicates [options.package_data]
        # means: for any package, include *.yml
        "": ["*.yml"],
    },
)
