from PySide_6.utils import CODECS
class Teste:
    def convert(self, formato):
        lista_com_formatos = (
            ("MP4", "libx264"),
            ("WEBM", "libvpx"),
            ("MOV", "mov"),
            ("MPEG-1", "mpeg1video"),
            ("MPEG-2", "mpeg2video"),
            ("MPG", "mpeg2video"),
            ("MPEGPS", "mpeg2video"),
            ("MPEG4", "mpeg4"),
            ("AVI", "msmpeg4"),
            ("WMV", "wmv2"),
            ("FLV", "flv"),
            ("3GPP", "h263p"),
        )
        for item in lista_com_formatos:
            if formato == item[0]:
                print(item[1])

variavel = [x for x, y in CODECS]
print(variavel)