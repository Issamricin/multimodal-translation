from argostranslate import package, translate

package.install_from_path('models/translate-en_fr-1_9.argosmodel')
installed_languages = translate.get_installed_languages()
print([str(lang) for lang in installed_languages])

translated = translate.translate("hello", "en", "fr")

print("printing: ", translated)