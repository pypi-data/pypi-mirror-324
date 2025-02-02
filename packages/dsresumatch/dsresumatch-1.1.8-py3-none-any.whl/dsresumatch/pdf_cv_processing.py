import PyPDF2 # type: ignore
import string
from collections import Counter
from nltk.corpus import stopwords # type: ignore
import nltk # type: ignore

# Ensure NLTK stopwords are downloaded
nltk.download('stopwords')

def read_pdf(file_path):
    """
    Extract text content from a PDF file and return it as a single consolidated string.

    Parameters
    ----------
    file_path : str
        Path to the PDF file.

    Returns
    -------
    str
        PDF file contents as text.

    Examples
    --------
    >>> read_pdf("cv.pdf")
    'Work Experience\nSoftware Developer at XYZ Corp.\nEducation\nBachelor of Science in Computer Science\n'
    """
    if not isinstance(file_path, str):
        raise TypeError("file_path must be a string representing the file path")
    if not file_path.lower().endswith(".pdf"):
        raise ValueError("file_path must point to a PDF file")
    
    text_content = []
    try:
        with open(file_path, 'rb') as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            for page in reader.pages:
                text_content.append(page.extract_text())
        return "".join(text_content).replace("\n", "")
    except FileNotFoundError as e:
        raise FileNotFoundError(f"The file {file_path} does not exist.") from e
    except Exception as e:
        raise ValueError(f"Error reading the PDF file: {e}")
    

def clean_text(raw_text):
    """
    Convert raw_text to lowercase, remove punctuation, and filter out common English stop words 
    to retain only meaningful words in the string.

    Parameters
    ----------
    raw_text : str
        Text to clean.

    Returns
    -------
    str
        Cleaned text.

    Examples
    --------
    >>> clean_text("Work Experience: Software Developer at XYZ Corp!")
    'work experience software developer xyz corp'
    """

    if not isinstance(raw_text, str):
        raise TypeError("raw_text must be a string")
    
    # Convert to lowercase
    raw_text = raw_text.lower()
    # Remove punctuation
    translator = str.maketrans('', '', string.punctuation)
    text_no_punctuation = raw_text.translate(translator)
    # Split into words and remove stop words
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in text_no_punctuation.split() if word not in stop_words]
    return " ".join(filtered_words)


def count_words_in_pdf(file_path):
    """
    Count the frequency of words in a PDF file.

    This function converts all words to lowercase, removing punctuation, and excluding common English 
    stop words to ensure meaningful word counts. 

    Parameters
    ----------
    file_path : str
        Path to the PDF file.

    Returns
    -------
    collections.Counter
        Dictionary-like object with the frequency of each remaining word where keys are words and 
        values are counts.

    Examples
    --------
    >>> count_words_in_pdf("cv.pdf")
    Counter({'work': 1, 'experience': 1, 'software': 1, 'developer': 1, 'at': 1, 'xyz': 1, 
    'corp': 1, 'education': 1, 'bachelor': 1, 'of': 1, 'science': 1, 'in': 1, 'computer': 1})
    """
    if not isinstance(file_path, str):
        raise TypeError("file_path must be a string representing the file path")
    if not file_path.lower().endswith(".pdf"):
        raise ValueError("file_path must point to a PDF file")
    
    pdf_text = read_pdf(file_path)
    cleaned_text = clean_text(pdf_text)
    word_list = cleaned_text.split()
    return Counter(word_list)
