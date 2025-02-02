import re
import warnings 

def missing_section(clean_text, add_benchmark_sections=None):
    """
    Identifies the sections missing from the resume based on the benchmark sections.

    Parameters
    ----------
    clean_text : str
        The text extracted from the resume.
    add_benchmark_sections : list of str or str, optional
        A list of additional section names (e.g., "Skills", "Education", 
        "Work Experience", "Contact") or a single section name as a string. 
        Defaults to None. If a single string is provided, it will be treated as 
        a list with one element.

    Returns
    -------
    list of str
        A list of section names from the benchmark that are not present in the resume.

    Examples
    --------
    Example 1: With additional benchmark sections as a list

    >>> clean_text = "Skills: Python, Machine Learning\nEducation: B.Sc. in CS"
    >>> add_benchmark_sections = ["Work Experience", "Contact"]
    >>> missing = missing_section(clean_text, add_benchmark_sections)
    Output: ['Work Experience', 'Contact']

    Example 2: With additional benchmark sections as a single string

    >>> clean_text = "Skills: Python, Machine Learning\nEducation: B.Sc. in CS"
    >>> add_benchmark_sections = "Projects"
    >>> missing = missing_section(clean_text, add_benchmark_sections)
    Output: ['Work Experience', 'Contact', 'Projects']

    Example 3: Without additioinal benchmark sections
    
    >>> clean_text = "Skills: Python, Machine Learning\nEducation: B.Sc. in CS"
    >>> missing = missing_section(clean_text)
    Output: ['Work Experience', 'Contact']
    """
    # Chek if 'clean_text' is an empty string
    if clean_text == "":
        warnings.warn("The provided resume text is an empty string. Returning all benchmark sections as missing.", UserWarning)

    if add_benchmark_sections is not None and not (isinstance(add_benchmark_sections, list) or isinstance(add_benchmark_sections, str)):
        raise TypeError(f"Expected a string, list, or None for additional benchmark sections. add_benchmark_sections is a {type(add_benchmark_sections)}")

    # Define hardcoded benchmark sections as a set
    benchmark_sections = {"Skills", "Education", "Work Experience", "Contact"}

    # Convert the single string to a list if necessary
    if isinstance(add_benchmark_sections, str):
        add_benchmark_sections = [add_benchmark_sections]

    # Add additional benchmark sections if provided
    if add_benchmark_sections:
        benchmark_sections.update(add_benchmark_sections)

    # Identify sections missing from the resume using regex
    missing = []
    for section in benchmark_sections:
        # Regex pattern to match section names (case-insensitive, handles concatenation)
        pattern = rf"\b{re.escape(section)}\b"
        if not re.search(pattern, clean_text, re.IGNORECASE):
            missing.append(section)

    return missing
