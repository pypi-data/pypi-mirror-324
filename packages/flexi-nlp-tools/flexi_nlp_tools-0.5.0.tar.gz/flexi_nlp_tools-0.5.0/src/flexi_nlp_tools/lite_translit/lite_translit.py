import re

CONSONANTS = 'BCDFGHKLMNPQRSTVWXZ'


REGEX_RULES = [
    (rf'([{CONSONANTS}][{CONSONANTS}]+)I([{CONSONANTS}]+)', r'\1І\2'),
    (rf'^([{CONSONANTS}]+)I$', r'\1АЙ'),
    (rf':::U([{CONSONANTS}][{CONSONANTS}]+)', r'А\1'),
    (rf':::([{CONSONANTS}])U([{CONSONANTS}][{CONSONANTS}]+)', r'\1А\2'),
    (r'([CGHMPTF])U', r'\1U'),
    (r':::U', r'Ю'),
]


STATIC_RULES = {
    'SES:::': 'СЕС',
    'XES:::': 'КСЕС',
    'IES:::': 'АЙС',
    'ATE:::': 'ЕТ',
    'ATES:::': 'ЕТС',
    'AY:::': 'АЙ',
    'OY:::': 'ОЙ',
    'Y:::': 'І',
    'YS:::': 'ЙS',
    'ES:::': 'С',
    'E:::': '',
    'S:::': 'С',
    'C:::': 'К',
    'CE': 'СE',
    'СI': 'СI',
    'СY': 'СY',
    "UE": 'У',
    "UI": 'У',
    'UO': 'У',
    'SHCH': 'Щ',
    'KH': 'Х',
    'TS': 'Ц',
    'TH': 'С',
    'CC': 'КЦ',
    'CH': 'Ч',
    'SH': 'Ш',
    "ZH": "Ж",
    "ZJ": "Ж",
    "IU": "Ю",
    "IA": "Я",
    "IO": "ЙО",
    "IE": "Є",
    "IY": "ІИ",
    "II": "ІЙ",
    "YA": "Я",
    "YI": "ИЙ",
    "YU": "Ю",
    "YO": "ЙО",
    "YE": "Є",
    "OO": 'У',
    'EE': 'І',
    'PH': 'Ф',
    "A": "А",
    "B": "Б",
    "V": "В",
    "G": "Г",
    "D": "Д",
    "E": "Е",
    "Z": "З",
    "Y": "АЙ",
    "K": "К",
    "L": "Л",
    "M": "М",
    "N": "Н",
    "O": "О",
    "P": "П",
    "R": "Р",
    "S": "С",
    "T": "Т",
    "U": "У",
    "F": "Ф",
    "Q": "КЬЮ",
    "W": "В",
    "I": "І",
    "H": "Х",
    "J": "Й",
    "X": "КС",
    "C": "К",
}


def __preserve_case(word, replacement):

    if word.islower():
        return replacement.lower()

    elif word.isupper():
        return replacement.upper()

    elif word.istitle():
        return replacement.capitalize()

    return replacement


def en2uk_translit(s: str) -> str:
    def repl(match):
        result = replacement
        for i in range(1, len(match.groups()) + 1):
            group = match.group(i)
            result = result.replace(f'\\{i}', __preserve_case(group, group))
        return result

    def repl_static(match):
        return __preserve_case(match.group(0), v)

    s_translit = f':::{s}:::'

    for pattern, replacement in REGEX_RULES:
        s_translit = re.sub(pattern, repl, s_translit)

    for k, v in STATIC_RULES.items():
        pattern = re.compile(re.escape(k), flags=re.IGNORECASE)
        s_translit = pattern.sub(repl_static, s_translit)

    return s_translit.replace(':::', '')
