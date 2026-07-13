import difflib

from utils.file_reader import read_file




# ✅ ADD THIS FUNCTION HERE
def get_word_diff(old_text, new_text):
    old_words = old_text.split()
    new_words = new_text.split()

    diff = list(difflib.ndiff(old_words, new_words))

    old_result = []
    new_result = []

    for word in diff:
        if word.startswith("- "):
            old_result.append(f"[{word[2:]}]")
        elif word.startswith("+ "):
            new_result.append(f"[{word[2:]}]")
        elif word.startswith("  "):
            old_result.append(word[2:])
            new_result.append(word[2:])

    return " ".join(old_result), " ".join(new_result)


def compare_docs(text1, text2):
    """
    Compare two DOCX files and detect:
    - Added paragraphs
    - Removed paragraphs
    - Modified paragraphs
    """

    

    matcher = difflib.SequenceMatcher(None, text1, text2)

    changes = []

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():

        # Paragraphs are identical
        if tag == "equal":
            continue

        # New paragraphs inserted
        elif tag == "insert":
            for paragraph in text2[j1:j2]:
                changes.append({
                    "type": "Added",
                    "old": "",
                    "new": paragraph
                })

        # Paragraphs deleted
        elif tag == "delete":
            for paragraph in text1[i1:i2]:
                changes.append({
                    "type": "Removed",
                    "old": paragraph,
                    "new": ""
                })

        # Paragraphs modified
        elif tag == "replace":

            old_paragraphs = text1[i1:i2]
            new_paragraphs = text2[j1:j2]

            max_len = max(len(old_paragraphs), len(new_paragraphs))

            for k in range(max_len):

                old_text = old_paragraphs[k] if k < len(old_paragraphs) else ""
                new_text = new_paragraphs[k] if k < len(new_paragraphs) else ""

                if old_text and new_text:

                    highlight_old, highlight_new = get_word_diff(old_text, new_text)

                    changes.append({
                        "type": "Modified",
                        "old": highlight_old,
                        "new": highlight_new
                    })

                elif old_text:
                    changes.append({
                        "type": "Removed",
                        "old": old_text,
                        "new": ""
                    })

                elif new_text:
                    changes.append({
                        "type": "Added",
                        "old": "",
                        "new": new_text
                    })

    return changes