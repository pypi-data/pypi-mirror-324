import json
import warnings
from pathlib import Path

# load in baseline keywords
def load_baseline_keywords():
    """Load baseline keywords from the JSON file.

    This function reads a JSON file containing baseline keywords organized by categories.
    It flattens the categories into a single list of keywords, converting them to lowercase
    for uniformity. This list can be used for evaluating resumes against a standard set of
    keywords relevant to data science. 

    Returns
    -------
    list of str
        A list of baseline keywords in lowercase, extracted from the JSON file. 

    Raises
    ------
    FileNotFoundError
        If the JSON file containing the baseline keywords cannot be found.
    json.JSONDecodeError
        If the JSON file is not properly formatted.
    """
    
    data_path = Path(__file__).parent / "data" / "baseline_keywords.json"
    with open(data_path, "r") as f:
        keywords_dict = json.load(f)
    
    # flatten all categories into a single list
    return [keyword.lower() for category in keywords_dict.values() for keyword in category]

def evaluate_keywords(cleaned_text, keywords=None, use_only_supplied_keywords=False):
    """
    Evaluate the quality of a resume by comparing its content against a set of predefined 
    or user-supplied keywords.

    This function assesses whether the resume contains relevant keywords that match the criteria 
    for a "good data science resume." Users can provide their own keywords or combine them with a 
    default set of predefined keywords.

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

    Returns
    -------
    list of str
        A list of keywords (from either the baseline or provided keywords) that do not appear 
        in the `cleaned_text`.

    Examples
    --------
    >>> evaluate_keywords("software development project management agile methodologies", ["software", "agile", "teamwork"])
    ['teamwork']

    >>> evaluate_keywords("data analysis machine learning statistical modeling", use_only_supplied_keywords=False)
    ['teamwork', 'communication']
    """
    # input validation: verify text and keywords are strings
    if not isinstance(cleaned_text, str):
        raise TypeError("cleaned_text must be a string")
    
    if keywords is not None and not all(isinstance(k, str) for k in keywords):
        raise TypeError("All keywords must be strings")
    
    # Check for empty text and warn user
    if not cleaned_text.strip():
        warnings.warn("The provided resume text is an empty string. Returning all baseline keywords as missing.", UserWarning)
    
    # Warn if user wants to use only supplied keywords but provides none
    if use_only_supplied_keywords and (keywords is None or len(keywords) == 0):
        warnings.warn("No keywords provided while use_only_supplied_keywords=True. Returning empty list.", UserWarning)
    
    # convert text to lowercase for case-insensitive matching
    cleaned_text = cleaned_text.lower()
    
    # initialize the set of keywords to check
    # this will avoid duplicates as well
    keywords_to_check = set()
    
    # handle the supplied keywords
    if keywords is not None:
        keywords_to_check.update(k.lower() for k in keywords)
    
    # add baseline keywords if needed
    if not use_only_supplied_keywords:
        keywords_to_check.update(load_baseline_keywords())
    
    # if no keywords to check (edge case: use_only_supplied_keywords=True but no keywords provided)
    if not keywords_to_check:
        return []
    
    # lastly find missing keywords
    missing_keywords = []
    for keyword in keywords_to_check:
        if keyword not in cleaned_text:
            missing_keywords.append(keyword)
    
    return missing_keywords
