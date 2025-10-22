from argostranslate import package, translate

package.install_from_path('models/translate-en_fr-1_9.argosmodel')
INSTALLED_LANGUAGES = translate.get_installed_languages()
print([str(lang) for lang in INSTALLED_LANGUAGES    ])

translated = translate.translate("hello", "en", "fr")

print("printing: ", translated)
