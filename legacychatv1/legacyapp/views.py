import mimetypes

from django.http import HttpResponse
from django.shortcuts import render, redirect
from .modules.GPT.openai_API import generate_chapter_API, generate_chapter_testing_API
from fireapp.views import (
    get_user_personal_data,
    get_questionnaire,
    get_user_answers,
    get_user_book_chapters,
    consume_chapter_token,
    get_user_dashboard_table,
    user_chapter_setup,
    set_generated_chapter,
    save_edited_chapters,
    setup_chapter_answers,
)

from .modules.titles import (
    TITLE_DICT,
    SHORT_NAMES,
    SUBCHAPTER_LIST,
    CH_DICT,
    SUBCHAPTER_QUESTIONS,
    QUESTIONNAIRE_DICT,

)

from fpdf import FPDF

from random import random


# Create your views here.
def homepage(request):
    return render(request, "homepage.html")


# def dashboard(request):
#     if request.session.get("user_id"):
#         user_id = request.session.get("user_id")
#         data = get_user_personal_data(user_id)
#
#         data["table"] = get_user_dashboard_table(user_id)
#         data["names"] = SHORT_NAMES
#
#         return render(request, "dashboard.html", data)


def dashboard2(request):
    if request.session.get("user_id"):
        user_id = request.session.get("user_id")
        data = get_user_personal_data(user_id)

        data["table"] = get_user_dashboard_table(user_id)
        data["names"] = [[y for y in x] for x in SHORT_NAMES]
        for chapter in range(len(SUBCHAPTER_LIST)):
            try:
                data["names"][chapter].append(
                    [("sch" + str(i), SUBCHAPTER_LIST[CH_DICT(str(chapter))]["sch" + str(i)]) for i in
                     range(1, len(SUBCHAPTER_LIST[CH_DICT(str(chapter))]))])
            except:
                data["names"][chapter].append(
                    [("sch" + str(i), "") for i in
                     range(1, len(SUBCHAPTER_LIST[CH_DICT(str(chapter))]))])

        data["audio_file"] = "media/hello.wav"

        return render(request, "dashboard_v2.html", data)


def choose_subchapter(request):
    if request.method == "POST":
        response = request.POST
        chapter = response["chapter"]
        print("IM HEREEEEEEEEEEEEEEEEEEEEE")

        return render(
            request,
            "choose-subchapter.html",
            dict(subchapters=SUBCHAPTER_LIST[CH_DICT(chapter)],
                 counter=["sch" + str(i) for i in range(1, len(SUBCHAPTER_LIST[CH_DICT(chapter)]))],
                 chapter_name=TITLE_DICT[chapter],
                 chapter=chapter,
                 )
        )


def questionnaire(request):
    if request.method == "POST":
        response = request.POST
        chapter = str(response["chapter"])

        questions = get_questionnaire(chapter)

        try:
            subchapter = str(response["subchapter"])
            idxs = SUBCHAPTER_QUESTIONS[CH_DICT(chapter)][subchapter]

        except:
            idxs = [i for i in range(1, len(questions) + 1)]
            subchapter = "sch0"

        # Index managing
        indices = ""
        for i in idxs:
            indices += str(i) + " "
        indices = indices[:-1]

        try:
            ID = request.session.get("user_id")
            prev_answers = get_user_answers(ID, chapter)
            if prev_answers is None:
                raise Exception("")
        except:
            prev_answers = {}
            for idx in range(1, len(questions.items()) + 1):
                prev_answers[f"question{idx}"] = ""

        data = []
        for (key, value) in questions.items():
            temp = key[8:]  # Since the keys are in the form questionX where X is the question number, key[8:] just
            # removes the 'question' part
            try:
                prev = prev_answers[key]
            except:
                prev = ""
            data.append({"question_idx": temp, "question": value, "previous_answer": prev})

        if chapter != "0":
            subchapter_name = SUBCHAPTER_LIST[CH_DICT(chapter)][subchapter]
        else:
            subchapter_name = ""

        return render(
            request,
            "questionnaire.html",
            {"data": data,
             "chapter": chapter,
             "subchapter": subchapter,
             "chapter_name": TITLE_DICT[chapter],
             "subchapter_name": subchapter_name,
             "indices": indices,
             "indices_int": idxs}
        )


