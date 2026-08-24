"""Small dependency-free BLAKE3 implementation for deterministic receipts."""
from __future__ import annotations

from dataclasses import dataclass

_MASK32 = 0xFFFFFFFF
_IV = (
    0x6A09E667,
    0xBB67AE85,
    0x3C6EF372,
    0xA54FF53A,
    0x510E527F,
    0x9B05688C,
    0x1F83D9AB,
    0x5BE0CD19,
)
_PERMUTATION = (2, 6, 3, 10, 7, 0, 4, 13, 1, 11, 12, 5, 9, 14, 15, 8)
_CHUNK_START = 1
_CHUNK_END = 2
_PARENT = 4
_ROOT = 8
_BLOCK_LEN = 64
_CHUNK_LEN = 1024


def _rotr32(value: int, count: int) -> int:
    return ((value >> count) | (value << (32 - count))) & _MASK32


def _g(state: list[int], a: int, b: int, c: int, d: int, mx: int, my: int) -> None:
    state[a] = (state[a] + state[b] + mx) & _MASK32
    state[d] = _rotr32(state[d] ^ state[a], 16)
    state[c] = (state[c] + state[d]) & _MASK32
    state[b] = _rotr32(state[b] ^ state[c], 12)
    state[a] = (state[a] + state[b] + my) & _MASK32
    state[d] = _rotr32(state[d] ^ state[a], 8)
    state[c] = (state[c] + state[d]) & _MASK32
    state[b] = _rotr32(state[b] ^ state[c], 7)


def _round(state: list[int], message: tuple[int, ...]) -> None:
    _g(state, 0, 4, 8, 12, message[0], message[1])
    _g(state, 1, 5, 9, 13, message[2], message[3])
    _g(state, 2, 6, 10, 14, message[4], message[5])
    _g(state, 3, 7, 11, 15, message[6], message[7])
    _g(state, 0, 5, 10, 15, message[8], message[9])
    _g(state, 1, 6, 11, 12, message[10], message[11])
    _g(state, 2, 7, 8, 13, message[12], message[13])
    _g(state, 3, 4, 9, 14, message[14], message[15])


def _words(block: bytes) -> tuple[int, ...]:
    padded = block.ljust(_BLOCK_LEN, b"\0")
    return tuple(int.from_bytes(padded[index:index + 4], "little") for index in range(0, 64, 4))


def _compress(
    chaining_value: tuple[int, ...],
    block_words: tuple[int, ...],
    counter: int,
    block_len: int,
    flags: int,
) -> tuple[int, ...]:
    state = list(chaining_value) + list(_IV[:4]) + [
        counter & _MASK32,
        (counter >> 32) & _MASK32,
        block_len,
        flags,
    ]
    message = block_words
    for round_index in range(7):
        _round(state, message)
        if round_index != 6:
            message = tuple(message[index] for index in _PERMUTATION)
    return tuple(
        [state[index] ^ state[index + 8] for index in range(8)]
        + [state[index + 8] ^ chaining_value[index] for index in range(8)]
    )


@dataclass(frozen=True)
class _Output:
    input_cv: tuple[int, ...]
    block_words: tuple[int, ...]
    counter: int
    block_len: int
    flags: int

    def chaining_value(self) -> tuple[int, ...]:
        return _compress(
            self.input_cv,
            self.block_words,
            self.counter,
            self.block_len,
            self.flags,
        )[:8]

    def root_bytes(self, length: int = 32) -> bytes:
        output = bytearray()
        output_counter = 0
        while len(output) < length:
            words = _compress(
                self.input_cv,
                self.block_words,
                output_counter,
                self.block_len,
                self.flags | _ROOT,
            )
            output.extend(b"".join(word.to_bytes(4, "little") for word in words))
            output_counter += 1
        return bytes(output[:length])


def _chunk_output(chunk: bytes, chunk_counter: int) -> _Output:
    block_count = max(1, (len(chunk) + _BLOCK_LEN - 1) // _BLOCK_LEN)
    chaining_value = _IV
    for block_index in range(block_count - 1):
        block = chunk[block_index * _BLOCK_LEN:(block_index + 1) * _BLOCK_LEN]
        flags = _CHUNK_START if block_index == 0 else 0
        chaining_value = _compress(
            chaining_value,
            _words(block),
            chunk_counter,
            len(block),
            flags,
        )[:8]
    last_start = (block_count - 1) * _BLOCK_LEN
    last_block = chunk[last_start:last_start + _BLOCK_LEN]
    flags = _CHUNK_END
    if block_count == 1:
        flags |= _CHUNK_START
    return _Output(chaining_value, _words(last_block), chunk_counter, len(last_block), flags)


def _parent_output(left_cv: tuple[int, ...], right_cv: tuple[int, ...]) -> _Output:
    return _Output(_IV, left_cv + right_cv, 0, _BLOCK_LEN, _PARENT)


def _largest_power_of_two_less_than(value: int) -> int:
    return 1 << ((value - 1).bit_length() - 1)


def _subtree_output(data: bytes, chunk_counter: int = 0) -> _Output:
    if len(data) <= _CHUNK_LEN:
        return _chunk_output(data, chunk_counter)
    chunk_count = (len(data) + _CHUNK_LEN - 1) // _CHUNK_LEN
    left_chunks = _largest_power_of_two_less_than(chunk_count)
    split = left_chunks * _CHUNK_LEN
    left = _subtree_output(data[:split], chunk_counter)
    right = _subtree_output(data[split:], chunk_counter + left_chunks)
    return _parent_output(left.chaining_value(), right.chaining_value())


def blake3(data: bytes) -> bytes:
    """Return the 32-byte unkeyed BLAKE3 digest for *data*."""
    return _subtree_output(data).root_bytes(32)


def blake3_hex(data: bytes) -> str:
    """Return the lowercase hexadecimal BLAKE3 digest for *data*."""
    return blake3(data).hex()
