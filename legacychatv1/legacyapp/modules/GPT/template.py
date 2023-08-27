class Template:

    def __init__(self, traits=None):
        self.writer_prompt = "You are a helpful assistant\n\n\n"

    def profile_prompt(self, question_dict, answer_dict):

        prompt = "The following is a set of questions asked to a person and the answers they have provided: " \
                 "\n\n\nQuestions:\n\n"

        for key, value in question_dict.items():
            prompt += f"* {key}: {value}\n"

        prompt += "\n\n\nAnswers\n\n"

        for key, value in answer_dict.items():
            prompt += f"* {key}: {value}\n"

        prompt += ("\n\nThis person wants to write a book about their life, an autobiography. Using the answers "
                   "provided by the person, write the foreword for the book.") \

        return self.writer_prompt + prompt

    def chapter_prompt(self, chapter_name, question_dict, answer_dict, person_profile):

        prompt = f"You are helping a person to write a book about their life. You will help them write the following " \
                 f"chapter: \"{chapter_name}.\"\n\nThe following is a set of questions asked to this person and their" \
                 f"answers to this questions:\n\n\nQuestions:\n\n"
        for key, value in question_dict.items():
            prompt += f"* {key}: {value}\n"

        prompt += "\n\n\nAnswers\n\n"

        for key, value in answer_dict.items():
            prompt += f"* {key}: {value}\n"

        prompt += f"Also, here is a brief description of the person:\n\nDescription:\n\n{person_profile}\n\nYour job " \
                  f"is to use the answers provided by the person and the person description to write the book " \
                  f"chapter in the form of an autobiography"

        return self.writer_prompt + prompt
