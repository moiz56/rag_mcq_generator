import re
from sympy import sympify, SympifyError

# Regex to extract inline \( ... \) and display \[ ... \] LaTeX
LATEX_PATTERN = re.compile(r"\\\((.*?)\\\)|\\\[(.*?)\\\]")

def extract_latex_fragments(option_text):
    """
    Returns a list of LaTeX fragments from a string.
    """
    fragments = []
    for m in LATEX_PATTERN.finditer(option_text):
        # m.groups() returns a tuple: (group1, group2)
        frag = m.group(1) or m.group(2)
        if frag:
            fragments.append(frag)
    return fragments

def is_valid_math_latex(fragment):
    """
    Returns True if the LaTeX fragment can be parsed by SymPy.
    """
    try:
        sympify(fragment)
        return True
    except SympifyError:
        return False
    except Exception:
        return False

def check_option_math(option_text):
    """
    Checks all LaTeX fragments in a single option.
    Returns list of invalid fragments (empty if all valid).
    """
    invalid = []
    fragments = extract_latex_fragments(option_text)
    for frag in fragments:
        if not is_valid_math_latex(frag):
            invalid.append(frag)
    return invalid

def check_mcq_options(mcq_dict):
    """
    Checks all options (A-D) in a MCQ dict.
    Returns a dict with invalid fragments per option.
    """
    invalid_options = {}
    for opt in ['A','B','C','D']:
        text = mcq_dict.get(opt,"")
        invalid_fragments = check_option_math(text)
        if invalid_fragments:
            invalid_options[opt] = invalid_fragments
    return invalid_options
