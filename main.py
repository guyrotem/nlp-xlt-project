# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import dataclasses
from dataclasses import dataclass
import warnings

from dumper import dump
from facades.translation import TranslationFacade
from facades.openai_facade import OpenAi
from facades.gsm8k_parser import Gsm8kParser

from prompt_processor import PromptProcessor
from response_extractor import extract_result

processor = PromptProcessor()
translation_facade = TranslationFacade()
open_ai = OpenAi()
gsm8k_parser = Gsm8kParser()


@dataclass
class Results:
    english_raw: str
    english_fsl: int
    hebrew_fsl: int
    hebrew_fsl_cot: int
    japanese_fsl: int
    japanese_fsl_cot: int


def run(english_prompt):
    translated_he = translation_facade.translate(english_prompt, 'he')
    translated_ja = translation_facade.translate(english_prompt, 'ja')

    he_fsl_result = get_result(translated_he, False, 'he')
    he_cot_result = get_result(translated_he, True, 'he')
    ja_fsl_result = get_result(translated_ja, False, 'ja')
    ja_cot_result = get_result(translated_ja, True, 'ja')

    english_raw = open_ai.complete(english_prompt)
    english_fsl_result = get_result(english_prompt, False, 'en')

    return Results(
        english_raw,
        english_fsl_result,
        he_fsl_result,
        he_cot_result,
        ja_fsl_result,
        ja_cot_result,
    )


def get_result(prompt, cot, target_lang):
    translated_fsl = processor.process(prompt, cot, translation_facade.language_in_english(target_lang))
    translated_fsl_completion = open_ai.complete(translated_fsl)
    result_str = extract_result(translated_fsl_completion)
    try:
        return int(result_str.replace("$", "").replace("%", ""))
    except ValueError:
        warnings.warn('Failed to extract number from result: TL {}, CoT {}, result: {}'.format(target_lang, cot, result_str))
        return result_str


@dataclass
class Gsm8kItem:
    question: str
    answer: str


if __name__ == '__main__':
    qa = gsm8k_parser.get_items()[55]
    # result = run(
    #     'There are 9 Fast and the Furious movies, Deepa has seen each one in the theatre three times. She has spent '
    #     '$216 seeing these movies. What is the average price she paid per ticket?',
    # )
    # print(result)
    result2 = run(qa.question)

    dump(qa, result2)
    print(result2)
    print(qa.gold_answer)
