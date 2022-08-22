import dynamic_programming as dp

def test_word_justification_dp_simple():
    words = ['i', 'am', 'hello', 'world',]
    result = dp.justify_words(page_width=7, words=words)
    expected_result = [['i', 'am'], ['hello'], ['world']]
    assert expected_result == result

def test_word_justification_dp_complex():
    # lol please work lets see what. happens not sure me I go now
    words = ["lol", "please", "work", "lets", "see", "what.", "happens", "not", "sure", "me", "i", "go", "now"]
    result = dp.justify_words(page_width=12, words=words)
    expected_result = [
        ["lol",  "please"],
        ["work",  "lets"],
        ["see",  "what."],
        ["happens", "not"],
        ["sure", "me", "i", "go"],
        ["now"],
    ]
    assert expected_result == result

def test_paranthesization_matrix_multipliciation_simple():
    matrices = [(5,1),(1,5),(5,1)]
    result = dp.paranthesize_matrix_multiplication(matrices)
    expected_result = [(5,1), [(1,5), (5,1)]]
    assert expected_result == result

def test_paranthesization_matrix_multipliciation_complex():
    matrices = [(5,25), (25,5), (5,1), (1,10), (10,3), (3,30), (30,6)]
    result = dp.paranthesize_matrix_multiplication(matrices)
    expected_result = [
        [
            (5, 25),
            [(25, 5), (5, 1)]
        ],
        [
            [
                [(1, 10), (10, 3)],
                (3, 30)
            ],
            (30, 6)
        ]
    ]
    assert expected_result == result