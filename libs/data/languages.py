'''special system for languages including conversion between types'''
from libs.config_option import ConfigOption

class Language:
    '''Single Language Class'''
    def __init__(self, name, iso_639_1, iso_639_2t, iso_639_2b, family):
        self._name = name
        self._iso_639_1 = iso_639_1
        self._iso_639_2t = iso_639_2t
        self._iso_639_2b = iso_639_2b
        self._family = family

    def name(self):
        '''Returns Name'''
        return self._name
    def iso_639_1(self):
        '''Returns 2 letter code'''
        return self._iso_639_1
    def iso_639_2t(self):
        '''Returns 3 letter local name'''
        return self._iso_639_2t
    def iso_639_2b(self):
        '''Returns 3 letter english name'''
        return self._iso_639_2b
    def family(self):
        '''Returns family'''
        return self._family

class Languages:
    '''controller for languages'''
    _LANGUAGES = [
        Language("Abkhazian", "ab", "abk", "abk", "Northwest Caucasian"),
        Language("Afar", "aa", "aar", "aar", "Afro-Asiatic"),
        Language("Afrikaans", "af", "afr", "afr", "Indo-European"),
        Language("Akan", "ak", "aka", "aka", "Niger–Congo"),
        Language("Albanian", "sq", "sqi", "alb", "Indo-European"),
        Language("Amharic", "am", "amh", "amh", "Afro-Asiatic"),
        Language("Arabic", "ar", "ara", "ara", "Afro-Asiatic"),
        Language("Aragonese", "an", "arg", "arg", "Indo-European"),
        Language("Armenian", "hy", "hye", "arm", "Indo-European"),
        Language("Assamese", "as", "asm", "asm", "Indo-European"),
        Language("Avaric", "av", "ava", "ava", "Northeast Caucasian"),
        Language("Avestan", "ae", "ave", "ave", "Indo-European"),
        Language("Aymara", "ay", "aym", "aym", "Aymaran"),
        Language("Azerbaijani", "az", "aze", "aze", "Turkic"),
        Language("Bambara", "bm", "bam", "bam", "Niger–Congo"),
        Language("Bashkir", "ba", "bak", "bak", "Turkic"),
        Language("Basque", "eu", "eus", "baq", "Language isolate"),
        Language("Belarusian", "be", "bel", "bel", "Indo-European"),
        Language("Bengali", "bn", "ben", "ben", "Indo-European"),
        Language("Bihari languages", "bh", "bih", "bih", "Indo-European"),
        Language("Bislama", "bi", "bis", "bis", "Creole"),
        Language("Bosnian", "bs", "bos", "bos", "Indo-European"),
        Language("Breton", "br", "bre", "bre", "Indo-European"),
        Language("Bulgarian", "bg", "bul", "bul", "Indo-European"),
        Language("Burmese", "my", "mya", "bur", "Sino-Tibetan"),
        Language("Catalan, Valencian", "ca", "cat", "cat", "Indo-European"),
        Language("Chamorro", "ch", "cha", "cha", "Austronesian"),
        Language("Chechen", "ce", "che", "che", "Northeast Caucasian"),
        Language("Chichewa, Chewa, Nyanja", "ny", "nya", "nya", "Niger–Congo"),
        Language("Chinese", "zh", "zho", "chi", "Sino-Tibetan"),
        Language("Chuvash", "cv", "chv", "chv", "Turkic"),
        Language("Cornish", "kw", "cor", "cor", "Indo-European"),
        Language("Corsican", "co", "cos", "cos", "Indo-European"),
        Language("Cree", "cr", "cre", "cre", "Algonquian"),
        Language("Croatian", "hr", "hrv", "hrv", "Indo-European"),
        Language("Czech", "cs", "ces", "cze", "Indo-European"),
        Language("Danish", "da", "dan", "dan", "Indo-European"),
        Language("Divehi, Dhivehi, Maldivian", "dv", "div", "div", "Indo-European"),
        Language("Dutch, Flemish", "nl", "nld", "dut", "Indo-European"),
        Language("Dzongkha", "dz", "dzo", "dzo", "Sino-Tibetan"),
        Language("English", "en", "eng", "eng", "Indo-European"),
        Language("Esperanto", "eo", "epo", "epo", "Constructed"),
        Language("Estonian", "et", "est", "est", "Uralic"),
        Language("Ewe", "ee", "ewe", "ewe", "Niger–Congo"),
        Language("Faroese", "fo", "fao", "fao", "Indo-European"),
        Language("Fijian", "fj", "fij", "fij", "Austronesian"),
        Language("Finnish", "fi", "fin", "fin", "Uralic"),
        Language("French", "fr", "fra", "fre", "Indo-European"),
        Language("Fulah", "ff", "ful", "ful", "Niger–Congo"),
        Language("Galician", "gl", "glg", "glg", "Indo-European"),
        Language("Georgian", "ka", "kat", "geo", "Kartvelian"),
        Language("German", "de", "deu", "ger", "Indo-European"),
        Language("Greek, Modern (1453-)", "el", "ell", "gre", "Indo-European"),
        Language("Guarani", "gn", "grn", "grn", "Tupian"),
        Language("Gujarati", "gu", "guj", "guj", "Indo-European"),
        Language("Haitian, Haitian Creole", "ht", "hat", "hat", "Creole"),
        Language("Hausa", "ha", "hau", "hau", "Afro-Asiatic"),
        Language("Hebrew", "he", "heb", "heb", "Afro-Asiatic"),
        Language("Herero", "hz", "her", "her", "Niger–Congo"),
        Language("Hindi", "hi", "hin", "hin", "Indo-European"),
        Language("Hiri Motu", "ho", "hmo", "hmo", "Austronesian"),
        Language("Hungarian", "hu", "hun", "hun", "Uralic"),
        Language("Interlingua (International Auxiliary Language Association)", "ia", "ina", "ina",
                 "Constructed"),
        Language("Indonesian", "id", "ind", "ind", "Austronesian"),
        Language("Interlingue, Occidental", "ie", "ile", "ile", "Constructed"),
        Language("Irish", "ga", "gle", "gle", "Indo-European"),
        Language("Igbo", "ig", "ibo", "ibo", "Niger–Congo"),
        Language("Inupiaq", "ik", "ipk", "ipk", "Eskimo–Aleut"),
        Language("Ido", "io", "ido", "ido", "Constructed"),
        Language("Icelandic", "is", "isl", "ice", "Indo-European"),
        Language("Italian", "it", "ita", "ita", "Indo-European"),
        Language("Inuktitut", "iu", "iku", "iku", "Eskimo–Aleut"),
        Language("Japanese", "ja", "jpn", "jpn", "Japonic"),
        Language("Javanese", "jv", "jav", "jav", "Austronesian"),
        Language("Kalaallisut, Greenlandic", "kl", "kal", "kal", "Eskimo–Aleut"),
        Language("Kannada", "kn", "kan", "kan", "Dravidian"),
        Language("Kanuri", "kr", "kau", "kau", "Nilo-Saharan"),
        Language("Kashmiri", "ks", "kas", "kas", "Indo-European"),
        Language("Kazakh", "kk", "kaz", "kaz", "Turkic"),
        Language("Central Khmer", "km", "khm", "khm", "Austroasiatic"),
        Language("Kikuyu, Gikuyu", "ki", "kik", "kik", "Niger–Congo"),
        Language("Kinyarwanda", "rw", "kin", "kin", "Niger–Congo"),
        Language("Kirghiz, Kyrgyz", "ky", "kir", "kir", "Turkic"),
        Language("Komi", "kv", "kom", "kom", "Uralic"),
        Language("Kongo", "kg", "kon", "kon", "Niger–Congo"),
        Language("Korean", "ko", "kor", "kor", "Koreanic"),
        Language("Kurdish", "ku", "kur", "kur", "Indo-European"),
        Language("Kuanyama, Kwanyama", "kj", "kua", "kua", "Niger–Congo"),
        Language("Latin", "la", "lat", "lat", "Indo-European"),
        Language("Luxembourgish, Letzeburgesch", "lb", "ltz", "ltz", "Indo-European"),
        Language("Ganda", "lg", "lug", "lug", "Niger–Congo"),
        Language("Limburgan, Limburger, Limburgish", "li", "lim", "lim", "Indo-European"),
        Language("Lingala", "ln", "lin", "lin", "Niger–Congo"),
        Language("Lao", "lo", "lao", "lao", "Tai–Kadai"),
        Language("Lithuanian", "lt", "lit", "lit", "Indo-European"),
        Language("Luba-Katanga", "lu", "lub", "lub", "Niger–Congo"),
        Language("Latvian", "lv", "lav", "lav", "Indo-European"),
        Language("Manx", "gv", "glv", "glv", "Indo-European"),
        Language("Macedonian", "mk", "mkd", "mac", "Indo-European"),
        Language("Malagasy", "mg", "mlg", "mlg", "Austronesian"),
        Language("Malay", "ms", "msa", "may", "Austronesian"),
        Language("Malayalam", "ml", "mal", "mal", "Dravidian"),
        Language("Maltese", "mt", "mlt", "mlt", "Afro-Asiatic"),
        Language("Maori", "mi", "mri", "mao", "Austronesian"),
        Language("Marathi", "mr", "mar", "mar", "Indo-European"),
        Language("Marshallese", "mh", "mah", "mah", "Austronesian"),
        Language("Mongolian", "mn", "mon", "mon", "Mongolic"),
        Language("Nauru", "na", "nau", "nau", "Austronesian"),
        Language("Navajo, Navaho", "nv", "nav", "nav", "Dené–Yeniseian"),
        Language("North Ndebele", "nd", "nde", "nde", "Niger–Congo"),
        Language("Nepali", "ne", "nep", "nep", "Indo-European"),
        Language("Ndonga", "ng", "ndo", "ndo", "Niger–Congo"),
        Language("Norwegian Bokmål", "nb", "nob", "nob", "Indo-European"),
        Language("Norwegian Nynorsk", "nn", "nno", "nno", "Indo-European"),
        Language("Norwegian", "no", "nor", "nor", "Indo-European"),
        Language("Sichuan Yi, Nuosu", "ii", "iii", "iii", "Sino-Tibetan"),
        Language("South Ndebele", "nr", "nbl", "nbl", "Niger–Congo"),
        Language("Occitan", "oc", "oci", "oci", "Indo-European"),
        Language("Ojibwa", "oj", "oji", "oji", "Algonquian"),
        Language("Church Slavic, Old Slavonic, Church Slavonic, Old Bulgarian, Old Church Slavonic",
                 "cu", "chu", "chu", "Indo-European"),
        Language("Oromo", "om", "orm", "orm", "Afro-Asiatic"),
        Language("Oriya", "or", "ori", "ori", "Indo-European"),
        Language("Ossetian, Ossetic", "os", "oss", "oss", "Indo-European"),
        Language("Panjabi, Punjabi", "pa", "pan", "pan", "Indo-European"),
        Language("Pali", "pi", "pli", "pli", "Indo-European"),
        Language("Persian", "fa", "fas", "per", "Indo-European"),
        Language("Polish", "pl", "pol", "pol", "Indo-European"),
        Language("Pashto, Pushto", "ps", "pus", "pus", "Indo-European"),
        Language("Portuguese", "pt", "por", "por", "Indo-European"),
        Language("Quechua", "qu", "que", "que", "Quechuan"),
        Language("Romansh", "rm", "roh", "roh", "Indo-European"),
        Language("Rundi", "rn", "run", "run", "Niger–Congo"),
        Language("Romanian, Moldavian, Moldovan", "ro", "ron", "rum", "Indo-European"),
        Language("Russian", "ru", "rus", "rus", "Indo-European"),
        Language("Sanskrit", "sa", "san", "san", "Indo-European"),
        Language("Sardinian", "sc", "srd", "srd", "Indo-European"),
        Language("Sindhi", "sd", "snd", "snd", "Indo-European"),
        Language("Northern Sami", "se", "sme", "sme", "Uralic"),
        Language("Samoan", "sm", "smo", "smo", "Austronesian"),
        Language("Sango", "sg", "sag", "sag", "Creole"),
        Language("Serbian", "sr", "srp", "srp", "Indo-European"),
        Language("Gaelic, Scottish Gaelic", "gd", "gla", "gla", "Indo-European"),
        Language("Shona", "sn", "sna", "sna", "Niger–Congo"),
        Language("Sinhala, Sinhalese", "si", "sin", "sin", "Indo-European"),
        Language("Slovak", "sk", "slk", "slo", "Indo-European"),
        Language("Slovenian", "sl", "slv", "slv", "Indo-European"),
        Language("Somali", "so", "som", "som", "Afro-Asiatic"),
        Language("Southern Sotho", "st", "sot", "sot", "Niger–Congo"),
        Language("Spanish, Castilian", "es", "spa", "spa", "Indo-European"),
        Language("Sundanese", "su", "sun", "sun", "Austronesian"),
        Language("Swahili", "sw", "swa", "swa", "Niger–Congo"),
        Language("Swati", "ss", "ssw", "ssw", "Niger–Congo"),
        Language("Swedish", "sv", "swe", "swe", "Indo-European"),
        Language("Tamil", "ta", "tam", "tam", "Dravidian"),
        Language("Telugu", "te", "tel", "tel", "Dravidian"),
        Language("Tajik", "tg", "tgk", "tgk", "Indo-European"),
        Language("Thai", "th", "tha", "tha", "Tai–Kadai"),
        Language("Tigrinya", "ti", "tir", "tir", "Afro-Asiatic"),
        Language("Tibetan", "bo", "bod", "tib", "Sino-Tibetan"),
        Language("Turkmen", "tk", "tuk", "tuk", "Turkic"),
        Language("Tagalog", "tl", "tgl", "tgl", "Austronesian"),
        Language("Tswana", "tn", "tsn", "tsn", "Niger–Congo"),
        Language("Tonga (Tonga Islands)", "to", "ton", "ton", "Austronesian"),
        Language("Turkish", "tr", "tur", "tur", "Turkic"),
        Language("Tsonga", "ts", "tso", "tso", "Niger–Congo"),
        Language("Tatar", "tt", "tat", "tat", "Turkic"),
        Language("Twi", "tw", "twi", "twi", "Niger–Congo"),
        Language("Tahitian", "ty", "tah", "tah", "Austronesian"),
        Language("Uighur, Uyghur", "ug", "uig", "uig", "Turkic"),
        Language("Ukrainian", "uk", "ukr", "ukr", "Indo-European"),
        Language("Urdu", "ur", "urd", "urd", "Indo-European"),
        Language("Uzbek", "uz", "uzb", "uzb", "Turkic"),
        Language("Venda", "ve", "ven", "ven", "Niger–Congo"),
        Language("Vietnamese", "vi", "vie", "vie", "Austroasiatic"),
        Language("Volapük", "vo", "vol", "vol", "Constructed"),
        Language("Walloon", "wa", "wln", "wln", "Indo-European"),
        Language("Welsh", "cy", "cym", "wel", "Indo-European"),
        Language("Wolof", "wo", "wol", "wol", "Niger–Congo"),
        Language("Western Frisian", "fy", "fry", "fry", "Indo-European"),
        Language("Xhosa", "xh", "xho", "xho", "Niger–Congo"),
        Language("Yiddish", "yi", "yid", "yid", "Indo-European"),
        Language("Yoruba", "yo", "yor", "yor", "Niger–Congo"),
        Language("Zhuang, Chuang", "za", "zha", "zha", "Tai–Kadai"),
        Language("Zulu", "zu", "zul", "zul", "Niger–Congo")
    ]

    def config_option_2(self):
        '''returns a list of 2 letter codes'''
        return [ConfigOption(x.iso_639_1(), x.name()) for x in self._LANGUAGES]

    def config_option_3t(self):
        '''returns a list of 3 letter local codes'''
        return [ConfigOption(x.iso_639_2t(), x.name()) for x in self._LANGUAGES]

    def config_option_3b(self):
        '''returns a list of 3 letter English codes'''
        return [ConfigOption(x.iso_639_2b(), x.name()) for x in self._LANGUAGES]

    def get_name_from_2(self, code):
        '''gets the name from the 2 letter code'''
        for language in self._LANGUAGES:
            if language.iso_639_1() == code:
                return language.name()
        return None

    def get_name_from_3t(self, code):
        '''gets the name from the 3 letter local code'''
        for language in self._LANGUAGES:
            if language.iso_639_2t() == code:
                return language.name()
        return None

    def get_name_from_3b(self, code):
        '''gets the name from the 3 letter English code'''
        for language in self._LANGUAGES:
            if language.iso_639_2b() == code:
                return language.name()
        return None

    def convert_2_to_3t(self, code):
        '''converts from 2 letter code to 3 letter local code'''
        for language in self._LANGUAGES:
            if language.iso_639_1() == code:
                return language.iso_639_2t()
        return None

    def convert_2_to_3b(self, code):
        '''converts from 2 letter code to 3 letter English code'''
        for language in self._LANGUAGES:
            if language.iso_639_1() == code:
                return language.iso_639_2t()
        return None

    def convert_3t_to_2(self, code):
        '''converts from 3 letter local code to 2 letter code'''
        for language in self._LANGUAGES:
            if language.iso_639_2t() == code:
                return language.iso_639_1()
        return None

    def convert_3t_to_3b(self, code):
        '''converts from 3 letter local code to 3 letter English code'''
        for language in self._LANGUAGES:
            if language.iso_639_2t() == code:
                return language.iso_639_2b()
        return None

    def convert_3b_to_2(self, code):
        '''converts from 3 letter English code to 2 letter code'''
        for language in self._LANGUAGES:
            if language.iso_639_2b() == code:
                return language.iso_639_1()
        return None

    def convert_3b_to_3t(self, code):
        '''converts from 3 letter English code to 3 letter local code'''
        for language in self._LANGUAGES:
            if language.iso_639_2b() == code:
                return language.iso_639_2t()
        return None
