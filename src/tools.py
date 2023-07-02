def format_size(size_bytes):
    """
    Converts a size in bytes to a human-readable format
    """
    for unit in ['', 'KB', 'MB', 'GB', 'TB']:
        if abs(size_bytes) < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} PB"