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


def _cost_of_matrix_multiplication(i,j,k):
    """
    approx cost of multiplying matrices A_ij B_jk
    i is number of rows
    k is number of columns
    j is number of rows and columns
    """
    return j*i*k

def _get_matrix_mult_result_size(matrices):
    assert len(matrices) > 0
    return matrices[0][0], matrices[-1][1]

def _paranths_to_result(matrices, paranths_memo, i, j):
    assert j > i
    if j - i == 1:
        return matrices[i]
    if j - i == 2:
        return matrices[i:j]
    k = paranths_memo[(i, j)]
    left = _paranths_to_result(matrices=matrices, paranths_memo=paranths_memo, i=i, j=k)
    right = _paranths_to_result(matrices=matrices, paranths_memo=paranths_memo, i=k, j=j)
    result = [left, right]
    return result

def _paranthesize(i, j, matrix_sizes, cost_memo, paranths_memo):
    if (i,j) in cost_memo:
        assert (i,j) in paranths_memo
        return cost_memo[(i,j)]
    current_min_cost = inf
    current_min_k = inf
    for k in range(i+1,j):
        assert k != i
        assert k != j
        left_matrix_size = _get_matrix_mult_result_size(matrix_sizes[i:k])
        right_matrix_size = _get_matrix_mult_result_size(matrix_sizes[k:j])
        assert left_matrix_size[1] == right_matrix_size[0], f"invalid shapes of matrices to be multiplied"
        if k-i <= 1:
            left_cost = 1
        else:
            left_cost = _paranthesize(i=i, j=k, matrix_sizes=matrix_sizes, cost_memo=cost_memo, paranths_memo=paranths_memo)
        if j-k <= 1:
            right_cost = 1
        else:
            right_cost = _paranthesize(i=k, j=j, matrix_sizes=matrix_sizes, cost_memo=cost_memo, paranths_memo=paranths_memo)
        outer_cost = _cost_of_matrix_multiplication(left_matrix_size[0],left_matrix_size[1],right_matrix_size[1])
        total_cost = outer_cost + left_cost + right_cost
        if total_cost < current_min_cost:
            current_min_cost = total_cost
            current_min_k = k
    cost_memo[(i,j)] = current_min_cost
    paranths_memo[(i,j)] = current_min_k
    return cost_memo[(i,j)]

def paranthesize_matrix_multiplication(matrix_sizes):
    cost_memo = {}
    paranths_memo = {}
    _ = _paranthesize(
        i=0,j=len(matrix_sizes),
        matrix_sizes=matrix_sizes,
        cost_memo=cost_memo,
        paranths_memo=paranths_memo
    )
    return _paranths_to_result(
        matrices=matrix_sizes, paranths_memo=paranths_memo, i=0, j=len(matrix_sizes)
    )
