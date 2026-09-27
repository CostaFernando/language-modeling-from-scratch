import regex as re

def init_vocab(special_tokens: list[str]) -> dict[int, bytes]:
  vocab_initial_len = 256
  vocab = {}

  for i in range(vocab_initial_len):
    vocab[i] = bytes([i])

  for index, token in enumerate(special_tokens):
    vocab[vocab_initial_len + index] = token.encode("utf-8")

  return vocab

def pre_tokenize(input_text: str, special_tokens: list[str]) -> list[tuple[list[bytes], int]]:
  PAT = r"""'(?:[sdmt]|ll|ve|re)| ?\p{L}+| ?\p{N}+| ?[^\s\p{L}\p{N}]+|\s+(?!\S)|\s+"""

  if special_tokens:
    special_token_pattern = "|".join(re.escape(token) for token in special_tokens)
    chunks = re.split(special_token_pattern, input_text)
  else:
    chunks = [input_text]

  input_text_words = [ ]
  for chunk in chunks:
    for word in re.findall(PAT, chunk):
      input_text_words.append(word)

  pre_token_counts = {}
  for word in input_text_words:
    if word not in pre_token_counts:
      pre_token_counts[word] = 1
    else:
      pre_token_counts[word] += 1


  sequences = []
  for word, frequency in pre_token_counts.items():
    tokens = [bytes([char]) for char in word.encode("utf-8")]
    sequences.append((tokens, frequency))

  return sequences


def count_pairs(sequences: list[tuple[list[bytes], int]]) -> tuple[dict[tuple[bytes, bytes], int], dict[tuple[bytes, bytes], set[int]]]:
    pair_counts = {}
    pair_sequence_indices = {}

    for sequence_index, (tokens, frequency) in enumerate(sequences):
        for i in range(len(tokens) - 1):
            pair = (tokens[i], tokens[i + 1])
            pair_counts[pair] = pair_counts.get(pair, 0) + frequency

            if pair not in pair_sequence_indices:
              pair_sequence_indices[pair] = {sequence_index}
            else:
              pair_sequence_indices[pair].add(sequence_index)

    return pair_counts, pair_sequence_indices

def merge_pair(tokens: list[bytes], winning_pair: tuple[bytes, bytes]) -> list[bytes]:
  tokens_len = len(tokens)
  updated_tokens = []

  i = 0
  while i < tokens_len:
    if i + 1 < tokens_len and (tokens[i], tokens[i + 1]) == winning_pair:
      updated_tokens.append(winning_pair[0] + winning_pair[1])
      i += 2
    else:
      updated_tokens.append(tokens[i])
      i += 1

  return updated_tokens

def train_bpe_tokenizer(input_path: str, vocab_size: int, special_tokens: list[str]) -> tuple[dict[int, bytes], list[tuple[bytes, bytes]]]:
  merges = []
  vocab = init_vocab(special_tokens)

  # pre-tokenization
  with open(input_path, encoding='utf-8') as file:
    input_text = file.read()

  sequences = pre_tokenize(input_text, special_tokens)
  pair_counts, pair_sequence_indices = count_pairs(sequences)

  # merges
  while len(vocab) < vocab_size:
    if not pair_counts or all(value == 0 for value in pair_counts.values()):
      break

    winning_pair = max(
      pair_counts,
      key=lambda pair: (pair_counts[pair], pair),
    )
    winning_pair_sequence_indices = pair_sequence_indices[winning_pair].copy()

    for index in winning_pair_sequence_indices:
      tokens, frequency = sequences[index]

      for token_index in range(len(tokens) - 1):
        pair = (tokens[token_index], tokens[token_index + 1])
        pair_counts[pair] -= frequency
        pair_sequence_indices[pair].discard(index)

      updated_tokens = merge_pair(tokens, winning_pair)

      for token_index in range(len(updated_tokens) - 1):
        pair = (updated_tokens[token_index], updated_tokens[token_index + 1])
        pair_counts[pair] = pair_counts.get(pair, 0) + frequency

        if pair not in pair_sequence_indices:
          pair_sequence_indices[pair] = {index}
        else:
          pair_sequence_indices[pair].add(index)

      sequences[index] = (updated_tokens, frequency)

    merges.append(winning_pair)
    vocab[len(vocab)] = winning_pair[0] + winning_pair[1]

  return (vocab, merges)
