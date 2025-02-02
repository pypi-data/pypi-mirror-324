# AzStemmer 📚
**AzStemmer** is a basic stemming library for Azerbaijani sentences. It is not highly effective but offers a simple way to stem Azerbaijani words, especially for cases where you need to reduce words to their root form. The stemmer uses a dictionary of root words and performs stemming based on that list.

## Installation ⬇️
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install azstemmer.

```bash
pip install azstemmer
```

## Usage ⚙️

```python
from azstemmer import AzStemmer

# Initialize stemmer with the appropriate keyboard type
# Use 'az' for Azerbaijani text or 'en' if the text is typed using an English keyboard
stemmer = AzStemmer(keyboard="az") 

# Stem your string
stemmed_string = stemmer.stem("your_string")
```

## Features 🧩
- Azerbaijani Stemming: Reduces Azerbaijani words to their root forms.
- English Keyboard Support: You can choose 'az' or 'en' for proper stemming based on the keyboard used for typing.
- Simple and Lightweight: A straightforward way to perform stemming without any advanced NLP models.

## Known Issues or Limitations ❗
- As the stemming is based on a dictionary of words, special names (e.g., proper nouns) cannot be stemmed.
- Some words may not be stemmed correctly due to the limitations of the dictionary-based approach.

## Contributing 🤝
Contributions are welcome, but as the project is fairly simple, there might not be significant need for collaboration. But in any case, feel free to contact me for collaboration or if you think improvements can be made.

## License 📜
[MIT](https://choosealicense.com/licenses/mit/)

## Contact 📧
Gmail: naginagiyev03@gmail.com.

Linkedin: https://www.linkedin.com/in/naginagiyev/