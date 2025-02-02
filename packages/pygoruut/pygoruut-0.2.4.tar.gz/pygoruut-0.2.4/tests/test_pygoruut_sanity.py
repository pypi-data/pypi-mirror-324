import unittest
import time
from pygoruut.pygoruut import Pygoruut

class TestPygoruutSanity(unittest.TestCase):
    def setUp(self):
        self.pygoruut = Pygoruut()

    def tearDown(self):
        del self.pygoruut

    def test_languages_and_word_pairs(self):
        test_cases = [
            ("el", [
                ("σιμερα", "simera", True),
                ("καλιμερα", "kalimera", True),
                ("ευχαριστώ", "eixaristo", False)
            ]),
            ("English", [
                ("hello", "hˈɛlloʊ", False),
                ("world", "wˈɚld", False),
                ("python", "piθoʊn", False)
            ]),
            ("Spanish", [
                ("hola", "ˌeola", False),
                ("mundo", "mundo", True),
                ("gracias", "gɾakˈias", False)
            ]),
            ("fr", [
                ("bonjour", "bɔ̃ʒuʁ", False),
                ("monde", "mɔ̃d", False),
                ("merci", "mʁki", False)
            ]),
            ("German", [
                ("hallo", "hˈaltoː", False),
                ("welt", "vəlt", True),
                ("danke", "dˈankə", True)
            ])
        ]

        for language, word_pairs in test_cases:
            with self.subTest(language=language):
                for input_word, expected_phonetic, _ in word_pairs:
                    with self.subTest(input_word=input_word):
                        try:
                            response = self.pygoruut.phonemize(language, input_word)
                            self.assertIsNotNone(response)
                            self.assertTrue(len(response.Words) > 0)
                            actual_word = response.Words[0]
                            
                            self.assertEqual(actual_word.CleanWord.lower(), input_word.lower())
                            self.assertEqual(actual_word.Phonetic, expected_phonetic)
                            
                            print(f"Successful phonemization for {language} word '{input_word}':")
                            print(f"  Expected: {expected_phonetic}")
                            print(f"  Actual:   {actual_word.Phonetic}")
                        except AssertionError as e:
                            print(f"Assertion failed for {language} word '{input_word}':")
                            print(f"  Expected: {expected_phonetic}")
                            print(f"  Actual:   {actual_word.Phonetic}")
                            raise e
                        except Exception as e:
                            self.fail(f"Phonemization failed for {language} word '{input_word}': {str(e)}")


        for language, word_pairs in test_cases:
            with self.subTest(language=language):
                for expected_word, input_phonetic, bidi in word_pairs:
                    if not bidi:
                        continue
                    with self.subTest(input_phonetic=input_phonetic):
                        try:
                            response = self.pygoruut.phonemize(language, input_phonetic, is_reverse=True)
                            self.assertIsNotNone(response)
                            self.assertTrue(len(response.Words) > 0)
                            actual_word = response.Words[0]
                            
                            self.assertEqual(actual_word.CleanWord.lower(), input_phonetic.lower())
                            self.assertEqual(actual_word.Phonetic, expected_word)
                            
                            print(f"Successful dephonemization for {language} IPA '{input_phonetic}':")
                            print(f"  Expected: {expected_word}")
                            print(f"  Actual:   {actual_word.Phonetic}")
                        except AssertionError as e:
                            print(f"Assertion failed for {language} IPA '{input_phonetic}':")
                            print(f"  Expected: {expected_word}")
                            print(f"  Actual:   {actual_word.Phonetic}")
                            raise e
                        except Exception as e:
                            self.fail(f"Dephonemization failed for {language} IPA '{input_phonetic}': {str(e)}")







if __name__ == '__main__':
    unittest.main()
