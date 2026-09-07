"""
Static seed content for the one English -> Spanish course (spec section 8).

Kept as plain Python data structures (not hardcoded into seed_data.py)
so the content itself is easy to review/extend independently of the
seeding mechanics. Every exercise type required by the spec
(multiple_choice, translate, word_bank, match, fill_blank, type_answer)
appears at least once across the seeded lessons.
"""
from __future__ import annotations

from app.models.exercise import ExerciseType

MC = ExerciseType.MULTIPLE_CHOICE.value
TR = ExerciseType.TRANSLATE.value
WB = ExerciseType.WORD_BANK.value
MATCH = ExerciseType.MATCH.value
FB = ExerciseType.FILL_BLANK.value
TA = ExerciseType.TYPE_ANSWER.value


COURSE = {
    "name": "Spanish for English Speakers",
    "source_language": "English",
    "target_language": "Spanish",
    "units": [
        {
            "title": "Basics",
            "description": "Greetings, food, and everyday words.",
            "skills": [
                {
                    "title": "Greetings",
                    "description": "Say hello and goodbye.",
                    "lessons": [
                        {
                            "title": "Greetings 1",
                            "exercises": [
                                {
                                    "type": MC,
                                    "question": "What does 'hola' mean?",
                                    "correct_answer": "Hello",
                                    "options": ["Hello", "Goodbye", "Thank you", "Please"],
                                },
                                {
                                    "type": TR,
                                    "question": "Translate: Hello",
                                    "correct_answer": "Hola",
                                },
                                {
                                    "type": WB,
                                    "question": "Build: Good morning",
                                    "correct_answer": "Buenos dias",
                                    "options": ["Buenos", "dias", "noches", "tardes"],
                                },
                                {
                                    "type": FB,
                                    "question": "___ dias (Good day)",
                                    "correct_answer": "Buenos",
                                },
                                {
                                    "type": TA,
                                    "question": "Translate: Goodbye",
                                    "correct_answer": "Adios",
                                },
                                {
                                    "type": MC,
                                    "question": "What does 'gracias' mean?",
                                    "correct_answer": "Thank you",
                                    "options": ["Hello", "Goodbye", "Thank you", "Please"],
                                },
                            ],
                        },
                        {
                            "title": "Greetings 2",
                            "exercises": [
                                {
                                    "type": MATCH,
                                    "question": "Match the pairs",
                                    "correct_answer": "hello-hola,goodbye-adios,please-por favor",
                                    "data": {
                                        "pairs": [
                                            {"left": "hello", "right": "hola"},
                                            {"left": "goodbye", "right": "adios"},
                                            {"left": "please", "right": "por favor"},
                                        ]
                                    },
                                },
                                {
                                    "type": TR,
                                    "question": "Translate: Please",
                                    "correct_answer": "Por favor",
                                },
                                {
                                    "type": TA,
                                    "question": "Translate: Thank you",
                                    "correct_answer": "Gracias",
                                },
                                {
                                    "type": MC,
                                    "question": "What does 'buenas noches' mean?",
                                    "correct_answer": "Good night",
                                    "options": ["Good morning", "Good night", "Good afternoon", "Goodbye"],
                                },
                                {
                                    "type": FB,
                                    "question": "Buenas ___ (Good night)",
                                    "correct_answer": "noches",
                                },
                                {
                                    "type": WB,
                                    "question": "Build: See you later",
                                    "correct_answer": "Hasta luego",
                                    "options": ["Hasta", "luego", "manana", "pronto"],
                                },
                            ],
                        },
                    ],
                },
                {
                    "title": "Food",
                    "description": "Talk about food and drink.",
                    "lessons": [
                        {
                            "title": "Food 1",
                            "exercises": [
                                {
                                    "type": MC,
                                    "question": "What does 'pan' mean?",
                                    "correct_answer": "Bread",
                                    "options": ["Bread", "Water", "Rice", "Milk"],
                                },
                                {
                                    "type": WB,
                                    "question": "Build: I eat bread",
                                    "correct_answer": "Yo como pan",
                                    "options": ["Yo", "como", "pan", "agua"],
                                },
                                {
                                    "type": FB,
                                    "question": "Yo ___ pan. (I eat bread.)",
                                    "correct_answer": "como",
                                },
                                {
                                    "type": TR,
                                    "question": "Translate: Water",
                                    "correct_answer": "Agua",
                                },
                                {
                                    "type": TA,
                                    "question": "Translate: Rice",
                                    "correct_answer": "Arroz",
                                },
                                {
                                    "type": MC,
                                    "question": "What does 'leche' mean?",
                                    "correct_answer": "Milk",
                                    "options": ["Bread", "Water", "Rice", "Milk"],
                                },
                            ],
                        },
                        {
                            "title": "Food 2",
                            "exercises": [
                                {
                                    "type": MATCH,
                                    "question": "Match the pairs",
                                    "correct_answer": "food-comida,water-agua,bread-pan",
                                    "data": {
                                        "pairs": [
                                            {"left": "food", "right": "comida"},
                                            {"left": "water", "right": "agua"},
                                            {"left": "bread", "right": "pan"},
                                        ]
                                    },
                                },
                                {
                                    "type": TR,
                                    "question": "Translate: Food",
                                    "correct_answer": "Comida",
                                },
                                {
                                    "type": WB,
                                    "question": "Build: I drink water",
                                    "correct_answer": "Yo bebo agua",
                                    "options": ["Yo", "bebo", "agua", "leche"],
                                },
                                {
                                    "type": FB,
                                    "question": "Yo ___ agua. (I drink water.)",
                                    "correct_answer": "bebo",
                                },
                                {
                                    "type": TA,
                                    "question": "Translate: Cheese",
                                    "correct_answer": "Queso",
                                },
                                {
                                    "type": MC,
                                    "question": "What does 'manzana' mean?",
                                    "correct_answer": "Apple",
                                    "options": ["Apple", "Orange", "Banana", "Grape"],
                                },
                            ],
                        },
                    ],
                },
                {
                    "title": "Everyday Words",
                    "description": "Common everyday vocabulary.",
                    "lessons": [
                        {
                            "title": "Everyday Words 1",
                            "exercises": [
                                {
                                    "type": MC,
                                    "question": "What does 'casa' mean?",
                                    "correct_answer": "House",
                                    "options": ["House", "Car", "Dog", "Book"],
                                },
                                {
                                    "type": TR,
                                    "question": "Translate: Book",
                                    "correct_answer": "Libro",
                                },
                                {
                                    "type": WB,
                                    "question": "Build: The big house",
                                    "correct_answer": "La casa grande",
                                    "options": ["La", "casa", "grande", "pequena"],
                                },
                                {
                                    "type": FB,
                                    "question": "La casa ___. (The big house.)",
                                    "correct_answer": "grande",
                                },
                                {
                                    "type": TA,
                                    "question": "Translate: Car",
                                    "correct_answer": "Carro",
                                },
                                {
                                    "type": MC,
                                    "question": "What does 'perro' mean?",
                                    "correct_answer": "Dog",
                                    "options": ["Cat", "Dog", "Bird", "Fish"],
                                },
                            ],
                        },
                        {
                            "title": "Everyday Words 2",
                            "exercises": [
                                {
                                    "type": MATCH,
                                    "question": "Match the pairs",
                                    "correct_answer": "house-casa,book-libro,dog-perro",
                                    "data": {
                                        "pairs": [
                                            {"left": "house", "right": "casa"},
                                            {"left": "book", "right": "libro"},
                                            {"left": "dog", "right": "perro"},
                                        ]
                                    },
                                },
                                {
                                    "type": TR,
                                    "question": "Translate: Cat",
                                    "correct_answer": "Gato",
                                },
                                {
                                    "type": WB,
                                    "question": "Build: My small dog",
                                    "correct_answer": "Mi perro pequeno",
                                    "options": ["Mi", "perro", "pequeno", "grande"],
                                },
                                {
                                    "type": FB,
                                    "question": "Mi perro ___. (My small dog.)",
                                    "correct_answer": "pequeno",
                                },
                                {
                                    "type": TA,
                                    "question": "Translate: Bird",
                                    "correct_answer": "Pajaro",
                                },
                                {
                                    "type": MC,
                                    "question": "What does 'libro' mean?",
                                    "correct_answer": "Book",
                                    "options": ["Book", "Pen", "Table", "Chair"],
                                },
                            ],
                        },
                    ],
                },
            ],
        },
        {
            "title": "Everyday Life",
            "description": "People, home, and activities.",
            "skills": [
                {
                    "title": "People",
                    "description": "Talk about people and family.",
                    "lessons": [
                        {
                            "title": "People 1",
                            "exercises": [
                                {
                                    "type": MC,
                                    "question": "What does 'amigo' mean?",
                                    "correct_answer": "Friend",
                                    "options": ["Friend", "Brother", "Sister", "Mother"],
                                },
                                {
                                    "type": TR,
                                    "question": "Translate: Mother",
                                    "correct_answer": "Madre",
                                },
                                {
                                    "type": WB,
                                    "question": "Build: My good friend",
                                    "correct_answer": "Mi buen amigo",
                                    "options": ["Mi", "buen", "amigo", "hermano"],
                                },
                                {
                                    "type": FB,
                                    "question": "Mi ___ amigo. (My good friend.)",
                                    "correct_answer": "buen",
                                },
                                {
                                    "type": TA,
                                    "question": "Translate: Father",
                                    "correct_answer": "Padre",
                                },
                                {
                                    "type": MC,
                                    "question": "What does 'hermano' mean?",
                                    "correct_answer": "Brother",
                                    "options": ["Brother", "Sister", "Friend", "Cousin"],
                                },
                            ],
                        },
                        {
                            "title": "People 2",
                            "exercises": [
                                {
                                    "type": MATCH,
                                    "question": "Match the pairs",
                                    "correct_answer": "mother-madre,father-padre,friend-amigo",
                                    "data": {
                                        "pairs": [
                                            {"left": "mother", "right": "madre"},
                                            {"left": "father", "right": "padre"},
                                            {"left": "friend", "right": "amigo"},
                                        ]
                                    },
                                },
                                {
                                    "type": TR,
                                    "question": "Translate: Sister",
                                    "correct_answer": "Hermana",
                                },
                                {
                                    "type": WB,
                                    "question": "Build: The whole family",
                                    "correct_answer": "Toda la familia",
                                    "options": ["Toda", "la", "familia", "casa"],
                                },
                                {
                                    "type": FB,
                                    "question": "Toda la ___. (The whole family.)",
                                    "correct_answer": "familia",
                                },
                                {
                                    "type": TA,
                                    "question": "Translate: Family",
                                    "correct_answer": "Familia",
                                },
                                {
                                    "type": MC,
                                    "question": "What does 'hermana' mean?",
                                    "correct_answer": "Sister",
                                    "options": ["Brother", "Sister", "Mother", "Aunt"],
                                },
                            ],
                        },
                    ],
                },
                {
                    "title": "Home",
                    "description": "Rooms and things in the home.",
                    "lessons": [
                        {
                            "title": "Home 1",
                            "exercises": [
                                {
                                    "type": MC,
                                    "question": "What does 'cocina' mean?",
                                    "correct_answer": "Kitchen",
                                    "options": ["Kitchen", "Bedroom", "Bathroom", "Garden"],
                                },
                                {
                                    "type": TR,
                                    "question": "Translate: Bedroom",
                                    "correct_answer": "Dormitorio",
                                },
                                {
                                    "type": WB,
                                    "question": "Build: The clean kitchen",
                                    "correct_answer": "La cocina limpia",
                                    "options": ["La", "cocina", "limpia", "sucia"],
                                },
                                {
                                    "type": FB,
                                    "question": "La cocina ___. (The clean kitchen.)",
                                    "correct_answer": "limpia",
                                },
                                {
                                    "type": TA,
                                    "question": "Translate: Bathroom",
                                    "correct_answer": "Bano",
                                },
                                {
                                    "type": MC,
                                    "question": "What does 'jardin' mean?",
                                    "correct_answer": "Garden",
                                    "options": ["Garden", "Roof", "Door", "Window"],
                                },
                            ],
                        },
                        {
                            "title": "Home 2",
                            "exercises": [
                                {
                                    "type": MATCH,
                                    "question": "Match the pairs",
                                    "correct_answer": "kitchen-cocina,bathroom-bano,garden-jardin",
                                    "data": {
                                        "pairs": [
                                            {"left": "kitchen", "right": "cocina"},
                                            {"left": "bathroom", "right": "bano"},
                                            {"left": "garden", "right": "jardin"},
                                        ]
                                    },
                                },
                                {
                                    "type": TR,
                                    "question": "Translate: Door",
                                    "correct_answer": "Puerta",
                                },
                                {
                                    "type": WB,
                                    "question": "Build: The big garden",
                                    "correct_answer": "El jardin grande",
                                    "options": ["El", "jardin", "grande", "pequeno"],
                                },
                                {
                                    "type": FB,
                                    "question": "El jardin ___. (The big garden.)",
                                    "correct_answer": "grande",
                                },
                                {
                                    "type": TA,
                                    "question": "Translate: Window",
                                    "correct_answer": "Ventana",
                                },
                                {
                                    "type": MC,
                                    "question": "What does 'puerta' mean?",
                                    "correct_answer": "Door",
                                    "options": ["Door", "Window", "Roof", "Wall"],
                                },
                            ],
                        },
                    ],
                },
                {
                    "title": "Activities",
                    "description": "Everyday activities and verbs.",
                    "lessons": [
                        {
                            "title": "Activities 1",
                            "exercises": [
                                {
                                    "type": MC,
                                    "question": "What does 'correr' mean?",
                                    "correct_answer": "To run",
                                    "options": ["To run", "To eat", "To sleep", "To read"],
                                },
                                {
                                    "type": TR,
                                    "question": "Translate: To read",
                                    "correct_answer": "Leer",
                                },
                                {
                                    "type": WB,
                                    "question": "Build: I run every day",
                                    "correct_answer": "Yo corro todos los dias",
                                    "options": ["Yo", "corro", "todos", "los", "dias"],
                                },
                                {
                                    "type": FB,
                                    "question": "Yo ___ todos los dias. (I run every day.)",
                                    "correct_answer": "corro",
                                },
                                {
                                    "type": TA,
                                    "question": "Translate: To sleep",
                                    "correct_answer": "Dormir",
                                },
                                {
                                    "type": MC,
                                    "question": "What does 'leer' mean?",
                                    "correct_answer": "To read",
                                    "options": ["To run", "To read", "To write", "To sing"],
                                },
                            ],
                        },
                        {
                            "title": "Activities 2",
                            "exercises": [
                                {
                                    "type": MATCH,
                                    "question": "Match the pairs",
                                    "correct_answer": "to run-correr,to read-leer,to sleep-dormir",
                                    "data": {
                                        "pairs": [
                                            {"left": "to run", "right": "correr"},
                                            {"left": "to read", "right": "leer"},
                                            {"left": "to sleep", "right": "dormir"},
                                        ]
                                    },
                                },
                                {
                                    "type": TR,
                                    "question": "Translate: To write",
                                    "correct_answer": "Escribir",
                                },
                                {
                                    "type": WB,
                                    "question": "Build: She reads a book",
                                    "correct_answer": "Ella lee un libro",
                                    "options": ["Ella", "lee", "un", "libro"],
                                },
                                {
                                    "type": FB,
                                    "question": "Ella ___ un libro. (She reads a book.)",
                                    "correct_answer": "lee",
                                },
                                {
                                    "type": TA,
                                    "question": "Translate: To sing",
                                    "correct_answer": "Cantar",
                                },
                                {
                                    "type": MC,
                                    "question": "What does 'escribir' mean?",
                                    "correct_answer": "To write",
                                    "options": ["To write", "To run", "To sleep", "To eat"],
                                },
                            ],
                        },
                    ],
                },
            ],
        },
    ],
}
