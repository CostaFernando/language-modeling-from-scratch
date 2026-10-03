import regex as re
import heapq

BYTE_VOCAB_SIZE = 256
PRE_TOKEN_PATTERN = r"""'(?:[sdmt]|ll|ve|re)| ?\p{L}+| ?\p{N}+| ?[^\s\p{L}\p{N}]+|\s+(?!\S)|\s+"""

Pair = tuple[bytes, bytes]
WeightedSequence = tuple[list[bytes], int]


class Candidate:
    def __init__(self, frequency, pair):
        self.frequency = frequency
        self.pair = pair

    def __lt__(self, other):
        return (self.frequency, self.pair) > (other.frequency, other.pair)


def init_vocab(special_tokens: list[str]) -> dict[int, bytes]:
    vocab = {}
    for byte_value in range(BYTE_VOCAB_SIZE):
        vocab[byte_value] = bytes([byte_value])

    for token_id, token in enumerate(special_tokens, start=BYTE_VOCAB_SIZE):
        vocab[token_id] = token.encode("utf-8")

    return vocab


def pre_tokenize(input_text: str, special_tokens: list[str]) -> list[WeightedSequence]:
    """Count pre-tokens without crossing special-token boundaries."""
    if special_tokens:
        special_token_pattern = "|".join(re.escape(token) for token in special_tokens)
        chunks = re.split(special_token_pattern, input_text)
    else:
        chunks = [input_text]

    pre_token_counts = {}
    for chunk in chunks:
        for pre_token in re.findall(PRE_TOKEN_PATTERN, chunk):
            pre_token_counts[pre_token] = pre_token_counts.get(pre_token, 0) + 1

    sequences = []
    for pre_token, frequency in pre_token_counts.items():
        tokens = [bytes([byte_value]) for byte_value in pre_token.encode("utf-8")]
        sequences.append((tokens, frequency))

    return sequences


def add_sequence_pairs(
    tokens: list[bytes],
    frequency: int,
    sequence_index: int,
    pair_counts: dict[Pair, int],
    pair_sequence_indices: dict[Pair, set[int]],
) -> None:
    """Add a sequence's weighted pair occurrences and index to the global totals."""
    for token_index in range(len(tokens) - 1):
        pair = (tokens[token_index], tokens[token_index + 1])
        pair_counts[pair] = pair_counts.get(pair, 0) + frequency

        if pair not in pair_sequence_indices:
            pair_sequence_indices[pair] = {sequence_index}
        else:
            pair_sequence_indices[pair].add(sequence_index)


def remove_sequence_pairs(
    tokens: list[bytes],
    frequency: int,
    sequence_index: int,
    pair_counts: dict[Pair, int],
    pair_sequence_indices: dict[Pair, set[int]],
) -> None:
    """Remove a sequence's contributions before replacing its tokens."""
    for token_index in range(len(tokens) - 1):
        pair = (tokens[token_index], tokens[token_index + 1])
        pair_counts[pair] -= frequency
        if pair_counts[pair] == 0:
            del pair_counts[pair]
        # A pair may occur repeatedly in the same sequence.
        pair_sequence_indices[pair].discard(sequence_index)


def count_pairs(sequences: list[WeightedSequence]) -> tuple[dict[Pair, int], dict[Pair, set[int]]]:
    pair_counts = {}
    pair_sequence_indices = {}

    for sequence_index, (tokens, frequency) in enumerate(sequences):
        add_sequence_pairs(tokens, frequency, sequence_index, pair_counts, pair_sequence_indices)

    return pair_counts, pair_sequence_indices


def merge_pair(tokens: list[bytes], winning_pair: Pair) -> list[bytes]:
    """Replace non-overlapping matches from left to right."""
    merged_token = winning_pair[0] + winning_pair[1]
    updated_tokens = []
    token_index = 0

    while token_index < len(tokens):
        if token_index + 1 < len(tokens) and (tokens[token_index], tokens[token_index + 1]) == winning_pair:
            updated_tokens.append(merged_token)
            token_index += 2
        else:
            updated_tokens.append(tokens[token_index])
            token_index += 1

    return updated_tokens


def train_bpe_tokenizer(
    input_path: str, vocab_size: int, special_tokens: list[str]
) -> tuple[dict[int, bytes], list[Pair]]:
    """Train BPE by updating pair statistics only for affected sequences."""
    vocab = init_vocab(special_tokens)
    merges = []

    with open(input_path, encoding="utf-8") as file:
        input_text = file.read()

    sequences = pre_tokenize(input_text, special_tokens)
    pair_counts, pair_sequence_indices = count_pairs(sequences)

    candidates = [Candidate(frequency, pair) for pair, frequency in pair_counts.items()]
    heapq.heapify(candidates)

    while len(vocab) < vocab_size:
        if not pair_counts:
            break

        winning_pair = None
        while winning_pair is None and candidates:
            winning_candidate = heapq.heappop(candidates)
            current_count = pair_counts.get(winning_candidate.pair, 0)

            if current_count > 0 and current_count == winning_candidate.frequency:
                winning_pair = winning_candidate.pair

        if winning_pair is None:
            break

        changed_pairs = set()
        # The helpers below modify the original sets, so iterate over a snapshot.
        affected_indices = pair_sequence_indices[winning_pair].copy()

        for sequence_index in affected_indices:
            old_tokens, frequency = sequences[sequence_index]
            remove_sequence_pairs(old_tokens, frequency, sequence_index, pair_counts, pair_sequence_indices)
            for i in range(len(old_tokens) - 1):
                changed_pairs.add((old_tokens[i], old_tokens[i + 1]))

            updated_tokens = merge_pair(old_tokens, winning_pair)
            add_sequence_pairs(updated_tokens, frequency, sequence_index, pair_counts, pair_sequence_indices)
            for i in range(len(updated_tokens) - 1):
                changed_pairs.add((updated_tokens[i], updated_tokens[i + 1]))

            sequences[sequence_index] = (updated_tokens, frequency)

        for pair in changed_pairs:
            current_count = pair_counts.get(pair, 0)

            if current_count > 0:
                heapq.heappush(candidates, Candidate(current_count, pair))

        merges.append(winning_pair)
        vocab[len(vocab)] = winning_pair[0] + winning_pair[1]

    return vocab, merges
