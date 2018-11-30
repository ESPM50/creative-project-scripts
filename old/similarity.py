import re
import random

NUMERIC_RE = re.compile(r'^[a-z]?\d+[a-z]?$')
CAMELCASE_RE = re.compile(r'[A-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))')

with open("corncob_lowercase.txt") as word_file:
    english_words = set(word.strip().lower() for word in word_file)

english_words.difference_update(('ben', 'smith', 'mike', 'mikes', 'anna'))
english_words.update(('espm', '50ac', 'protiab', 'muralist', 'muralists'))


filenames = ['Acuna - Michelle - ESPMFinalpaper.pdf', 'Acuna, Michelle - espm_final_model.pdf', 'Ajayi, Iyioluwa.docx',
  'Anderson, Julia - Nature and Civilization Collide .pdf', 'Babikian, Karnie - IMG_6094.jpg', 'Babikian, Karnie - IMG_6095 (1).jpg',
  'Campos, Josh - Ceiling to the Sand.m4a', 'Carabuena, Sara Kate - reflective essay.pdf', 'Chen, Fei Yu - 1.1.MP3',
  'Chen, Fei Yu -1Nature.MP3', 'Chen, Fei Yu -2Fire.MP3', 'Chen, Fei Yu -3.1.MP3', 'Chen, Fei Yu -3Gold.MP3',
  'Chen, Fei Yu -4Tempest.MP3', 'Emily Wagner - ducks in wetland.jpg', 'Emily Wagner - grizzly sketch.jpg',
  'Emily Wagner - O4 - Final Project Reflection.docx', 'Emily Wagner - redwood and chinook salmon sketch.JPG',
  'ESPM-50FS4ChenFeiYuS17.pdf', 'Fann, Amy and Brenton Chu - Short Story Final Version.docx',
  'Hwang, Anna - Reflective Essay and Final Draft.docx', 'Johnson, Marisa - ESPM 50 FP O4A-1.pdf', 'Jow, Owen - issei_200dpi.mov',
  'Kim, Heidi-1.pdf', 'Kim, Heidi.png', 'KimYoona-SureshSahana-TangSarahReflectiveEssayandBibliography-2.pdf', 'Le, Sabrina & .pdf',
  'Mallit, Ben - ReflectiveEssayModelMinority.pdf', 'Mallit, Ben – Images .docx', 'Meteo, Crystal -IMG_3482.JPG', 'Meteo, Crystal -IMG_3485.JPG',
  "Montanez, Martha - Reflective Essay - S'17.docx", 'Naik,Nishali - Reflection-107 .pdf', 'Naik,Nishali -.pptx',
  "Nussbaum, Jasper - Reflective Essay - S'17.pdf", 'NUssbaum, Jaspewr & Anna Schiff - Comic Book.pdf', 'O4A-Zhan,Shuya-1.docx',
  'Owen Jow - Issei Link.pdf', 'Wang, Kebvin & Alex Wu - Final_Project_Image.pdf', 'Wu, LIsa - Hey, CAreful with that WATER.jpg',
  'Wu, Lisa - Relfective Essay.pdf']

def group_filenames(filenames, threshold=0.5):
    groups = []
    for filename in filenames:
        best_group = None
        best_sim = threshold
        for group in groups:
            # def sim_map(group_filename):
            #     _, sim = filename_similarity(group_filename, filename)
            #     return sim
            # sim = max(map(sim_map, group))

            rep = random.choice(group)
            _, sim = filename_similarity(rep, filename)

            if sim > best_sim:
                best_sim = sim
                best_group = group
        if best_group:
            best_group.append(filename)
        else:
            groups.append([ filename ])
    return groups

def remove_extension(S):
    f = S.rfind('.')
    if f >= 0:
        S = S[:f]
    return S.strip()

IGNORED_WORDS = [ 'espm', 'final', 'paper', 'essay', 'reflective', 'reflection',
    'bibliography', 'and', 'draft', 'summary', 'for', 'instructors', 'students',
    'gentrification', '50ac', 'project', 'image', 'description', 'submission',
    'protiab', 'idea' ]
IGNORED_WORDS.sort(key=len, reverse=True)
def preprocess_filename(S):
    S = remove_extension(S)
    # words = re.split(r'[-_,\s:&\']+', S)
    words = re.split(r'[^a-zA-Z0-9]+', S)
    words = filter(lambda word: word.lower() not in english_words, words)
    words = filter(lambda word: not NUMERIC_RE.match(word), words)
    words = sum(map(lambda word: CAMELCASE_RE.findall(word) or [ word ], words), [])
    words = filter(lambda word: word.lower() not in english_words, words)
    # for ignored_word in IGNORED_WORDS:
    #     S = S.replace(ignored_word, '')
    # S = re.sub(r'[_\b]\d+', '', S)
    # S = re.sub(r'[-_,\s:&]+', '', S)
    return ''.join(words).lower()

def filename_similarity(S, T):
    S = preprocess_filename(S)
    T = preprocess_filename(T)
    return substr(S, T)

def substr(S, T):
    L = [ 0 for _ in range(len(S) + len(T)) ]
    tot = 0
    best_len = 0
    best_end = 0
    for i in range(len(S)):
        for j in range(len(T)):
            k = len(S) + j - i
            if S[i] == T[j]:
                L[k] += 1
                if L[k] >= 3:
                   tot += L[k] ** 2
                if L[k] > best_len:
                    best_len = L[k]
                    best_end = i
            else:
                L[k] = 0
    return S[best_end - best_len + 1:best_end + 1], tot / (0 + min(len(S), len(T)) ** 2)

if __name__ == '__main__':
    # for row in group_filenames(filenames):
    #     print(repr(row))
    #     print()

    a = 'nakagawaalexander_5356719_73133731_ESPM 50 - GS - Water Crisis Policy and Data Analysis'
    b = 'kwakjemma_late_5360790_73181830_ESPM 50 – FP 05 - The Muralists - S\'18"'
    print(preprocess_filename(a))
    print(preprocess_filename(b))
    print(filename_similarity(a, b))

# L = lcs(*filenames[:2])
# print('\n'.join(map(lambda row: ' '.join(map(str, row)), L)))

def test_all_to_all():
    # filenames = ['Emily Wagner - ducks in wetland.jpg', 'Emily Wagner - grizzly sketch.jpg', 'Emily Wagner - O4 - Final Project Reflection.docx', 'Emily Wagner - redwood and chinook salmon sketch.JPG', 'Naik,Nishali - Reflection-107 .pdf', 'Naik,Nishali -.pptx']
    for f1 in filenames:
        row = []
        for f2 in filenames:
            _, score = filename_similarity(f1, f2)
            # if score > 0.2:
            #     print('score', score, ss)
            row.append(str(int(100 * score)))
        print(' '.join(row))

    groups = group_filenames(filenames)
    for group in groups:
        print('    ', group)

# test_all_to_all()
