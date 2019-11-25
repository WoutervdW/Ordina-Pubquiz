import unittest

from text_processing.AnswerProcessor import get_score


class AnswerScoringTest(unittest.TestCase):
    correct_answers = [
        # photo questions
        [["Mr. Bean"], ["Shrek"]],
        [["Justin Bieber"], ["Oprah Winfrey"]],
        [["Leonardo Dicaprio"], ["Sean Penn"]],
        [["Max verstappen"]],
        [["Charlie Sheen"], ["Ashton Kutcher"]],
        [["Will Smith"], ["geest", "ghost", "ghost alladin", "geest alladin"]],
        [["Steven Spielberg"], ["Woody Allen"]],
        [["Rihanna"], ["Katy Perry"]],
        [["Arnold Schwarzenegger"], ["Sylvester Stallone"]],
        [["Robert de Niro"], ["Kevin Spacey"]],
        # Algemeen questions (standard)
        [["400 keer", "400 x", "vierhonderd", "four hundred"]],
        [["1980"]],
        [["46", "46m", "46 meter"]],
        [["Fatima"]],
        [["Boeddha", "Buddha"]],
        [["Maestro"]],
        [["Geel"]],
        [["Turkije"]],
        [["V"]],
        [["Utrecht"]],
        # Film & Televisie questions (standard)
        [["Mini"]],
        [["1981"]],
        [["Batman"]],
        [["De krokante krab", "De korstige krab", "the krusty crab"]],
        [["1000000"]],
        [["Michael Chrichton"]],
        [["Robin"]],
        [["Philadelphia"]],
        [["53"]],
        [["Baantjes"]],
        # Music questions
        [["George Michael"], ["Aretha Franklin"], ["I knew you were waiting", "I knew you were waiting for me"]],
        [["Ronnie Flex"], ["Frenna"], ["Energie"]],
        [["Queen"], ["David Bowie"], ["Under Pressure"]],
        [["Marco Borsato"], ["Sita"], ["Lopen op het water"]],
        [["Dolly Parton"], ["Kenny Rogers"], ["Islands in the stream"]],
        [["Akon"], ["Eminem"], ["Smack That"]],
        [["Mental THeo"], ["Charlie Lownoise"], ["Wonderful Days"]],
        [["Robbie Williams"], ["Nicole Kidman"], ["Something Stupid"]],
        [["David Guetta"], ["sia"], ["Titanium"]],
        [["Bonnie st. Claire"], ["Ron Brandsteder"], ["Dokter Bernhard"]]
    ]
    categories = ["photo", "photo", "photo", "photo", "photo", "photo", "photo", "photo", "photo", "photo",
                  "standard", "standard", "standard", "standard", "standard", "standard", "standard", "standard",
                  "standard", "standard",
                  "standard", "standard", "standard", "standard", "standard", "standard", "standard", "standard",
                  "standard", "standard",
                  "music", "music", "music", "music", "music", "music", "music", "music", "music", "music",
                  ]

    def test_answer_scoring(self):
        given_answers = [
            # photo questions
            ["Mr. Bean", "Shrek"],
            ["Justin Bieber", "Oprah Winfrey"],
            ["Leonardo Dicaprio", "Sean Penn"],
            ["Max verstappen"],
            ["Charlie Sheen", "Ashton Kutcher"],
            ["Will Smith", "ghost alladin"],
            ["Steven Spielberg", "Woody Allen"],
            ["Rihanna", "Katy Perry"],
            ["Arnold Schwarzenegger", "Sylvester Stallone"],
            ["Robert de Niro", "Kevin Spacey"],
            # Algemeen questions (standard)
            ["400 keer"],
            ["1980"],
            ["46m"],
            ["Fatima"],
            ["Boeddha"],
            ["Maestro"],
            ["Geel"],
            ["Turkije"],
            ["V"],
            ["Utrecht"],
            # Film & Televisie questions (standard)
            ["Mini"],
            ["1981"],
            ["Batman"],
            ["De krokante krab"],
            ["1000000"],
            ["Michael Chrichton"],
            ["Robin"],
            ["Philadelphia"],
            ["53"],
            ["Baantjes"],
            # Music questions
            ["George Michael", "Aretha Franklin", "I knew you were waiting"],
            ["Ronnie Flex", "Frenna", "Energie"],
            ["Queen", "David Bowie", "Under Pressure"],
            ["Marco Borsato", "Sita", "Lopen op het water"],
            ["Dolly Parton", "Kenny Rogers", "Islands in the stream"],
            ["Akon", "Eminem", "Smack That"],
            ["Mental THeo", "Charlie Lownoise", "Wonderful Days"],
            ["Robbie Williams", "Nicole Kidman", "Something Stupid"],
            ["David Guetta", "sia", "Titanium"],
            ["Bonnie st. Claire", "Ron Brandsteder", "Dokter Bernhard"]
        ]

        score = get_score(given_answers, self.correct_answers, self.categories)
        self.assertEqual(score, 59)

    def test_misspelled_answers(self):
        given_answers = [
            ["Mr Bean", "Shrek"],  # FOTO question
            ["400x"],  # ALGEMEEN question
            ["Mimi"],  # FILM & TELEVISIE question
            ["Ronny Flex", "Frenna", "Energy"]  # MUZIEK question
        ]
        score = get_score(given_answers, self.correct_answers, self.categories)
        self.assertEqual(score, 59)

    def test_each_answer(self):
        for correct_answer, category in self.correct_answers


