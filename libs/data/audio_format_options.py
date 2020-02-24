''' audio format options'''
from libs.config.obj.data.checkbox import ConfigObjCheckbox


OPTIONS = [
    ConfigObjCheckbox("pcm", "PCM"),
    ConfigObjCheckbox("mp2", "MP2"),
    ConfigObjCheckbox("mp3", "MP3"),
    ConfigObjCheckbox("ogg", "Vorbis (ogg)"),
    ConfigObjCheckbox("flac", "Free Lossless Audio Codec (flac)"),
    ConfigObjCheckbox("ac3", "Dolby Digital (AC-3)"),
    ConfigObjCheckbox("aac", "Advanced Audio Coding (AAC)"),
    ConfigObjCheckbox("dts5.1", "Digital Theater Systems (DTS)"),
    ConfigObjCheckbox("dd+", "Dolby Digital Plus (DD+)"),
    ConfigObjCheckbox("dtshdma", "DTS-HD Master Audio"),
    ConfigObjCheckbox("dthd", "Dolby TrueHD"),
    ConfigObjCheckbox("dtshdhr", "DTS-HD High Resolution"),
    ConfigObjCheckbox("dtsx", "DTS:X"),
    ConfigObjCheckbox("da", "Dolby Atmos"),
    ConfigObjCheckbox("a3d", "Auro 3D")
]
