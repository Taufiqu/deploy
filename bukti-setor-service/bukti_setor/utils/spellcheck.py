from spellchecker import SpellChecker
import os
import threading

# Global variables for lazy loading
_spell_checker = None
_spell_lock = threading.Lock()

def get_spell_checker():
    """
    Lazy loading untuk SpellChecker
    Hanya initialize ketika benar-benar dibutuhkan
    """
    global _spell_checker
    
    if _spell_checker is None:
        with _spell_lock:
            if _spell_checker is None:  # Double-check locking pattern
                try:
                    print("📚 Inisialisasi SpellChecker...")
                    _spell_checker = SpellChecker(language=None, case_sensitive=False)
                    kamus_path = os.path.join(os.path.dirname(__file__), 'kamus_indonesia.txt')
                    _spell_checker.word_frequency.load_text_file(kamus_path)
                    print(f"✅ Kamus Indonesia berhasil dimuat dari: {kamus_path}")
                except Exception as e:
                    print(f"❌ Error memuat kamus Indonesia: {e}")
                    _spell_checker = SpellChecker(language='id')  # fallback ke bahasa Indonesia default
    
    return _spell_checker

def correct_spelling(text):
    """
    Correct spelling dengan lazy-loaded SpellChecker
    """
    if not text or not text.strip():
        return text
        
    spell = get_spell_checker()
    words = text.split()
    corrected_words = []
    
    for word in words:
        if word in spell or not spell.correction(word):
            corrected_words.append(word)
        else:
            corrected_words.append(spell.correction(word))
    
    return ' '.join(corrected_words)
