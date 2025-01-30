import os
import subprocess
import pkg_resources
from setuptools.command.install import install
# from setuptools.command.uninstall import uninstall
REQUIREMENTS_FILE = "requirements.txt"

def ensure_requirements_file():
    """Ensure that requirements.txt exists."""
    if not os.path.exists(REQUIREMENTS_FILE):
        with open(REQUIREMENTS_FILE, "w") as f:
            pass  # Create an empty file

def get_requirements():
    """Read requirements.txt and return a dictionary of package:version."""
    ensure_requirements_file()
    requirements = {}
    with open(REQUIREMENTS_FILE, "r") as f:
        for line in f:
            if "==" in line:
                pkg, version = line.strip().split("==")
                requirements[pkg] = version
    return requirements

def write_requirements(requirements):
    """Write the updated dependencies to requirements.txt."""
    with open(REQUIREMENTS_FILE, "w") as f:
        for pkg, version in requirements.items():
            f.write(f"{pkg}=={version}\n")

def add_package(package):
    """Install a package and update requirements.txt."""
    subprocess.run(["pip", "install", package])
    installed_packages = {pkg.key: pkg.version for pkg in pkg_resources.working_set}
    requirements = get_requirements()
    if package in installed_packages:
        requirements[package] = installed_packages[package]
    write_requirements(requirements)

def remove_package(package):
    """Uninstall a package and update requirements.txt."""
    subprocess.run(["pip", "uninstall", "-y", package])
    requirements = get_requirements()
    if package in requirements:
        del requirements[package]
        write_requirements(requirements)

class CustomInstall(install):
    """Custom install command to update requirements.txt."""
    def run(self):
        super().run()
        package_name = self.distribution.get_name()
        add_package(package_name)

class CustomUninstall:
    """Custom uninstall command to update requirements.txt."""
    def run(self):
        package_name = self.distribution.get_name()
        remove_package(package_name)
