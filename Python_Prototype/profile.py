import os
import json


def get_profile(name: str) -> None:
    def read_questions():
        with open(r"profiles/questions2.json", 'r') as f:
            lines = f.readlines()
            qs = list(map(lambda x: x[:-1], lines[:-1])) + [lines[-1]]
            return qs

    filename = f"{name}.json"
    file_list = os.listdir('profiles/')
    if filename in file_list:
        print("Continue with the next step")
        return

    f = open('profiles/questions2.json')
    questions = json.load(f)["questions"]
    responses = {"name": name}

    for idx, question in enumerate(questions, start=1):
        q = f"question{idx}"
        answer = input(f"{idx}. {questions[q]} ")
        responses[f"question{idx}"] = answer

    # Convert the responses dictionary to JSON format
    json_data = json.dumps({"responses": responses}, indent=2)

    # Save the JSON data to a file
    with open(filename, "w") as file:
        file.write(json_data)

    os.rename(filename, f"profiles/{filename}")

    print(f"\nQuestionnaire responses have been saved to 'profiles/{filename}'")


# def get_profile(name: str) -> None:
#     def read_questions():
#         with open(r"profiles/questions2.json", 'r') as f:
#             lines = f.readlines()
#             qs = list(map(lambda x: x[:-1], lines[:-1])) + [lines[-1]]
#             return qs
#
#     # List all profiles
#     file_list = os.listdir('profiles/')
#     filename = f"{name}.txt"
#     print(file_list)
#
#     # Check if the person already has a profile created
#     if filename in file_list:
#         print("Continue with the next step")
#         return
#
#     questions = read_questions()
#     with open(f"{name}.txt", "w") as f:
#         for idx, q in enumerate(questions):
#             print("========================================================================")P
#             print(f"{idx + 1}. {q}\n")
#
#             print("Answer:", end="")
#             answer = input()
#
#             f.write(f"{answer}\n")
#
#     os.rename(filename, f"profiles/{filename}")






if __name__ == "__main__":
    name = input("Welcome! Please enter your name to continue: ")
    get_profile(name)
