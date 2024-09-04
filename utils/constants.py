ALLOWED_FORMATS = [
    "avi", "AVI", "srt", "SRT", "mkv", "MKV", "mp4", "MP4", "mpg", "MPG",
    "mov", "MOV", "wmv", "WMV", "flv", "FLV", "webm", "WEBM", "3gp", "3GP",
    "vtt", "VTT", "sub", "SUB", "ass", "ASS", "ssa", "SSA"
]

FILE_EXTENSIONS = [
    # Imágenes
    '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg', '.webp',  
    # Videos
    '.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm', '.mpg', '.mpeg', '.3gp',  
    # Audios
    '.mp3', '.wav', '.aac', '.ogg', '.m4a', '.flac', '.wma', '.aiff', '.alac',  
    # Documentos
    '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.txt', '.rtf', '.odt', '.ods', '.odp',  
    # Archivos comprimidos y de imagen de disco
    '.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz', '.iso', '.dmg',  
    # Archivos de código y scripts
    '.html', '.htm', '.css', '.js', '.json', '.xml', '.csv', '.sql', '.php', '.asp', '.aspx', 
    '.jsp', '.py', '.rb', '.java', '.c', '.cpp', '.h', '.hpp', '.cs', '.swift', '.go', '.sh', '.bat', '.cmd', 
    # Archivos ejecutables y de sistema
    '.exe', '.dll', '.bin', '.sys', '.msi', '.apk', '.deb', '.rpm',  
    # Otros
    '.nfo', '.ts', '.m3u8', '.log', '.cfg', '.ini', '.inf', '.plist', 
]

DATABASE_DIRECTORY = "./remembered_database"