def chapter_edit(request):
    # try:
    user_id = request.session.get("user_id")

    # Handle if the request comes from a POST form or from the 'generate_chapter()' view
    chapter = ""
    error = ""
    try:
        chapter = str(request.session.get("chapter"))
        if chapter is None:
            raise ValueError("No chapter stored in session!")
        if int(request.session.get("failed")):
            error = True

    except:
        if request.method == "POST":
            response = request.POST
            chapter = response["chapter"]
            error = False

    if chapter is None or chapter == "":
        raise ValueError(f"Chapter must be a string representation of a number, not {chapter}")

    # Show the texts stored in the database
    pages = get_user_book_chapters(user_id, chapter)
    if pages is None:
        user_chapter_setup(user_id)
        pages = get_user_book_chapters(user_id, chapter)

    # print("CHAPTER: ", chapter)
    # print("PAGES: ", pages)

    temp = {key: pages[key]["text"] for key in pages}

    prevs = {}

    for key, value in temp.items():
        prevs[key] = value[: min(200, len(value))] + ("..." if len(value) > 200 else "")

    flag = ""
    if error:
        flag = "You've reached the chapter generation limit!"

    try:
        del request.session['failed']
        # del request.session['chapter']
    except KeyError:
        pass

    text = create_summary(user_id, chapter)

    return render(
        request,
        "edit.html",
        {"chapter": chapter, "chapter_name": TITLE_DICT[chapter], "pages": pages, "prevs": prevs, "flag": flag,
         "text": text})

    # except:
    #     print("EXCEPTION!")
    #     pass


# def generate_chapter(request):
#     try:
#         user_id = request.session.get("user_id")
#         if request.method == "POST":
#             response = request.POST
#             chapter = response["chapter"]
#             creativity = response["Creativity"]
#             tone = response["Tone"]
#             level = response["WritingLevel"]
#
#             pages = get_user_book_chapters(user_id, chapter)
#
#             params = {"creativity": creativity, "tone": tone, "level": level}
#
#             if consume_chapter_token(user_id, chapter):
#                 new_gen = generate_chapter_API(user_id, chapter, params)
#                 # new_gen = "Changed!"
#
#                 texts = []
#                 for dic in pages.values():
#                     texts.append(dic["text"])
#
#                 try:
#                     gen_idx = texts.index("") + 1
#                 except:
#                     gen_idx = 1
#
#                 set_generated_chapter(user_id, chapter, new_gen, params, gen_idx)
#             else:
#                 request.session["failed"] = 1
#
#             request.session["chapter"] = chapter
#             return redirect("../chapter-edit/")
#
#     except:
#         pass


def generate_chapter_testing(request):
    user_id = request.session.get("user_id")
    if request.method == "POST":
        response = request.POST
        chapter = response["chapter"]
        prompt = response["prompt"]
        temperature = response["temperature"]

        pages = get_user_book_chapters(user_id, chapter)

        params = {"prompt": prompt, "temperature": temperature}

        new_gen = generate_chapter_testing_API(user_id, chapter, params)
        # new_gen = "Changed!"

        texts = []
        for dic in pages.values():
            texts.append(dic["text"])

        try:
            gen_idx = texts.index("") + 1
        except:
            gen_idx = 1

        params = {"creativity": temperature, "tone": "Not applicable", "level": "Not applicable"}
        set_generated_chapter(user_id, chapter, new_gen, params, gen_idx)

        request.session["chapter"] = chapter
        return redirect("../chapter-edit/")


def save_answers(request):
    print("SAVEDDDDDDDDDD")
    try:
        user_id = request.session.get("user_id")
        if request.method == "POST":
            response = request.POST
            chapter = response["chapter"]

            gen1 = response["gen_text_1"]
            gen2 = response["gen_text_2"]
            gen3 = response["gen_text_3"]

            save_edited_chapters(user_id, chapter, gen1, gen2, gen3)

            request.session["chapter"] = chapter
            return redirect("../chapter-edit/")

    except:
        pass


def logout(request):
    try:
        del request.session['user_id']
    except KeyError:
        pass
    return redirect("../../")


# def summary(request):
#     try:
#         user_id = request.session.get("user_id")
#         if request.method == "POST":
#             response = request.POST
#             chapter = response["chapter"]
#             flag = ""
#
#             questions = get_questionnaire(chapter)
#             answers = get_user_answers(user_id, chapter)
#             idxs = [f"question{i}" for i in range(1, len(questions) + 1)]
#
#             data = {"questions": questions, "answers": answers, "idxs": idxs, "flag": flag,
#                     "chapter_name": TITLE_DICT[chapter]}
#
#             return render(
#                 request,
#                 "summary.html",
#                 data)
#
#     except:
#         pass


