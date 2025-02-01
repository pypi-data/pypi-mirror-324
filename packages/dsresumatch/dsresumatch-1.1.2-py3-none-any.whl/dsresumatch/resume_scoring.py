from dsresumatch.sections_check import missing_section
from dsresumatch.evaluate_keywords import evaluate_keywords, load_baseline_keywords
import warnings

def resume_score(cleaned_text, keywords=None, use_only_supplied_keywords=False, add_benchmark_sections=[], feedback=True):
    """
    This function uses the results of keyword and section analyses (from evaluate_keywords and sections_check) to give a 
    summary and a score that indicates of the quality of the resume text compared to the predefined baseline. The score is
    calculated using the formula:
    ((Total No. of Sections - Missing No. of Sections) + (Total No. of Keywords - Missing No. of Section)) / 
    (Total No. of Keywords + Total No. of Sections) * 100


    Users can provide their own keywords or combine them with a default set of predefined keywords.
    Users can also provide names of additional sections to be checked.

    Parameters
    ----------
    cleaned_text : str
        The cleaned text content of the resume.
    keywords : list of str, optional
        A list of keywords to compare against the resume content. If not provided, only the baseline 
        keywords will be used. If `use_only_supplied_keywords` is set to True without supplying keywords, 
        no keywords will be used, and the function will return an empty result.
    use_only_supplied_keywords : bool, optional
        A flag to determine whether to use only the supplied keywords or to combine them with a default 
        set of predefined keywords. Defaults to False.
    add_benchmark_sections : list of str or str, optional
        A list of additional section names (e.g., "Skills", "Education", "Work Experience", "Contact") or 
        a single section name as a string. Defaults to None. If a single string is provided, it will be 
        treated as a list with one element.
    feedback : bool, optional
        A flag to determine whether the summary should be included in the results (True), or just a line with
        the score should be given (False). The default is True.

    Returns
    -------
    str
        A string with a summary that gives the score of the given resume content. If feedback is True, lines
        explaining missing sections and keywords are also given.

    Examples
    --------
    >>> resume_text = '''
    ... Jane Doe
    ... Contact Information: janedoe@example.com
    ... Education: Master of Science in Data Science (2021)
    ... Work Experience: Data Scientist at Big Data Inc. (2022 - Present)
    ... Skills: Python, Machine Learning, SQL, Data Visualization
    ... '''
    >>> custom_keywords = ["Python", "Machine Learning", "SQL", "Big Data", "Cloud Computing"]
    >>> custom_sections = ["Certifications", "Projects"]
    >>> print(resume_score(
    ...     cleaned_text=resume_text,
    ...     keywords=custom_keywords,
    ...     use_only_supplied_keywords=False,
    ...     add_benchmark_sections=custom_sections
    ... ))

    This resume attained a score of 81.3.
    Feedback:
    - Missing Keywords: 'Big Data', 'Cloud Computing'
    - Missing Sections: 'Certifications', 'Projects'
    """

    # Data type check for feedback
    if not isinstance(feedback, bool):
        raise TypeError(f"Expected a boolean for feedback. feedback is a {type(feedback)}")

    # Data type check for cleaned_text
    if not isinstance(cleaned_text, str):
        raise TypeError(f"Expected a string for cleaned_text. cleaned_text is a {type(cleaned_text)}")

    # Data type check for keywords
    if keywords is not None:
        if not isinstance(keywords, list):
            raise TypeError(f"Expected a list for keywords. keywords is a {type(keywords)}")
    
    # Data type check for use_only_supplied_keywords
    if not isinstance(use_only_supplied_keywords, bool):
        raise TypeError(f"Expected a boolean for use_only_supplied_keywords. use_only_supplied_keywords is a {type(use_only_supplied_keywords)}")
    
    # Data type check for add_benchmark_sections
    if not isinstance(add_benchmark_sections, (str, list)):
        raise TypeError(f"Expected a string or list for add_benchmark_sections. add_benchmark_sections is a {type(add_benchmark_sections)}")
    
    # Issue warning if cleaned_text is blank
    if cleaned_text == "":
         warnings.warn("The provided resume text is an empty string.", UserWarning)

    # Issue warning if keywords is empty list
    if keywords == []:
         warnings.warn("The provided keywords list is empty.", UserWarning)

    # Issue warning and revert use_only_supplied_keywords if False and keywords is empty list
    if (keywords == [] or keywords is None) and use_only_supplied_keywords == True:
         warnings.warn("The provided keywords list is empty. Using default keywords.", UserWarning)
         use_only_supplied_keywords = False

    # Issue warning if add_benchmark_section is empty string
    if add_benchmark_sections == "":
         warnings.warn("The provided added sections text is an empty string.", UserWarning)

    
    # Getting missing keywords
    missing_keywords = evaluate_keywords(cleaned_text=cleaned_text,
                                         keywords=keywords,
                                         use_only_supplied_keywords=use_only_supplied_keywords)
    
    # Getting missing sections
    missing_sections = missing_section(clean_text=cleaned_text,
                                       add_benchmark_sections=add_benchmark_sections)
    
    # Evaluate score of resume. Weights for built in sections will be used in scoring.

    built_in_section_weight = 2
    sections = {"Skills", "Education", "Work Experience", "Contact"}
    baseline_keywords = load_baseline_keywords()

    # Getting lengths of missing sections and keywords and total sections and keywords
    sections_count = len(sections)
    additional_sections_count = len(add_benchmark_sections)
    baseline_keywords_count = len(baseline_keywords)
    missing_section_count = len(missing_sections)
    missing_keywords_count = len(missing_keywords)
    total_sections = sections_count + additional_sections_count

    # Adding weights for section names
    for section in missing_sections:
        if section in sections:
            missing_section_count += built_in_section_weight
        if missing_section_count > total_sections:
            missing_section_count = total_sections

    # Checking for only_supplied_keywords
    if use_only_supplied_keywords and keywords is not None:
        total_keywords = len(keywords)
    elif keywords is not None:
        total_keywords = baseline_keywords_count + len(keywords)
    else:
        total_keywords = baseline_keywords_count

    # Calculation of score
    score = ((total_sections-missing_section_count) + (total_keywords-missing_keywords_count)) / (total_keywords + total_sections) * 100

    # Creation of results string
    score_section = f"This resume attained a score of {score:.2f}."

    # If feedback is not needed, simply return the score only
    if not feedback:
        return score_section
    
    # If feedback is needed, construct the feedback string
    feedback_keywords = "- Missing Keywords: "
    feedback_keywords += ', '.join(missing_keywords) if missing_keywords else "None"
    feedback_sections = "- Missing Sections: "
    feedback_sections += ', '.join(missing_sections) if missing_sections else "None"

    # Concatenate all strings and return final string.
    result_string = f"{score_section} \n {feedback_keywords} \n {feedback_sections}"
    return result_string