from cmath import inf
import math

def _badness(line: list[str], page_width: int) -> int:
    """
    badness of using words in line as single line
    """
    line_width = sum([len(word) for word in line]) + len(line) - 1
    if line_width > page_width: return inf
    return math.pow(page_width - line_width, 3)

def _slices_to_result(words, slices):
    result = []
    i = 0
    sorted_slices = sorted(list(slices))
    sorted_slices.append(len(words))
    for j in sorted_slices:
        current_line = []
        current_line.extend(words[i:j])
        result.append(current_line)
        i = j
    return result

def _calc_suffixes_badness(words, page_width, i, badness_memo, slices_memo: dict[int, set[int]]) -> tuple[int, set[int]]:
    """
    justify words[i:] which includes words[i]
    """
    if i in badness_memo:
        assert i in slices_memo
        return badness_memo[i], slices_memo[i]
    current_minimum_badness = inf
    current_minimum_slice_end = inf
    current_minimum_slices = set()
    for j in range(i+1, len(words)):
        current_badness = _badness(line=words[i:j], page_width=page_width)
        if current_badness == inf:
            # probably cant fit more words, no need to check more
            break
        if j == len(words) - 1:
            total_badness = current_badness
            total_slices = set({j})
        else:
            suffixes_badness, suffixes_slices = _calc_suffixes_badness(
                words=words, page_width=page_width,
                i=j, badness_memo=badness_memo, slices_memo=slices_memo
            )
            total_badness = suffixes_badness + current_badness
            assert j not in suffixes_slices
            total_slices = suffixes_slices.union({j})
        if current_minimum_badness > total_badness:
            current_minimum_badness = total_badness
            current_minimum_slices = total_slices
            current_minimum_slice_end = j
    assert current_minimum_badness is not inf
    assert current_minimum_slice_end is not inf
    badness_memo[i] = current_minimum_badness
    slices_memo[i] = current_minimum_slices
    return badness_memo[i], slices_memo[i]

def justify_words(page_width: int, words: list) -> list [list [str]]:
    total_badness_memo = dict()
    slices_memo = dict()
    badness, slices = _calc_suffixes_badness(
        words=words,
        page_width=page_width,
        i=0,
        badness_memo=total_badness_memo,
        slices_memo=slices_memo
    )
    return _slices_to_result(words, slices)
