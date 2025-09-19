from multimodaltranslation.text.translate import translate_text


translation = translate_text("Hello", "en", ["fr"], 5000)
print(translation)