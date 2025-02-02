import re
import bisect
import pkg_resources

class AzStemmer:
    def __init__(self, keyboard="az"):
        if keyboard == "az":
            path = pkg_resources.resource_filename(__name__, 'azwords.txt')
        elif keyboard == "en":
            path = pkg_resources.resource_filename(__name__, 'enwords.txt')
        else:
            raise ValueError("Invalid keyboard. Choose 'az' or 'en'.")
        
        with open(path, "r", encoding='utf-8') as file:
            self.roots = sorted(line.strip() for line in file)
    
    def _find_root(self, word):
        for i in range(len(word), 0, -1):
            prefix = word[:i]
            idx = bisect.bisect_left(self.roots, prefix)
            if idx < len(self.roots) and self.roots[idx] == prefix:
                return prefix
        return word

    def stem(self, text):
        words = re.findall(r"\w+|[^\w\s]", text)
        result = []
        
        for i, word in enumerate(words):
            if not word.isalpha():
                if result:
                    result[-1] = result[-1].rstrip() + word
                else:
                    result.append(word)
            else:
                stemmed = self._find_root(word.lower())
                result.append(stemmed + ' ')
        
        text = " ".join(result).strip()
        return text.replace("  ", " ")