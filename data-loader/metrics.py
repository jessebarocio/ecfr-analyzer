class Metrics:
    def __init__(self, xml):
        self.xml = xml

    def get_word_count(self):
        text_content = "".join(self.xml.itertext())
        return len(text_content.split())

    # TODO: More metrics!
