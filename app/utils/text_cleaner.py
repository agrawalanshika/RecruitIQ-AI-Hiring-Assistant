import re


def clean_resume_text(text):

    # Remove extra spaces/tabs
    text = re.sub(r"[ \t]+", " ", text)

    # Remove excessive newlines
    text = re.sub(r"\n{2,}", "\n\n", text)

    # Remove leading/trailing spaces
    text = text.strip()

    return text