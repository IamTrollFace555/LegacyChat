TITLE_DICT = {
    "0": "Building your profile",
    "1": "The Early Years: Foundations of a Life<br>(Chapter 1)",
    "2": "Teenage Revelations: Navigating Change and Discovery<br>(Chapter 2)",
    "3": "Into Adulthood: The Awakening of Purpose<br>(Chapter 3)",
    "4": "Personal Milestones: Love, Family, and Personal Growth<br>(Chapter 4)",
    "5": "Mature Reflections: A Lifetime of Lessons Learned<br>(Chapter 5)",
    "6": "Golden Years: Embracing Wisdom and Legacy<br>(Chapter 6)",
}

SHORT_NAMES = [
    ("chapter0", "Author Foreword"),
    ("chapter1", "The Early Years"),
    ("chapter2", "Teenage Revelations"),
    ("chapter3", "Into Adulthood"),
    ("chapter4", "Personal Milestones"),
    ("chapter5", "Mature Reflections"),
    ("chapter6", "Golden Years"),
]

SUBCHAPTER_LIST = {

    "ch1": {
        "sch0": "",
        "sch1": "Roots and Beginnings",  # 1, 4, 2, 3, 5, 16
        "sch2": "Exploring Childhood Joys and Challenges",  # 6, 7, 8, 10, 12
        "sch3": "Early Education and Dreams",  # 11, 15, 17, 14
        "sch4": "Treasured Memories and Influences",  # 13, 9, 18, 19
        "sch5": "Reflections on Early Years",  # 20
    },

    "ch2": {
        "sch0": "",
        "sch1": "Transitioning into Adolescence",  # 1-4
        "sch2": "Family and Personal Evolution",  # 5-8
        "sch3": "Decisions and Turning Points",  # 9-12
        "sch4": "Challenges and Resilience",  # 13-16
        "sch5": "Milestones and Experiences",  # 17-20
    },
}

SUBCHAPTER_QUESTIONS = {
    "ch1": {
        "sch0": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
        "sch1": [1, 2, 3, 4, 5, 16],
        "sch2": [6, 7, 8, 10, 12],
        "sch3": [11, 14, 15, 17],
        "sch4": [9, 17, 18, 19],
        "sch5": [20],
    },

    "ch2": {
        "sch0": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
        "sch1": [1, 2, 3, 4],
        "sch2": [5, 6, 7, 8],
        "sch3": [9, 10, 11, 12],
        "sch4": [13, 14, 15, 16],
        "sch5": [17, 18, 19, 20],
    },
}

CH_DICT = lambda x: "ch" + x if x != "0" else "profile"

QUESTIONNAIRE_DICT = {
            "0": "profile",
            "1": "Chapter 1: The Early Years: Foundations of a Life",
            "2": "Chapter 2: Teenage Revelations: Navigating Change and Discovery",
            "3": "Chapter 3: Into Adulthood: The Awakening of Purpose",
            "4": "Chapter 4: Personal Milestones: Love, Family, and Personal Growth",
            "5": "Chapter 5: Mature Reflections: A Lifetime of Lessons Learned",
            "6": "Chapter 6: Golden Years: Embracing Wisdom and Legacy",
        }