def summary2(request):
    user_id = request.session.get("user_id")
    if request.method == "POST":
        response = request.POST
        chapter = response["chapter"]
        flag = ""

        questions = get_questionnaire(chapter)

        answers = get_user_answers(user_id, chapter)
        if answers is None:
            setup_chapter_answers(user_id, chapter)
            answers = get_user_answers(user_id, chapter)

        idxs = [f"question{i}" for i in range(1, len(questions) + 1)]

        data = {"questions": questions, "answers": answers, "idxs": idxs, "flag": flag,
                "chapter_name": TITLE_DICT[chapter], "chapter": chapter}

        return render(
            request,
            "summary_v2.html",
            data)


def download_summary(request):
    user_id = request.session.get("user_id")
    if request.method == "POST":
        response = request.POST
        chapter = response["chapter"]

        filename = create_summary(user_id, chapter, file=True)
        fl_path = "legacyapp\\static\\" + filename

        fl = open(fl_path, 'r')
        mime_type, _ = mimetypes.guess_type(fl_path)
        response = HttpResponse(fl, content_type=mime_type)
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        print("RESPONSE: ", response)
        return response


def download_book_pdf(request):
    user_id = request.session.get("user_id")
    print("USER_ID:", user_id)
    if request.method == "POST":
        filename = create_book_pdf(user_id)
        fl_path = "legacyapp/static/" + filename

        fl = open(fl_path, 'rb')
        mime_type, _ = mimetypes.guess_type(fl_path)
        print("MIME_TYPE:", mime_type)
        print("FILE:", fl)
        response = HttpResponse(fl, content_type=mime_type)
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        print("RESPONSE: ", response)
        return response


def get_question_audio(chapter, question):
    filename = "hello.wav"
    fl_path = "legacyapp/media/" + filename

    fl = open(fl_path, 'rb')
    mime_type, _ = mimetypes.guess_type(fl_path)
    print("MIME_TYPE:", mime_type)
    print("FILE:", fl)
    response = HttpResponse(fl, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    print("RESPONSE: ", response)
    return response



# ======================================= HELPER FUNCTIONS ======================================= #
def create_summary(user_id, chapter, file=False):
    user_data = get_user_personal_data(user_id)
    questions = get_questionnaire(chapter)
    answers = get_user_answers(user_id, chapter)
    chapter_name = QUESTIONNAIRE_DICT[chapter]

    first_name = user_data["first_name"]
    last_name = user_data["last_name"]
    path = "legacyapp\\static\\"

    if file:
        filename = f"{first_name}_{last_name}.txt".replace(" ", "_")
        with open(path + filename, "w") as file:
            file.write(f"Author: {first_name} {last_name}\nChapter name: {chapter_name}\n\n" +
                       f"=======================================================================\n\n")

            for i in range(1, 21):
                question = questions[f"question{i}"]
                answer = answers[f"question{i}"]

                file.write(f"Question {i}: {question}\nAnswer: {answer}\n\n")

        return filename

    else:
        text = ""
        for i in range(1, 21):
            question = questions[f"question{i}"]
            answer = answers[f"question{i}"]

            text += f"Question {i}: {question}\nAnswer: {answer}\n\n"

        return text


def create_book_pdf(user_id):
    pdf = FPDF()

    user_data = get_user_personal_data(user_id)
    first_name = user_data["first_name"]
    last_name = user_data["last_name"]

    gen = 1

    pdf.add_page()

    for chapter in range(1, 7):
        pdf.set_font("Times", size=15)
        pdf.multi_cell(0, 10, txt=QUESTIONNAIRE_DICT[str(chapter)], align='L')

        pages = get_user_book_chapters(user_id, str(chapter))
        if pages is None:
            user_chapter_setup(user_id)
            pages = get_user_book_chapters(user_id, str(chapter))

        temp = {key: pages[key]["text"] for key in pages}
        text = temp[f"gen{gen}"]

        pdf.set_font("Times", size=12)
        pdf.multi_cell(0, 10, txt=text, align='L')

    # save the pdf with name .pdf
    path = "legacyapp/static/"
    filename = f"{first_name}_{last_name}.pdf".replace(" ", "_")

    pdf.output(path + filename)

    print("PDF CREATED")
    return filename
