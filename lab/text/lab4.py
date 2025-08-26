# This is how to install different langs. Taken from google

import argostranslate.package
import argostranslate.translate

# Update available packages
argostranslate.package.update_package_index()
available_packages = argostranslate.package.get_available_packages()

# Pick English → Italian (example)
package = next(p for p in available_packages if p.from_code == "en" and p.to_code == "it")

# Download and install
path = package.download()
argostranslate.package.install_from_path(path)

print("Installed:", package)
