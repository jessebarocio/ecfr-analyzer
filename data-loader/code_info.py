import math
import re


class CodeInfo:
    def __init__(self, code_reference, xml):
        self.code_reference = code_reference
        self.xml = xml
        self.text_content = "".join(self.xml.itertext())

    def get_reference_text(self):
        reference_text = (
            f"{self.code_reference['title_id']} CFR {self.code_reference['chapter']}"
        )
        if self.code_reference["subtitle"] is not None:
            reference_text += f" Subtitle {self.code_reference['subtitle']}"
        if self.code_reference["chapter"] is not None:
            reference_text += f" Chapter {self.code_reference['chapter']}"
        if self.code_reference["subchapter"] is not None:
            reference_text += f" Subchapter {self.code_reference['subchapter']}"
        if self.code_reference["part"] is not None:
            reference_text += f" Part {self.code_reference['part']}"
        if self.code_reference["subpart"] is not None:
            reference_text += f" Subpart {self.code_reference['subpart']}"
        if self.code_reference["section"] is not None:
            reference_text += f" Section {self.code_reference['section']}"
        return reference_text

    def get_name(self):
        return self.xml.xpath(".//HEAD[1]")[0].text.strip()

    def get_link(self):
        link = f"https://www.ecfr.gov/current/title-{self.code_reference['title_id']}"
        if self.code_reference["subtitle"] is not None:
            link += f"/subtitle-{self.code_reference['subtitle']}"
        if self.code_reference["chapter"] is not None:
            link += f"/chapter-{self.code_reference['chapter']}"
        if self.code_reference["subchapter"] is not None:
            link += f"/subchapter-{self.code_reference['subchapter']}"
        if self.code_reference["part"] is not None:
            link += f"/part-{self.code_reference['part']}"
        return link

    def calculate_burden_score(self):
        text = self.text_content.lower()

        word_count = len(self.text_content.split())
        requirements = len(
            re.findall(r"\b(shall|must|required|will|mandatory)\b", text)
        )
        conditionals = len(
            re.findall(r"\b(if|unless|provided that|subject to)\b", text)
        )
        exceptions = len(
            re.findall(
                r"\b(except|exception|excluding|other than|exemption|waiver)\b", text
            )
        )
        deadlines = len(
            re.findall(r"\b(within|deadline|not later than|prior to)\b", text)
        )
        paperwork = len(re.findall(r"\b(form|report|submit|file|document)\b", text))
        penalties = len(
            re.findall(r"\b(penalty|violation|fine|enforcement|prohibited)\b", text)
        )

        density_score = (
            (requirements * 2.0 + 
             conditionals * 1.5 + 
             exceptions * 1.75 + 
             deadlines * 1.0 + 
             paperwork * 1.5 + 
             penalties * 1.0) / word_count
        ) * 1000

        # Size factor is a multiplier that accounts for the size of the section of code. 
        # Longer, more complex sections have a higher regulatory burden.
        size_factor = math.log10(word_count) * 10

        # The final burden score is a combination of the density score and the size factor.
        burden_score = (density_score * 0.4) + (size_factor * 0.6)

        return {
            "burden_score": burden_score,
            "density_score": density_score,
            "word_count": word_count,
            "breakdown": {
                "requirements": requirements,
                "conditionals": conditionals,
                "exceptions": exceptions,
                "deadlines": deadlines,
                "paperwork": paperwork,
                "penalties": penalties,
            },
        }
