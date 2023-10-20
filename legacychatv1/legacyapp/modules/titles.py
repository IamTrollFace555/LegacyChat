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
    ["chapter0", "Author Foreword", "0"],
    ["chapter1", "The Early Years", "1"],
    ["chapter2", "Teenage Revelations", "2"],
    ["chapter3", "Into Adulthood", "3"],
    ["chapter4", "Personal Milestones", "4"],
    ["chapter5", "Mature Reflections", "5"],
    ["chapter6", "Golden Years", "6"],
]

SUBCHAPTER_LIST = {

    "profile": {},

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

    "ch3": {
        "sch0": "",
        "sch1": "Transition and Challenges",  # 1-5
        "sch2": "Achievements and Setbacks",  # 6-10
        "sch3": "Personal Relationships and Romantic Partnerships",  # 11-15
        "sch4": "Self-Discovery and Transitions",  # 16-20
    },

    "ch4": {
            "sch0": "",
            "sch1": "Personal Relationships and Love",  # 1, 3, 13
            "sch2": "Family and Identity",  # 4, 5, 7
            "sch3": "Personal Development and Beliefs",  # 6, 8, 11, 15
            "sch4": "Influence and Mentorship",  # 9, 10, 17
            "sch5": "Challenges and Reflection",  # 2, 12, 14, 16, 18, 20
        },

    "ch5": {
            "sch0": "",
            "sch1": "Self-Reflection and Personal Growth",  # 1, 3, 7, 16
            "sch2": "Life Lessons and Values",  # 2, 8, 15, 20
            "sch3": "Relationships and Connections",  # 5, 11, 12, 18
            "sch4": "Professional and Philanthropic Pursuits",  # 9, 10, 13, 14
            "sch5": "Personal Well-Being and Societal Impact",  # 4, 6, 17, 19
        },

    "ch6": {
            "sch0": "",
            "sch1": "Embracing Aging and Self-Care",  # 1, 3, 4, 9, 13
            "sch2": "Sharing Wisdom and Life Lessons",  # 2, 6, 16
            "sch3": "Relationships and Fulfillment",  # 5, 7, 12, 17
            "sch4": "Exploration and Resilience",  # 8, 11, 15
            "sch5": "Spirituality, Technology, and Reflection",  # 10, 14, 18, 19, 20
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

    "ch3": {
        "sch0": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
        "sch1": [1, 2, 3, 4, 5],
        "sch2": [6, 7, 8, 9, 10],
        "sch3": [11, 12, 13, 14, 15],
        "sch4": [16, 17, 18, 19, 20],
    },

    "ch4": {
        "sch0": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
        "sch1": [1, 3, 13],
        "sch2": [4, 5, 7],
        "sch3": [6, 8, 11, 15],
        "sch4": [9, 10, 17],
        "sch5": [2, 12, 14, 16, 18, 20],
    },

    "ch5": {
        "sch0": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
        "sch1": [1, 3, 7, 16],
        "sch2": [2, 8, 15, 20],
        "sch3": [5, 11, 12, 18],
        "sch4": [9, 10, 13, 14],
        "sch5": [4, 6, 17, 19],
    },

    "ch6": {
        "sch0": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
        "sch1": [1, 3, 4, 9, 13],
        "sch2": [2, 6, 16],
        "sch3": [5, 7, 12, 17],
        "sch4": [8, 11, 15],
        "sch5": [10, 14, 18, 19, 20],
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
