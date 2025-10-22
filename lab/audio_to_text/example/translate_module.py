from multimodaltranslation.text.translate import translate_text

translation = translate_text("Hello", "en", ["fr"])
print(translation)
