class Template:

    def __init__(self, traits=None):
        self.writer_prompt = "You are a helpful assistant\n\n\n"

    def profile_prompt(self, question_dict, answer_dict, params=None):

        prompt = "The following is a set of questions asked to a person and the answers they have provided: " \
                 "\n\n\nQuestions:\n\n"

        for key, value in question_dict.items():
            prompt += f"* {key}: {value}\n"

        prompt += "\n\n\nAnswers\n\n"

        for key, value in answer_dict.items():
            prompt += f"* {key}: {value}\n"

        prompt += ("\n\nThis person wants to write a book about their life, an autobiography. Using the answers " +
                   "provided by the person, write the foreword for the book. Do not mention the fact that the person "
                   f"answered a questionnaire. Do not include things such as 'on question 19 ...' or mention literal "
                   f"answers from the questionnaire. Since this is an autobiography, the text should be in first "
                   f"person form, as if you were that person telling your own story.\n\nUse the"
                   f"following traits:\n"
                   + f"Tone: {params['tone']}. This means that you have to write using a {params['tone']} tone.\n" +
                   f"Writing Level: {params['tone']}. This means you need like a {params['tone']} ")

        return self.writer_prompt + prompt

    def chapter_prompt(self, chapter_name, question_dict, answer_dict, profile_questions, profile_answers, params):

        prompt = f"You are helping a person to write a book about their life. You will help them write the following " \
                 f"chapter: \"{chapter_name}.\"\n\nThe following is a set of questions asked to this person and their" \
                 f"answers to this questions:\n\n\nQuestions:\n\n"

        for key, value in question_dict.items():
            prompt += f"* {key}: {value}\n"

        prompt += "\n\n\nAnswers:\n\n"

        for key, value in answer_dict.items():
            prompt += f"* {key}: {value}\n"

        prompt += f"Also, the person provided some answers to questions describing their personality traits:" \
                  f"\n\n\nQuestions:\n\n"

        for key, value in profile_questions.items():
            prompt += f"* {key}: {value}\n"

        prompt += "\n\n\nAnswers:\n\n"

        for key, value in profile_answers.items():
            prompt += f"* {key}: {value}\n"

        prompt += ("\n\nThis person wants to write a book about their life, an autobiography. Using the answers " +
                   f"provided by the person, write a chapter for the book. Do not mention the fact that the user "
                   f"answered a questionnaire. Do not include things such as 'on question 19 ...' or mention literal "
                   f"answers from the questionnaire. Since this is an autobiography, the text should be in first "
                   f"person form, as if you were that person telling your own story..\n\nThe name of the "
                   f"chapter is:" +
                   f"{chapter_name}\n\nUse the following traits:\n"
                   + f"Tone: {params['tone']}. This means that you have to write using a {params['tone']} tone.\n" +
                   f"Writing Level: {params['level']}. This means you need like a {params['level']}")

        return self.writer_prompt + prompt

    def chapter_prompt_testing(self, question_dict, answer_dict, params):
        questions = ""
        for key, value in question_dict.items():
            questions += f"{key}: {value}\n"

        answers = ""
        for key, value in answer_dict.items():
            answers += f"{key}: {value}\n"

        user_prompt = params["prompt"]
        prompt = user_prompt.replace("{questions}", questions)
        prompt = prompt.replace("{answers}", answers)

        print("PROMPT: ", prompt)
        return prompt
