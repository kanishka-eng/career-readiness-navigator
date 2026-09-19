"""
career_data.py
Final data, matching the approved Career | Skill | Required Level (1-5) sheet.
Edit this file to add/change careers or skills — the UI reads from it directly.
"""

CAREERS = {
    "Data Scientist": {
        "icon": "🔬",
        "tagline": "Turn messy data into decisions.",
        "skills": {
            "Python": 5,
            "Statistics": 5,
            "Machine Learning": 5,
            "SQL": 4,
            "Pandas": 4,
            "Data Visualization": 3,
            "Communication": 2,
        },
    },
    "Software Developer": {
        "icon": "💻",
        "tagline": "Build the products people actually use.",
        "skills": {
            "Data Structures": 5,
            "Algorithms": 5,
            "Java": 4,
            "Git": 4,
            "Python": 3,
            "System Design": 3,
            "Testing": 3,
        },
    },
    "Data Analyst": {
        "icon": "📊",
        "tagline": "Find the story hiding in the numbers.",
        "skills": {
            "Excel": 5,
            "SQL": 5,
            "Data Visualization": 4,
            "Python": 3,
            "Statistics": 3,
            "Communication": 3,
        },
    },
    "Machine Learning Engineer": {
        "icon": "🤖",
        "tagline": "Ship ML models that survive contact with production.",
        "skills": {
            "Python": 5,
            "Machine Learning": 5,
            "Deep Learning": 5,
            "MLOps": 4,
            "Cloud (AWS/GCP)": 4,
            "Git": 3,
            "System Design": 3,
        },
    },
    "Cybersecurity Analyst": {
        "icon": "🛡️",
        "tagline": "Keep the bad actors out.",
        "skills": {
            "Network Security": 5,
            "Risk Assessment": 4,
            "SIEM Tools": 4,
            "Linux": 4,
            "Cryptography": 3,
            "Python": 3,
            "Communication": 3,
        },
    },
}

MAX_LEVEL = 5  # required-level scale used across the whole app

SKILL_CATEGORIES = {
    "Programming": ["Python", "Java"],
    "Data & ML": ["Statistics", "Machine Learning", "Deep Learning", "Pandas", "Data Visualization", "MLOps"],
    "Tools & Infra": ["SQL", "Excel", "Git", "Cloud (AWS/GCP)", "Testing", "Linux"],
    "Core CS": ["Data Structures", "Algorithms", "System Design"],
    "Security": ["Network Security", "Risk Assessment", "SIEM Tools", "Cryptography"],
    "Soft Skills": ["Communication"],
}

RESOURCES = {
    "Python": [("Python for Everybody (Coursera)", "https://www.coursera.org/specializations/python"),
               ("Official Python Tutorial", "https://docs.python.org/3/tutorial/")],
    "Statistics": [("Khan Academy: Statistics", "https://www.khanacademy.org/math/statistics-probability")],
    "Machine Learning": [("Andrew Ng's ML Specialization", "https://www.coursera.org/specializations/machine-learning-introduction")],
    "SQL": [("SQL Tutorial - Mode Analytics", "https://mode.com/sql-tutorial/")],
    "Pandas": [("Pandas Official Docs", "https://pandas.pydata.org/docs/getting_started/index.html")],
    "Data Visualization": [("Kaggle: Data Visualization", "https://www.kaggle.com/learn/data-visualization")],
    "Communication": [("Coursera: Effective Communication", "https://www.coursera.org/learn/wharton-communication-skills")],
    "Data Structures": [("freeCodeCamp: DS & Algorithms", "https://www.freecodecamp.org/learn/javascript-algorithms-and-data-structures/")],
    "Algorithms": [("Coursera: Algorithms, Stanford", "https://www.coursera.org/specializations/algorithms")],
    "Java": [("Java Tutorials (Oracle)", "https://docs.oracle.com/javase/tutorial/")],
    "Git": [("Git Official Docs", "https://git-scm.com/doc")],
    "System Design": [("GitHub: System Design Primer", "https://github.com/donnemartin/system-design-primer")],
    "Testing": [("Real Python: Testing", "https://realpython.com/python-testing/")],
    "Excel": [("Excel Skills for Business (Coursera)", "https://www.coursera.org/specializations/excel")],
    "Deep Learning": [("DeepLearning.AI Specialization", "https://www.coursera.org/specializations/deep-learning")],
    "MLOps": [("MLOps Specialization (Coursera)", "https://www.coursera.org/specializations/machine-learning-engineering-for-production-mlops")],
    "Cloud (AWS/GCP)": [("AWS Skill Builder", "https://skillbuilder.aws/")],
    "Network Security": [("Cisco Intro to Cybersecurity", "https://www.netacad.com/courses/cybersecurity/introduction-cybersecurity")],
    "Risk Assessment": [("NIST Risk Management Framework", "https://csrc.nist.gov/projects/risk-management")],
    "SIEM Tools": [("Splunk Free Training", "https://www.splunk.com/en_us/training.html")],
    "Linux": [("Linux Journey", "https://linuxjourney.com/")],
    "Cryptography": [("Khan Academy: Cryptography", "https://www.khanacademy.org/computing/computer-science/cryptography")],
}

ALL_SKILLS = sorted({s for cat in SKILL_CATEGORIES.values() for s in cat})
