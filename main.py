# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import dataclasses
from dataclasses import dataclass
import warnings

from dumper import dump
from facades.translation import TranslationFacade
from facades.openai_facade import OpenAi
from facades.gsm8k_parser import Gsm8kParser, QA

from prompt_processor import PromptProcessor
from response_extractor import extract_result

processor = PromptProcessor()
translation_facade = TranslationFacade()
open_ai = OpenAi()
gsm8k_parser = Gsm8kParser()


@dataclass
class LangResults:
    raw: str
    fsl: int
    cot: int


@dataclass
class Results:
    english_raw: str
    english_fsl: int
    lang_results: dict[str, LangResults]


def run(english_prompt):
    res = {}
    for lang in ['he', 'ja', 'es']:
        translated = translation_facade.translate(english_prompt, lang)
        raw_result = open_ai.complete(translated)
        fsl_result = get_result(translated, False, lang)
        cot_result = get_result(translated, True, lang)
        res[lang] = LangResults(raw_result, fsl_result, cot_result)

    english_raw = open_ai.complete(english_prompt)
    english_fsl_result = get_result(english_prompt, False, 'en')

    return Results(
        english_raw,
        english_fsl_result,
        res,
    )


def get_result(prompt, cot, target_lang):
    translated_fsl = processor.process(prompt, cot, translation_facade.language_in_english(target_lang))
    translated_fsl_completion = open_ai.complete(translated_fsl)
    result_str = extract_result(translated_fsl_completion)
    try:
        return int(result_str.replace("$", "").replace("%", ""))
    except ValueError:
        warnings.warn(
            'Failed to extract number from result: TL {}, CoT {}, result: {}'.format(target_lang, cot, result_str)
        )
        return result_str


if __name__ == '__main__':
    q = 'There are 9 Fast and the Furious movies, Deepa has seen each one in the theatre three times. She has spent ' \
        '$216 seeing these movies. What is the average price she paid per ticket? '
    # result = run(q)
    # dump(QA(1234, q, 8), result)
    # print(result)
    for qa in gsm8k_parser.get_items()[11:12]:
        if qa.index in [11]:
            result = run(qa.question)
            dump(qa, result)
            print(result)
            print(qa.gold_answer)
