from moonleap.parser.term import is_it_term, words_to_terms


class Line:
    def __init__(self, text, words, terms, it_term, block=None):
        self.text = text
        self.words = words
        self.terms = terms
        self.it_term = it_term

    def find_terms_with_tag(self, tag, left_of=None):
        result = []
        for x in self.terms:
            if x.tag == tag:
                result.append(x)
            if left_of and x is left_of:
                break
        return result

    def __repr__(self):
        return "Line: " + ",".join(str(x) for x in self.terms)


def _preprocess_words(words):
    result = []
    for word in words:
        if word.startswith("("):
            result.append("(")
            word = word[1:]

        if word.endswith(")"):
            result.append(word[:-1])
            result.append(")")
        else:
            result.append(word)
    return result


def get_create_line():
    def create_line(text, it_term=None):
        terms = []
        words = _preprocess_words(text.split())
        next_it_term = None
        for term in words_to_terms(words):
            # check if :it must be replaced with it_term
            if is_it_term(term):
                if not it_term:
                    raise Exception(
                        f":It tag does not refer to a previous resource. Text:\n{text}"
                    )
                terms.append(it_term)
                next_it_term = it_term
            else:
                terms.append(term)
                if not next_it_term:
                    next_it_term = term

        return Line(text, words, terms, next_it_term)

    return create_line
