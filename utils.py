import copy
import string
import random


def generate_word_dataset(label_list, num_docs: int = 1):
    with open('wikigold.conll.txt', 'r', encoding='utf-8') as fp:
        doc_count = 0
        words = []
        labels = []
        for line in fp.readlines():
            if 'DOCSTART' in line:
                doc_count += 1
                if doc_count > num_docs:
                    break
                continue
            elif line == '\n':
                continue

            word, label = line.strip().split(' ')

            if word in string.punctuation:
                continue

            label_int = 1 if label in label_list else 0
            words.append(word)
            if label_int:
                labels.append(word)
            else:
                labels.append("")
    return words, labels


def generate_sentence_dataset(label_list, num_docs: int = 1):
    with open('wikigold.conll.txt', 'r', encoding='utf-8') as fp:
        doc = []
        named_words = []
        sentence = []
        sentence_names = []
        doc_count = 0
        prev_label_int = 0
        for line in fp.readlines():
            if 'DOCSTART' in line:
                doc_count += 1
                doc.append("".join(sentence))
                named_words.append(" ".join(sentence_names))

                sentence = []
                sentence_names = []
                continue
            if doc_count > num_docs:
                break

            if line == '\n':
                continue

            word, label = line.strip().split(' ')
            label_int = 1 if label in label_list else 0

            # we have a NE
            if label_int == 1:
                # unique NE, add entry to master lists
                if prev_label_int == 0:
                    doc.append("".join(sentence))
                    named_words.append(" ".join(sentence_names))

                    # reset current lists
                    sentence = [sentence[-1]] if sentence else []  # keep last word for context
                    sentence_names = []

                sentence_names.append(word)

            if word in string.punctuation and word not in '()':
                sentence.append(word)
            else:
                sentence.append(" " + word)

            prev_label_int = label_int
    return doc, named_words


def generate_sentence_dataset_v2(label_list, num_docs: int = 1, random_context=False):
    with open('wikigold.conll.txt', 'r', encoding='utf-8') as fp:
        running_document = []
        last_named_entity_index = None
        doc = []
        named_words = []
        sentence = []
        sentence_names = []
        doc_count = 0
        prev_label_int = 0
        for line in fp.readlines():
            if 'DOCSTART' in line:
                last_named_entity_index = None
                doc_count += 1
                doc.append("".join(sentence))
                named_words.append(" ".join(sentence_names))

                sentence = []
                sentence_names = []
                continue
            if doc_count > num_docs:
                break
            if line == '\n':
                continue

            word, label = line.strip().split(' ')
            label_int = 1 if label in label_list else 0

            # we have a NE
            if label_int == 1:
                # unique NE, add entry to master lists
                if prev_label_int == 0:
                    doc.append("".join(sentence))
                    named_words.append(" ".join(sentence_names))

                    # reset current lists
                    context = 1
                    if last_named_entity_index:
                        if random_context:
                            # keep random amount of last words for context,
                            # up to but not including the last named entity
                            maximum_context = len(running_document) - last_named_entity_index
                            context = random.choice(range(1, maximum_context)) if maximum_context > 1 else 1
                        else:
                            # keep maximal amount of context, up to but not including the last NER
                            context = len(running_document) - last_named_entity_index
                    old_sentence = copy.deepcopy(sentence)
                    sentence = []
                    sentence.extend(old_sentence[-context:]) if old_sentence else []
                    sentence_names = []

                sentence_names.append(word)

            if word in string.punctuation and word not in '()':
                sentence.append(word)
                running_document.append(word)
            else:
                sentence.append(" " + word)
                running_document.append(" "+word)

            prev_label_int = label_int
            if label_int == 1:
                last_named_entity_index = len(running_document)

    return doc, named_words


if __name__ == '__main__':
    labelList = ['I-PER', 'I-ORG', 'I-LOC', 'I-MISC']
    targets, labels = generate_sentence_dataset_v2(['I-PER', 'I-ORG', 'I-LOC', 'I-MISC'], 10, random_context=True)

