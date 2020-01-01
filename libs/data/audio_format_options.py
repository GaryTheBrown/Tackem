''' audio format options'''
from libs.config.obj.data.option import ConfigObjOption


OPTIONS = [
    ConfigObjOption("pcm", "PCM"),
    ConfigObjOption("mp2", "MP2"),
    ConfigObjOption("mp3", "MP3"),
    ConfigObjOption("ogg", "Vorbis (ogg)"),
    ConfigObjOption("flac", "Free Lossless Audio Codec (flac)"),
    ConfigObjOption("ac3", "Dolby Digital (AC-3)"),
    ConfigObjOption("aac", "Advanced Audio Coding (AAC)"),
    ConfigObjOption("dts5.1", "Digital Theater Systems (DTS)"),
    ConfigObjOption("dd+", "Dolby Digital Plus (DD+)"),
    ConfigObjOption("dtshdma", "DTS-HD Master Audio"),
    ConfigObjOption("dthd", "Dolby TrueHD"),
    ConfigObjOption("dtshdhr", "DTS-HD High Resolution"),
    ConfigObjOption("dtsx", "DTS:X"),
    ConfigObjOption("da", "Dolby Atmos"),
    ConfigObjOption("a3d", "Auro 3D")
]
