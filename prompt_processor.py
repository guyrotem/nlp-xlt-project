class PromptProcessor:
    def __init__(self):
        with open('data/FSL.txt') as fsl_file:
            self._FSL = fsl_file.read()

        with open('data/CoT.txt') as cot_file:
            self._CoT = cot_file.read()

    def process(self, text, cot, language):
        if cot:
            return self._FSL + self._get_cot(language) + "Q: " + text + "\n"
        else:
            return self._FSL + "Q: " + text + "\n"

    def _get_cot(self, language):
        return self._CoT.replace("{{ lang }}", language)
