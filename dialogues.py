# coding: utf-8
import nltk

with open('dialogues.txt','r',encoding='utf-8') as dialogues_file:
    dialogues_text = dialogues_file.read()
    dialogues = dialogues_text.split('\n\n')


def clear_text(text):
    text = text.lower()
    text = ''.join(char for char in text if char in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя -')
    return text


dataset = []
questions = set()
for dialogue in dialogues:
    replicas = dialogue.split('\n')
    replicas = replicas[:2]

    if len(replicas) == 2:
        question, answer = replicas
        question = clear_text(question[2:])
        answer = answer[2:]

        if len(question) > 0 and question not in questions:
            questions.add(question)
            dataset.append([question, answer])

dataset_by_word = {}
for question, answer in dataset:
    words = question.split(' ')
    for word in words:
        if word not in dataset_by_word:
            dataset_by_word[word] = []
        dataset_by_word[word].append([question, answer])

dataset_by_word_filtered = {}
for word, word_dataset in dataset_by_word.items():
    word_dataset.sort(key=lambda pair: len(pair[0]))
    dataset_by_word_filtered[word] = word_dataset[:1000]

dataset_by_word_count = []
for word, word_dataset in dataset_by_word_filtered.items():
    dataset_by_word_count.append([word, len(word_dataset)])
dataset_by_word_count.sort(key=lambda pair: pair[1], reverse=True)
# print(dataset_by_word_count[:100])


def generate_answer(replica):
    replica = clear_text(replica)
    if not replica:
        return
    words = set(replica.split(' '))
    words_dataset = []

    for word in words:
        if word in dataset_by_word_filtered:
            word_dataset = dataset_by_word_filtered[word]
            words_dataset += word_dataset

    results = []

    for question, answer in dataset:
        if abs(len(question) - len(replica)) / len(question) < 0.2:
            distance = nltk.edit_distance(replica, question)
            if distance / len(question) < 0.2:
                results.append([question, answer, distance])

    question, answer, distance = min(results, key=lambda three: three[2])
    return answer

print(generate_answer('как тебя зовут?'))
