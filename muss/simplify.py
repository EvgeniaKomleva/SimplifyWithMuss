import argparse
from deep_translator import GoogleTranslator
import time
import random

from muss.simplify import ALLOWED_MODEL_NAMES, simplify_sentences
from muss.utils.helpers import read_lines

f_en = open("en_input.txt", "w+")
f_out = open("output.txt", "w+")


def safe_translate(translator, text):
    text = translator.translate(text)
    time.sleep(0.5 + random.random())
    return text


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Simplify a file line by line.')
    parser.add_argument('--filepath',
                        type=str, default="ru_input.txt",
                        help='File containing the source sentences, one sentence per line.')
    parser.add_argument(
        '--model-name',
        type=str,
        default=ALLOWED_MODEL_NAMES[0],
        choices=ALLOWED_MODEL_NAMES,
        help=f'Model name to generate from. Models selected with the highest validation SARI score.',
    )
    args = parser.parse_args()
    f = open(args.filepath, "r")
    content = f.readlines()
    source_sentences = []
    for sent in content:
        transated = safe_translate(GoogleTranslator(source='ru', target='en'), sent)
        source_sentences.append(transated)
    print("translation ready!")

    # source_sentences = read_lines("en_input.txt")
    pred_sentences = simplify_sentences(source_sentences, model_name=args.model_name)
    for c, s in zip(source_sentences, pred_sentences):
        answer = safe_translate(GoogleTranslator(source='en', target='ru'), s)
        print(answer)
        f_out.write(answer)
        f_out.write('\n')