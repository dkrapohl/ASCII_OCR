
class TestUserStories:

    def test_story_1(self):
        # case: write a program that can take 1-9 digit file and parse it into actual numbers
        # exists at tests/resources/number_1-9.txt
        assert -1 == 4

    def test_story_2_valid(self):
        # case: calculate the checksum for a given number and identify if it is a valid policy number
        assert '345882865' == 4

    def test_story_2_not_valid(self):
        # case: calculate the checksum for a given number make sure it's NOT a valid policy number
        assert -1 == 4

    def test_story_3(self):
        assert -1 == 4

    def test_story_4(self):
        assert -1 == 4

