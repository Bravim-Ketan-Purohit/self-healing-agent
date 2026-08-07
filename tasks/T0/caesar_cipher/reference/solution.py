def caesar_cipher(text: str, shift: int) -> str:
    """Shift each letter by shift positions, wrapping around. Preserve case, non-alpha unchanged."""
    result = []
    for ch in text:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            result.append(chr((ord(ch) - base + shift) % 26 + base))
        else:
            result.append(ch)
    return "".join(result)
