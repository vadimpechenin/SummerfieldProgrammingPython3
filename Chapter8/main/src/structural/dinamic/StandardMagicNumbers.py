_file_type_magic_pairs = (
    ("BZip", bytes.fromhex("425A")),
    ("GZip", bytes.fromhex("1F8B")),
    ("Java Bytecode", bytes.fromhex("CAFEBABE")),
    ("JPEG Image", bytes.fromhex("FFD8FFE0")),
    ("MIDI", b"MThd"),
    ("PDF", b"%PDF"),
    ("PNG Image", b".PNG"),
    ("PNG Image", b"\x89PNG"),
    ("PostScript", b"%!"),
    ("TIFF Image", bytes.fromhex("49492A00")),
    ("TIFF Image", bytes.fromhex("4D4D002A")),
    ("Unix Executable", b"\x7FELF"),
    ("Unix Executable", b".ELF"),
    ("Windows Executable", b"MZ"),
    ("XPM Image", b"/* XPM */"),
    ("ZIP", bytes.fromhex("504B0304")),
    )


def get_file_type(text, extension):
    if extension.lower() in {".htm", ".html"}:
        return "HTML"
    if text.startswith(b"<?xml"):
        return "XML"
    if text[:2] == b"#!":
        text = text.lower()
        if b"python" in text:
            return "Python Program"
        elif b"perl" in text:
            return "Perl Program"
        else:
            return "Shell Script"
    for file_type, magic in _file_type_magic_pairs:
        if magic == text[:len(magic)]:
            return file_type