from argostranslate import package

def install_lang_pair(from_code, to_code):
    available = package.get_available_packages()
    for p in available:
        if p.from_code == from_code and p.to_code == to_code:
            print(f"Installing {from_code} → {to_code}")
            package.install_from_path(p.download())

install_lang_pair("en", "es")
install_lang_pair("en", "fr")
install_lang_pair("en", "zh")
install_lang_pair("zh", "fr")