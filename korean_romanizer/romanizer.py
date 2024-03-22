import re

from korean_romanizer.syllable import Syllable
from korean_romanizer.pronouncer import Pronouncer

'''
### Transcribing vowels ###
'''

vowel = {
    # 단모음 monophthongs
    'ㅏ' : 'a',
    'ㅓ' : 'eo',
    'ㅗ' : 'o',
    'ㅜ' : 'u',
    'ㅡ' : 'eu',
    'ㅣ' : 'i',
    'ㅐ' : 'ae',
    'ㅔ' : 'e',
    'ㅚ' : 'oe',
    'ㅟ' : 'wi',
    
    # 이중모음 diphthongs
    'ㅑ' : 'ya',
    'ㅕ' : 'yeo',
    'ㅛ' : 'yo',
    'ㅠ' : 'yu',
    'ㅒ' : 'yae',
    'ㅖ' : 'ye',
    'ㅘ' : 'wa',
    'ㅙ' : 'wae',
    'ㅝ' : 'wo',
    'ㅞ' : 'we',
    'ㅢ' : 'ui', # [붙임 1] ‘ㅢ’는 ‘ㅣ’로 소리 나더라도 ‘ui’로 적는다.
}

'''
### Transcribing consonants ###

Consonants are defined in separate dicts, choseong and jongseong,
for some characters are pronounced differently depending on 
its position in the syllable.

e.g. ㄱ, ㄷ, ㅂ, ㄹ are (g, d, b, r) in onset,
                  but (k, t, p, l) in coda.
e.g. ㅇ is a null sound when placed in onset, but becomes [ng] in coda.
'''

# 초성 Choseong (Syllable Onset)
onset = {
    # 파열음 stops/plosives
    'ᄀ' : 'g',
    'ᄁ' : 'kk',
    'ᄏ' : 'k',
    'ᄃ' : 'd',
    'ᄄ' : 'tt',
    'ᄐ' : 't',
    'ᄇ' : 'b',
    'ᄈ' : 'pp',
    'ᄑ' : 'p',
    # 파찰음 affricates
    'ᄌ' : 'j',
    'ᄍ' : 'jj',
    'ᄎ' : 'ch',
    # 마찰음 fricatives
    'ᄉ' : 's',
    'ᄊ' : 'ss',
    'ᄒ' : 'h',
    # 비음 nasals
    'ᄂ' : 'n',
    'ᄆ' : 'm',
    # 유음 liquids
    'ᄅ' : 'r',
    # Null sound
    'ᄋ' : '',
}

'''
종성 Jongseong (Syllable Coda)

"The 7 Jongseongs (7종성)"
Only the seven consonants below may appear in coda position
'''

coda = {
    # 파열음 stops/plosives
    'ᆨ' : 'k',
    'ᆮ' : 't',
    'ᆸ' : 'p',
    # 비음 nasals
    'ᆫ' : 'n',
    'ᆼ' : 'ng',
    'ᆷ' : 'm',
    # 유음 liquids
    'ᆯ' : 'l',
    
    None: '',
}

# 谚文兼容字母到罗马字母的基础映射表（Revised Romanization）
hangul_to_roman_map = {
    'ㄱ': 'g', 'ㄲ': 'kk', 'ㄴ': 'n', 'ㄷ': 'd', 'ㄸ': 'tt',
    'ㄹ': 'r', 'ㅁ': 'm', 'ㅂ': 'b', 'ㅃ': 'pp', 'ㅅ': 's',
    'ㅆ': 'ss', 'ㅇ': '', 'ㅈ': 'j', 'ㅉ': 'jj', 'ㅊ': 'ch',
    'ㅋ': 'k', 'ㅌ': 't', 'ㅍ': 'p', 'ㅎ': 'h',
    # 韵母
    'ㅏ': 'a', 'ㅐ': 'ae', 'ㅑ': 'ya', 'ㅒ': 'yae', 'ㅓ': 'eo',
    'ㅔ': 'e', 'ㅕ': 'yeo', 'ㅖ': 'ye', 'ㅗ': 'o', 'ㅘ': 'wa',
    'ㅙ': 'wae', 'ㅚ': 'oe', 'ㅛ': 'yo', 'ㅜ': 'u', 'ㅝ': 'wo',
    'ㅞ': 'we', 'ㅟ': 'wi', 'ㅠ': 'yu', 'ㅡ': 'eu', 'ㅢ': 'ui',
    'ㅣ': 'i',
    # 特殊考虑：'ㅇ'在词首时无声，在词中或词尾时表示ng声音，此处简化处理
}
class Romanizer(object):
    def __init__(self, text):
        self.text = text

    def romanize(self):
        pronounced = Pronouncer(self.text).pronounced
        hangul = r"[가-힣ㄱ-ㅣ]"
        _romanized = ""
        for char in pronounced:
            print(char)
            print(char=='ᄏ')
            if char in hangul_to_roman_map:
                _romanized +=  hangul_to_roman_map[char]
            elif char in onset:
                _romanized +=  onset[char]
            elif char in     vowel:
                _romanized +=  vowel[char]
            elif char in    coda:
                _romanized +=  coda[char]
            elif (re.match(hangul, char)):
                s = Syllable(char)

                if not s.medial and not s.final:
                    # s is NOT a full syllable (e.g. characters)
                    # if onset.get(chr(s.initial)):
                    #     _romanized += onset[chr(s.initial)]
                    # elif vowel.get(chr(s.initial)):
                    #     _romanized += vowel[chr(s.initial)]
                    # else:
                    #    _romanized += char
                    _romanized += char
                else:
                    # s is a full syllable
                    _romanized += onset[s.initial] + vowel[s.medial]
                    if s.final in coda:
                        _romanized += coda[s.final]
            else:
                _romanized += char

        return _romanized
