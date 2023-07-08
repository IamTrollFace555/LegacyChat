import tkinter as tk
from tkinter import font, ttk
from GPT_request import get_response
from texts import *
import json
import os

USERNAME = ""
GENERATED = False
RESPONSE = ""


class SampleApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.geometry("1600x900")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.pages = {}
        for PageClass in (HomePage, Questionnaire, EditPage, EndPage):
            page_name = PageClass.__name__
            page = PageClass(parent=container, controller=self)
            self.pages[page_name] = page
            page.grid(row=0, column=0, sticky="nsew")

        self.show_page("HomePage")

    def show_page(self, page_name):
        page = self.pages[page_name]
        page.tkraise()

    def update_user(self):
        end = self.pages["EndPage"]
        end.text = f"That's it! Your book chapter has been saved to {USERNAME}_chapter.txt"
        end.var.set(end.text)
        self.after(100, self.update_user)


class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Custom font for the title of the page
        title_font = font.Font(family="Roboto", size=30, weight="bold")

        label = tk.Label(self, text="Home Page", font=title_font)
        label.grid(row=0, column=0, pady=10, padx=10, columnspan=2)

        # Custom font for the text
        text_font = font.Font(family="Roboto", size=23)

        # Custom font for Questionnaire button
        questionnaire_font = font.Font(family="Roboto", size=20)

        # Create a label with word wrapping
        textbox = tk.Label(self, width=100, wraplength=1600, font=text_font, justify="left")
        textbox.grid(row=1, column=0, pady=10, padx=10, columnspan=2)

        # Set the text in the label
        textbox.config(text=main_page_text)

        questionnaire_button = tk.Button(self, text="Questionnaire",
                                         command=lambda: controller.show_page("Questionnaire"), font=questionnaire_font)
        questionnaire_button.grid(row=2, column=1, pady=35, padx=0)


class Questionnaire(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.textbox_data = {}  # Dictionary to store textbox data

        # Custom font for the title of the page
        title_font = font.Font(family="Roboto", size=30, weight="bold")

        # Custom font for the text
        text_font = font.Font(family="Roboto", size=23)

        label = tk.Label(self, text="Questionnaire", font=title_font)
        label.pack(pady=10, padx=10)

        # Create a frame to hold the questionnaire content
        questionnaire_frame = tk.Frame(self)
        questionnaire_frame.pack(fill="both", expand=True)

        # Create a canvas and scrollbar
        canvas = tk.Canvas(questionnaire_frame)
        scrollbar = ttk.Scrollbar(questionnaire_frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)

        # Load questions from JSON
        with open("profiles/questions.json") as file:
            questions = json.load(file)["questions"]

        # Create a frame to hold the questions
        questions_frame = tk.Frame(canvas)

        # Create labels and textboxes for each question
        for question_key, question_text in questions.items():
            question_label = tk.Label(questions_frame, text=question_text, font=text_font)
            question_label.pack(side="top", anchor="nw")

            answer_textbox = tk.Text(questions_frame, font=text_font, width=100, height=2)
            answer_textbox.pack(side="top", anchor="nw")

            self.textbox_data[question_key] = answer_textbox  # Store textbox reference in the dictionary

        # Configure the canvas to scroll the questions frame
        questions_frame.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=questions_frame, anchor="nw")

        # Create the "Submit" button
        submit_button = tk.Button(self, text="Submit", font=text_font, command=self.submit_questionnaire)
        submit_button.pack(side="right", padx=10, pady=10)

        # Create the "Go to Home" button
        home_button = tk.Button(self, text="Go to Home", font=text_font,
                                command=lambda: controller.show_page("HomePage"))
        home_button.pack(side="left", padx=10, pady=10)

    def submit_questionnaire(self):
        # Retrieve the data from the textboxes
        responses = {}

        for question_key, textbox in self.textbox_data.items():
            answer = textbox.get("1.0", "end-1c")  # Retrieve the text from the textbox
            if question_key == "name":
                responses["name"] = answer
                global USERNAME
                USERNAME = answer
            else:
                responses[question_key] = answer
        name = responses["name"]
        filename = f"{name}.json"

        file_list = os.listdir('profiles/')
        if filename in file_list:
            self.controller.show_page("EditPage")
            return

        # Convert the responses dictionary to JSON format
        json_data = json.dumps({"responses": responses}, indent=2)

        # Save the JSON data to a file
        with open(filename, "w") as file:
            file.write(json_data)

        # Save the file in the profiles folder
        os.rename(filename, f"profiles/{filename}")

        self.controller.show_page("EditPage")


class EditPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Custom font for the title of the page
        title_font = font.Font(family="Roboto", size=30, weight="bold")

        # Custom font for the text
        text_font = font.Font(family="Roboto", size=23)

        label = tk.Label(self, text="About Page", font=title_font)
        label.pack(pady=10, padx=10)

        # Adding a Textbox
        self.textbox = tk.Text(self, font=text_font)

        def generate_chapter():
            global GENERATED
            global RESPONSE

            if USERNAME != "" and not GENERATED:
                RESPONSE = get_response(USERNAME)
                GENERATED = True
                self.textbox.insert("1.0", RESPONSE)

            self.after(100, generate_chapter)

        generate_chapter()

        self.textbox.pack(fill="both", expand=True)

        button = tk.Button(self, text="Go to End Page",
                           command=self.finalize)
        button.pack(pady=10)

    def finalize(self):
        text = self.textbox.get("1.0", "end-1c")
        with open(f"chapters/{USERNAME}.txt", "w") as file:
            file.write(text)

        self.controller.show_page("EndPage")


class EndPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.text = f"That's it! Your book chapter has been saved to {USERNAME}_chapter.txt"
        self.var = tk.StringVar()

        # Custom font for the text
        text_font = font.Font(family="Roboto", size=23)

        self.var.set(self.text)
        label = tk.Label(self, textvariable=self.var,
                         font=text_font)
        label.pack(pady=10, padx=10)


if __name__ == "__main__":
    app = SampleApp()
    app.update_user()
    app.mainloop()