if __name__ == "__main__":
    test_answer_scoring()


'''
correct_answers = [
        # photo questions
        [["Mr. Bean"], ["Shrek"]],
        [["Justin Bieber"], ["Oprah Winfrey"]],
        [["Leonardo Dicaprio"], ["Sean Penn"]],
        [["Max verstappen"]],
        [["Charlie Sheen"], ["Ashton Kutcher"]],
        [["Will Smith"], ["geest", "ghost", "ghost alladin", "geest alladin"]],
        [["Steven Spielberg"], ["Woody Allen"]],
        [["Rihanna"], ["Katy Perry"]],
        [["Arnold Schwarzenegger"], ["Sylvester Stallone"]],
        [["Robert de Niro"], ["Kevin Spacey"]],
        # Algemeen questions (standard)
        [["400 keer", "400 x", "vierhonderd", "four hundred"]],
        [["1980"]],
        [["46", "46m", "46 meter"]],
        [["Fatima"]],
        [["Boeddha", "Buddha"]],
        [["Maestro"]],
        [["Geel"]],
        [["Turkije"]],
        [["V"]],
        [["Utrecht"]],
        # Film & Televisie questions (standard)
        [["Mini"]],
        [["1981"]],
        [["Batman"]],
        [["De krokante krab", "De korstige krab", "the krusty crab"]],
        [["1000000"]],
        [["Michael Chrichton"]],
        [["Robin"]],
        [["Philadelphia"]],
        [["53"]],
        [["Baantjes"]],
        # Music questions
        [["George Michael"], ["Aretha Franklin"], ["I knew you were waiting", "I knew you were waiting for me"]],
        [["Ronnie Flex"], ["Frenna"], ["Energie"]],
        [["Queen"], ["David Bowie"], ["Under Pressure"]],
        [["Marco Borsato"], ["Sita"], ["Lopen op het water"]],
        [["Dolly Parton"], ["Kenny Rogers"], ["Islands in the stream"]],
        [["Akon"], ["Eminem"], ["Smack That"]],
        [["Mental THeo"], ["Charlie Lownoise"], ["Wonderful Days"]],
        [["Robbie Williams"], ["Nicole Kidman"], ["Something Stupid"]],
        [["David Guetta"], ["sia"], ["Titanium"]],
        [["Bonnie st. Claire"], ["Ron Brandsteder"], ["Dokter Bernhard"]]
    ]
    
categories = ["photo", "photo", "photo", "photo", "photo", "photo", "photo", "photo", "photo", "photo",
              "standard", "standard", "standard", "standard", "standard", "standard", "standard", "standard",
              "standard", "standard",
              "standard", "standard", "standard", "standard", "standard", "standard", "standard", "standard",
              "standard", "standard",
              "music", "music", "music", "music", "music", "music", "music", "music", "music", "music",
              ]
    
given answers = [
        # photo questions
        ["Mr. Bean", "Shrek"],
        ["Justin Bieber", "Oprah Winfrey"],
        ["Leonardo Dicaprio", "Sean Penn"],
        ["Max verstappen"],
        ["Charlie Sheen", ["Ashton Kutcher"]],
        ["Will Smith", "ghost alladin"],
        ["Steven Spielberg", "Woody Allen"],
        ["Rihanna", "Katy Perry"],
        ["Arnold Schwarzenegger", "Sylvester Stallone"],
        ["Robert de Niro", "Kevin Spacey"],
        # Algemeen questions (standard)
        ["400 keer"],
        ["1980"],
        ["46m"],
        ["Fatima"],
        ["Boeddha"],
        ["Maestro"],
        ["Geel"],
        ["Turkije"],
        ["V"],
        ["Utrecht"],
        # Film & Televisie questions (standard)
        ["Mini"],
        ["1981"],
        ["Batman"],
        ["De krokante krab"],
        ["1000000"],
        ["Michael Chrichton"],
        ["Robin"],
        ["Philadelphia"],
        ["53"],
        ["Baantjes"],
        # Music questions
        ["George Michael", "Aretha Franklin", ["I knew you were waiting", "I knew you were waiting for me"]],
        ["Ronnie Flex", "Frenna", "Energie"],
        ["Queen", "David Bowie", "Under Pressure"],
        ["Marco Borsato", "Sita", "Lopen op het water"],
        ["Dolly Parton", "Kenny Rogers", "Islands in the stream"],
        ["Akon", "Eminem", "Smack That"],
        ["Mental THeo", "Charlie Lownoise", "Wonderful Days"],
        ["Robbie Williams", "Nicole Kidman", "Something Stupid"],
        ["David Guetta", "sia", "Titanium"],
        ["Bonnie st. Claire", "Ron Brandsteder", "Dokter Bernhard"]
]
'''
