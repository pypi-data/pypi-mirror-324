import re

CONSONANTS_EN = 'BCDFGHKLMNPQRSTVWXZ'


REGEX_RULES_EN2UK = [
    (rf'([{CONSONANTS_EN}][{CONSONANTS_EN}]+)I([{CONSONANTS_EN}]+)', r'\1І\2'),
    (rf'^([{CONSONANTS_EN}]+)I$', r'\1АЙ'),
    (rf':::U([{CONSONANTS_EN}][{CONSONANTS_EN}]+)', r'А\1'),
    (rf':::([{CONSONANTS_EN}])U([{CONSONANTS_EN}][{CONSONANTS_EN}]+)', r'\1А\2'),
    (r'([CGHMPTF])U', r'\1U'),
    (r':::U', r'Ю'),
    (r'AH:::', r'А')
]


STATIC_RULES_EN2UK = {
    'SES:::': 'СЕС',
    'XES:::': 'КСЕС',
    'IES:::': 'АЙС',
    'ATE:::': 'ЕТ',
    'ATES:::': 'ЕТС',
    'AY:::': 'АЙ',
    'OY:::': 'ОЙ',
    'Y:::': 'І',
    'YS:::': 'ЙС',
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
    "IY": "ІЙ",
    "II": "ІЙ",
    "YA": "Я",
    "YI": "ИЙ",
    "YU": "Ю",
    "YO": "ЙО",
    "YE": "Є",
    "OO": 'У',
    'EE': 'І',
    'PH': 'Ф',
    'GH': 'Ж',
    'CK': 'К',
    'EA': 'ІА',
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
    "Q": "К’Ю",
    "W": "В",
    "I": "І",
    "H": "Х",
    "J": "Ж",
    "X": "КС",
    "C": "К",
}


STATIC_RULES_UK2RU = {
    'Є': 'Е',
    'Е': 'Э',
    'И': 'Ы',
    'І': 'И',
    'Ґ': 'Г',
    'Ї': 'ЙИ',
    '’': 'Ь'
}


def __preserve_case(word, replacement):

    if not word.isalpha():
        return replacement.lower()

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

    for pattern, replacement in REGEX_RULES_EN2UK:
        s_translit = re.sub(pattern, repl, s_translit)

    for k, v in STATIC_RULES_EN2UK.items():
        pattern = re.compile(re.escape(k), flags=re.IGNORECASE)
        s_translit = pattern.sub(repl_static, s_translit)

    return s_translit.replace(':::', '')


def uk2ru_translit(s: str) -> str:
    def repl_static(match):
        return __preserve_case(match.group(0), v)

    s_translit = s
    for k, v in STATIC_RULES_UK2RU.items():
        pattern = re.compile(re.escape(k), flags=re.IGNORECASE)
        s_translit = pattern.sub(repl_static, s_translit)

    return s_translit


def en2ru_translit(s: str) -> str:
    s_translit = en2uk_translit(s)
    return uk2ru_translit(s_translit)
