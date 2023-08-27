class PromptProcessor:
    def __init__(self):
        with open('data/FSL.txt') as fsl_file:
            self._FSL = fsl_file.read()

        with open('data/CoT-Huang-et-al.txt') as cot_file:
            self._CoT = cot_file.read()

    def process(self, question, cot, language):
        if cot:
            return self._FSL + self._get_cot(language, question) + "\n"
        else:
            return self._FSL + "Q: " + question + "\n"

    def _get_cot(self, language, question):
        return self._CoT.replace("{{ lang }}", language).replace("{{ question }}", question)
