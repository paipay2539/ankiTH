from bs4 import BeautifulSoup
import requests

import os

from gtts import gTTS
from playsound import playsound

import sys
sys.dont_write_bytecode = True
import rainbow_divider_lib as rdl


def progress(count, total, suffix=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '#' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', suffix))
    sys.stdout.flush()  # As suggested by Rom Ruben
    if percents == 100:
        print("")


def remove_repeated_element(test_list):
    res = []
    for i in test_list:
        if i not in res:
            res.append(i)
    return res


def search_vocab_en(word, exactly_mode=False,
                    src="NECTEC Lexitron Dictionary EN-TH"):
    url = requests.get("https://dict.longdo.com/mobile.php?search="+word)
    soup = BeautifulSoup(url.content, "html.parser")
    target_src_exist = soup.find("b", string=src)
    if target_src_exist is not None:
        data = soup.find("b", string=src).next_sibling
        # print(data)
        '''
        print(data.prettify())
        print(data.tr.td)
        print(data.tr.td.contents)
        print(data.tr.td.text)

        print(data.tr.children)
        print(list(data.tr.children))
        '''

        result_lst = []
        for tr in data:
            tr_lst = []
            for td in tr:
                tr_lst.append(td.text)
            if exactly_mode is True:
                if tr_lst[0] == word:
                    result_lst.append(tr_lst)
            else:
                result_lst.append(tr_lst)

        for idx, text in enumerate(result_lst):
            if text[1].find(', Syn.') != -1:
                result_lst[idx][1] = text[1][:text[1].find(', Syn.')]
            # print(text)
        return result_lst
    else:
        return None

    # soup = BeautifulSoup(data)
    # table = soup.find("table", attrs={"class":"result-table"})


def search_vocab_jp(word, exactly_mode=False):
    '''search_mode = 'Start', 'End', 'Between', 'Exact' '''
    if exactly_mode is True:
        search_mode = 'Exact'
    else:
        search_mode = 'Between'
    url = requests.get("https://j-doradic.com/?searchPosition=search"
                       + search_mode + "&q=" + word)
    soup = BeautifulSoup(url.content, "html.parser")
    target_exist = soup.find("table", class_="table table-striped")
    # print(data.prettify())
    if target_exist is not None:
        data = soup.find("table", class_="table table-striped").tbody
        descendant_lst = []
        for d in data.descendants:
            if d.name == "a" and d.text != "thumb_up" and len(d.attrs) == 1:
                descendant_lst.append(d.text.replace('\n', ' ')
                                      .replace('\r', ''))
                # print(d.text.replace('\n', ' ').replace('\r', ''))

        if len(descendant_lst) % 3 == 0:
            result_lst = []
            for i in range(len(descendant_lst)//3):
                kanji = descendant_lst[i*3]
                hiragana = descendant_lst[i*3+1]
                thai_meaning = descendant_lst[i*3+2]

                if kanji.count('•') > 0:
                    hiragana_copy = hiragana
                    for i in range(kanji.count('•')):
                        hiragana = hiragana + '•' + hiragana_copy
                if kanji.count('・') > 0:
                    hiragana_copy = hiragana
                    for i in range(kanji.count('・')):
                        hiragana = hiragana + '・' + hiragana_copy

                meaning_lst = ["<ruby>"+kanji+"<rt>"
                               + hiragana+"</rt></ruby>", thai_meaning]
                '''
                meaning_lst = [descendant_lst[i*3],
                               descendant_lst[i*3+1],
                               descendant_lst[i*3+2]]
                '''
                if exactly_mode is True:
                    if descendant_lst[i*3] == word:
                        result_lst.append(meaning_lst)
                else:
                    result_lst.append(meaning_lst)

            return result_lst
        else:
            print("error")
            return None
    else:
        return None


def read_txt(file_name):
    f = open(file_name, "r", encoding="utf8")
    vocab_lst = f.read().strip('\n').split('\n')
    return vocab_lst


def find_text_between(text, start, end):
    return text[text.find(start)+len(start):text.rfind(end)]


def text_convert(meaning_lst, vocab):
    text = ''
    exactly_text = ''
    rgb_lst = rdl.divider2str(len(meaning_lst))
    for idx, meaning in enumerate(meaning_lst):
        # print(meaning[1])
        # found_vocab = '<p style="color:rgb(255, 99, 71);">'+meaning[0]+'</p>'
        if '<ruby>' in meaning[0]:  # is firigana
            is_exactly_vocab = bool(find_text_between(
                                    meaning[0], '<ruby>', '<rt>') == vocab)
        else:
            is_exactly_vocab = bool(meaning[0] == vocab)
        if is_exactly_vocab:
            found_vocab = '<span style="color:rgb(102, 255, 153); font-size:30px">'+meaning[0]+'</span>'
            found_meaning = '<span style="color:rgb(102, 255, 153); font-size:30px">'+meaning[1]+'</span>'
            exactly_text = '<span style="color:rgb(233, 253, 226); font-size:50px">'+meaning[0]+'</span>'
        else:
            found_vocab = '<span style="color:rgb'+ rgb_lst[idx] +'; font-size:20px">'+meaning[0]+'</span>'
            found_meaning = '<span style="color:rgb'+ rgb_lst[idx] +'; font-size:20px">'+meaning[1]+'</span>'
        new_text = found_vocab + ' : ' + found_meaning

        if is_exactly_vocab:
            text = new_text + '<br>' + text
        else:
            text = text + new_text + '<br>'

    return text, exactly_text


def text2sound(vocab, sound_number):
    tts = gTTS(text=vocab, lang='ja')
    tts.save('data/output/sound/#' + sound_number + '.mp3')


def ankiTH(input_text, gen_sound=False, exactly_mode=False):
    vocab_lst = read_txt('data/input/'+input_text+'.txt')
    output = open('data/output/'+input_text+'_output.txt', "w", encoding="utf8")
    fail_output = open('data/output/'+input_text+'_fail_output.txt', "w", encoding="utf8")
    for vocab_cnt, vocab in enumerate(vocab_lst):
        if 'jp' in input_text:
            meaning_lst = search_vocab_jp(vocab, exactly_mode)
            if exactly_mode is False:
                meaning_lst_exact = search_vocab_jp(vocab, True)
                if meaning_lst is not None and meaning_lst_exact is not None:
                    meaning_lst = meaning_lst_exact + meaning_lst
                    meaning_lst = remove_repeated_element(meaning_lst)
            furigana_offset = "</br>"
        elif 'en' in input_text:
            meaning_lst = search_vocab_en(vocab, exactly_mode)
            furigana_offset = ""
        else:
            break
        if meaning_lst is not None:
            # print(search_vocab_en(vocab))
            meaning_text, furigana = text_convert(meaning_lst, vocab)
            if gen_sound is True:
                sound_number = input_text + '_' + str(vocab_cnt)
                sound_call_name = '[sound:#' + sound_number + '.mp3]'
                text2sound(vocab, sound_number)
            else:
                sound_call_name = ''
            vocab = '<span style="color:rgb(233, 253, 226); font-size:50px">' \
                    + "<ruby>" + vocab + "<rt>" + furigana_offset \
                    + "</rt></ruby>" + '</span>'
            if furigana == '':
                furigana = vocab
            output.write(vocab + '@' + meaning_text + sound_call_name
                         + '@' + furigana + '\n')
        else:
            fail_output.write(vocab + '\n')
        progress(vocab_cnt, len(vocab_lst)-1)
    output.close()
    # search_vocab_en('carrot')


def main():

    do_list = [
             #  'N3_100_jp.txt',
             #  'N3_500_jp.txt',
             #  'N3_full_jp.txt',
               'vocab_en.txt',
               'vocab_jp.txt'
               ]
    directory = 'data/input/'
    for filename in os.listdir(directory):
        if filename.endswith(".txt") and filename in do_list:
            ankiTH(os.path.splitext(filename)[0],
                   gen_sound=True, exactly_mode=False)

    # ankiTH('N3_full_jp', gen_sound=True, exactly_mode=False)
    # ankiTH('N3_100_jp', gen_sound=False, exactly_mode=False)
    # ankiTH('vocab_jp', gen_sound=True, exactly_mode=False)
    # ankiTH('vocab_en', gen_sound=True, exactly_mode=False)


if __name__ == '__main__':
    main()
