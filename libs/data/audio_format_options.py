''' audio format options'''
from libs.config_option import ConfigOption


OPTIONS = [
    ConfigOption("pcm", "PCM"),
    ConfigOption("mp2", "MP2"),
    ConfigOption("mp3", "MP3"),
    ConfigOption("ogg", "Vorbis (ogg)"),
    ConfigOption("flac", "Free Lossless Audio Codec (flac)"),
    ConfigOption("ac3", "Dolby Digital (AC-3)"),
    ConfigOption("aac", "Advanced Audio Coding (AAC)"),
    ConfigOption("dts5.1", "Digital Theater Systems (DTS)"),
    ConfigOption("dd+", "Dolby Digital Plus (DD+)"),
    ConfigOption("dtshdma", "DTS-HD Master Audio"),
    ConfigOption("dthd", "Dolby TrueHD"),
    ConfigOption("dtshdhr", "DTS-HD High Resolution"),
    ConfigOption("dtsx", "DTS:X"),
    ConfigOption("da", "Dolby Atmos"),
    ConfigOption("a3d", "Auro 3D")
]
