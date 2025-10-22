"""lab to install different argos languages."""
# This is how to install different langs. Taken from google

import argostranslate.package

# Update available packages
argostranslate.package.update_package_index()
AVAIALABLE_PACKAGES = argostranslate.package.get_available_packages()

# Pick English → Italian (example)
package = next(p for p in AVAIALABLE_PACKAGES if p.from_code == "it" and p.to_code == "en")

# Download and install
path = package.download()
argostranslate.package.install_from_path(path)

print("Installed:", package)
