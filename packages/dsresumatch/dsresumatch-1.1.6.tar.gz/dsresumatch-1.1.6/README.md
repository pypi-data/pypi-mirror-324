# dsresumatch

[![Documentation Status](https://readthedocs.org/projects/dsresumatch/badge/?version=latest)](https://dsresumatch.readthedocs.io/en/latest/?badge=latest) [![codecov](https://codecov.io/github/UBC-MDS/dsresumatch/graph/badge.svg?token=iE9YGm9RLm)](https://codecov.io/github/UBC-MDS/dsresumatch) [![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dsresumatch) ![PyPI - Version](https://img.shields.io/pypi/v/dsresumatch)



<img src="https://raw.githubusercontent.com/UBC-MDS/dsresumatch/refs/heads/project_logo/docs/logo.png" width="150">

## Outline

`dsresumatch` is a Python library designed to do the analysis, evaluation, and scoring of resumes in PDF format. With tools to extract, clean, and analyze text, it allows users to identify missing, count word frequencies, evaluate keyword matches, and generate scores for resumes based on predefined criteria. This package is especially useful for recruiters, hiring managers, and job seekers aiming to optimize resumes for keyword-based Applicant Tracking Systems (ATS).

## **Features**

- **Text Processing**
  - `read_pdf(file_path)`: Extracts raw text from a PDF file.
  - `clean_text(raw_text)`: Cleans and preprocesses extracted text by removing punctuation, stop words, and converting to lowercase.
  - `count_words_in_pdf(file_path)`: Counts word frequencies in a PDF file.

- **Section Evaluation**
  - `missing_section(clean_text, add_benchmark_sections=None)`: Identifies sections missing from the resume compared to benchmark sections.

- **Keyword Analysis**
  - `evaluate_keywords(cleaned_text, keywords=None, use_only_supplied_keywords=False)`: Matches keywords against the resume text and evaluates the coverage.

- **Resume Scoring**
  - `resume_score(cleaned_text, keywords=None, use_only_supplied_keywords=False, add_benchmark_sections=[], feedback=True)`: Scores resumes based on keyword matching, benchmark sections, and provides detailed feedback on missing or extra keywords and sections.

## **How Does `dsresumatch` Fit into the Python Ecosystem?**

`dsresumatch` addresses a unique niche in the Python ecosystem by focusing on resume analysis and scoring, particularly for optimizing resumes for Applicant Tracking Systems (ATS) for Data Scientists. While there are general-purpose text analysis libraries such as:
- [NLTK](https://www.nltk.org/): For advanced natural language processing tasks.
- [spaCy](https://spacy.io/): For large-scale NLP and text processing.

There are no Python packages that consistently support resume matching (e.g., [resume-matcher](https://pypi.org/project/resume-matcher/), which was last updated in February 2024). However, there are some Python programs available, such as [resume-job-matcher](https://github.com/sliday/resume-job-matcher) and [Resume Compatibility](https://github.com/sumitprdrsh/Resume_Compatibility).

If you are looking for general PDF text extraction, libraries like [PyPDF2](https://github.com/py-pdf/pypdf) and [pdfplumber](https://github.com/jsvine/pdfplumber) might suit your needs. However, `dsresumatch` builds on this functionality to provide domain-specific tools tailored to resume evaluation.

## Installation

```bash
$ pip install dsresumatch
```

## Usage
The full documentation can be found [here](https://dsresumatch.readthedocs.io/en/latest/?badge=latest#).

Here is an example of using `dsresumatch` to extract text from pdf, count words from pdf:

```python

# Import required functions
from dsresumatch.pdf_cv_processing import read_pdf, count_words_in_pdf, clean_text
from dsresumatch.sections_check import missing_section
from dsresumatch.evaluate_keywords import evaluate_keywords
from dsresumatch.resume_scoring import resume_score
#additonal imports would be determined later

file_path = "~/Desktop/my_example_cv.pdf" # Specify the file path

raw_text = read_pdf(file_path) # Read text from the PDF
cleaned_text = clean_text(raw_text) # Clean and preprocess the text
word_counts = count_words_in_pdf(file_path) # Count words in the PDF

# (Optional) give keywords 
add_benchmark_sections = ["Work Experience", "Education", "Skills", "Projects", "Certifications"] 

# Identify missing sections
missing = missing_section(cleaned_text, benchmark_sections) 

keywords = ["Python", "Data Analysis", "Machine Learning"] # Evaluate keywords
keyword_evaluation = evaluate_keywords(cleaned_text, keywords)

resume_summary = resume_score(
    cleaned_text,
    keywords=keywords,
    add_benchmark_sections=benchmark_sections,
    feedback=True,
) # Score the resume

print("Word Counts:", word_counts)
print("Missing Sections:", missing)
print("Keyword Evaluation:", keyword_evaluation)
print("Resume Summary:", resume_summary)

```

A vignette, outlining the full functionality of the package can be found [here](https://dsresumatch.readthedocs.io/en/latest/example.html).


## Contributors

Nelli Hovhannisyan, Ashita Diwan, Timothy Singh, Jia Quan Lim

## Contributing

As a developer, are you innterested in contributing? Check out the contributing guidelines.

You may find the guided instructions in [CONTRIBUTING.md](https://github.com/UBC-MDS/dsresumatch/blob/main/CONTRIBUTING.md) Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`dsresumatch` was created by Nelli Hovhannisyan, Ashita Diwan, Timothy Singh, Jia Quan Lim. It is licensed under the terms of the MIT license.

## Credits

`dsresumatch` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
