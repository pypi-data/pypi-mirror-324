_ORD_A = ord('a')

class Bitmask26:
    def __init__(self, word: str):
        ords = set(ord(c) - _ORD_A for c in word.lower())
        self.mask = sum(1 << i for i in ords if 0 <= i < 26)

    def __eq__(self, other: 'Bitmask26'):
        return self.mask == other.mask
    
    def __hash__(self):
        return self.mask

    def __ge__(self, other: 'Bitmask26'):
        return self.mask | other.mask == self.mask

    def __repr__(self) -> str:
        s = ''.join(chr(i + _ORD_A) for i in range(26) if ((1 << i) & self.mask) != 0)
        return f'bm26[{s}]'
