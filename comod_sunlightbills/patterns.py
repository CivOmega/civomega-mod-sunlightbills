"""
contains `PATTERNS`, defining strings that this module may respond to
you can set anything you want here (which you can use in `parser.py`,
but you must set `PATTERNS`)
"""

# patterns for returning info about bills in congress
BILL_PATTERNS = frozenset([
    "what bills are about {topic}?",
    "what laws are about {topic}?",
    "what bills have {congress_person} sponsored?"
])

# patterns for returning info about congresspeople
PERSON_PATTERNS = frozenset([
    "who are the legislators for {zipcode}?",
    "what legislators are {party}?"
])

# IMPORTANT:
#   * all questions must be unique (you can change the variable inside
#     the pattern if the wording is otherwise identical)
#   * the variable must be unique inside the question (you can't have
#     "what are {person} and {person} talking about" but you can have
#     "what are {person1} and {person2} talking about")

PATTERNS = BILL_PATTERNS | PERSON_PATTERNS
