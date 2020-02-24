''' audio format options'''
def audio_format_options(obj):
    '''returns the list of audio formats'''
    return [
        obj("pcm", "PCM"),
        obj("mp2", "MP2"),
        obj("mp3", "MP3"),
        obj("ogg", "Vorbis (ogg)"),
        obj("flac", "Free Lossless Audio Codec (flac)"),
        obj("ac3", "Dolby Digital (AC-3)"),
        obj("aac", "Advanced Audio Coding (AAC)"),
        obj("dts5.1", "Digital Theater Systems (DTS)"),
        obj("dd+", "Dolby Digital Plus (DD+)"),
        obj("dtshdma", "DTS-HD Master Audio"),
        obj("dthd", "Dolby TrueHD"),
        obj("dtshdhr", "DTS-HD High Resolution"),
        obj("dtsx", "DTS:X"),
        obj("da", "Dolby Atmos"),
        obj("a3d", "Auro 3D")
    ]
