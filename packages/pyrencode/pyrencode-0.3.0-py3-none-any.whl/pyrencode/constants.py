from pyrencode.utils import to_bytes

# The bencode 'typecodes' such as i, d, etc have been extended and
# relocated on the base-256 character set.
CHR_LIST = to_bytes(59)
CHR_DICT = to_bytes(60)
CHR_INT = to_bytes(61)
CHR_INT1 = to_bytes(62)
CHR_INT2 = to_bytes(63)
CHR_INT4 = to_bytes(64)
CHR_INT8 = to_bytes(65)
CHR_FLOAT32 = to_bytes(66)
CHR_FLOAT64 = to_bytes(44)
CHR_TRUE = to_bytes(67)
CHR_FALSE = to_bytes(68)
CHR_NONE = to_bytes(69)
CHR_TERM = to_bytes(127)

# Integer breakpoints
INT1_SIZE = 2**7
INT2_SIZE = 2**15
INT4_SIZE = 2**31
INT8_SIZE = 2**63

# Positive integers with value embedded in typecode.
INT_POS_FIXED_START = 0
INT_POS_FIXED_COUNT = 44
INT_POS_FIXED_END = 43

# Negative integers with value embedded in typecode.
INT_NEG_FIXED_START = 70
INT_NEG_FIXED_COUNT = 32
INT_NEG_FIXED_END = 101

# Dictionaries with length embedded in typecode.
DICT_FIXED_START = 102
DICT_FIXED_COUNT = 25
DICT_FIXED_END = 126

# Strings with length embedded in typecode.
STR_FIXED_START = 128
STR_FIXED_COUNT = 64
STR_FIXED_END = 191

# Lists with length embedded in typecode.
LIST_FIXED_START = 192
LIST_FIXED_COUNT = 64
LIST_FIXED_END = 255

# Maximum length of integer when written as base 10 string.
MAX_INT_LENGTH = 64

# Default number of bits for serialized floats,
# either 32 or 64 (also a parameter for dumps()).
DEFAULT_FLOAT_BITS = 32

# Whether strings should be decoded when loading
DECODE_UTF8 = False
