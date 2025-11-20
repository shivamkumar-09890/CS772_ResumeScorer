class ResumeContentExtractor:
    """
    Extract joined text and bullet content from parsed resume sections.

    This class:
    - Takes the parsed resume dictionary (sections → text/bullets/etc)
    - Skips irrelevant sections (skill, hobbies, extracurricular etc)
    - Outputs flattened dictionary: text_1, bullets_1, text_2, ...
    """

    # Normalized section names that should be skipped
    SKIP_SECTIONS = [
        "career objective",
        "objective",
        "summary",
        "professional summary",
        "profile summary",
        "personal profile",
        "overview",
        "about me",
        "declaration",
        "personal details",
        "references",
        "hobbies",
        "hobby",
        "interests",
        "interest",
        "personal interests",
        "extra-curricular activities",
        "extra curricular",
        "extracurricular",
        "extra-curricular",
        "co-curricular activities",
        "strengths",
        "weaknesses",
        "languages known",
        "academic achievements",
        "scholastic achievements",
        "coursework",
        "relevant coursework",
        "subjects undertaken",
        "workshops attended",
        "seminars attended",
        "certifications",
        "contact information",
        "social links",
        "key strengths",
        "key highlights",
        "soft skills",
        "responsibilities",
        "accomplishments",
        "skill",
        "skills",
        "technical skill",
        "technical skills",
        "hobbies",
        "extra curricular",
        "extracurricular",
        "extra-curricular",
        "interest",
        "interests",
    ]

    def __init__(self, resume_dict: dict):
        self.resume_dict = resume_dict

    @staticmethod
    def normalize_section(name: str) -> str:
        """Normalize section names to compare reliably."""
        return name.strip().upper().replace(":", "")

    def should_skip(self, section_name: str) -> bool:
        """Check if section is unwanted."""
        normalized = self.normalize_section(section_name)

        # fuzzy match (contains 'SKILL', 'HOBBY', 'EXTRA')
        if any(word in normalized for word in self.SKIP_SECTIONS):
            return True

        return False

    def extract(self) -> dict:
        """
        Produces:
        {
            "text_1": "joined text ...",
            "bullets_1": "joined bullets ...",
            "text_2": "...",
            "bullets_2": "..."
        }
        """

        output = {}
        text_counter = 1
        bullets_counter = 1

        for section, content in self.resume_dict.items():

            if self.should_skip(section):
                continue  # skip SKILL, HOBBIES, EXTRA CURRICULAR etc.

            # ---- Extract TEXT ----
            texts = content.get("text", [])
            if texts:
                joined_text = " ".join(t.strip() for t in texts if t.strip())
                if joined_text:
                    key = f"text_{text_counter}"
                    output[key] = joined_text
                    text_counter += 1

            # ---- Extract BULLETS ----
            bullets = content.get("bullets", [])
            if bullets:
                joined_bullets = " ".join(b.strip() for b in bullets if b.strip())
                if joined_bullets:
                    key = f"bullets_{bullets_counter}"
                    output[key] = joined_bullets
                    bullets_counter += 1

        return output
