from bs4 import BeautifulSoup
import requests

import sys
sys.dont_write_bytecode = True
import rainbow_divider_lib as rdl


def search_vocab(word, exactly_mode=False,
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


def read_txt(file_name):
    f = open(file_name, "r", encoding="utf8")
    vocab_lst = f.read().strip('\n').split('\n')
    return vocab_lst


def text_convert(meaning_lst, vocab):
    text = ''
    rgb_lst = rdl.divider2str(len(meaning_lst))
    for idx, meaning in enumerate(meaning_lst):
        # print(meaning[1])
        # found_vocab = '<p style="color:rgb(255, 99, 71);">'+meaning[0]+'</p>'
        if meaning[0] == vocab:
            found_vocab = '<span style="color:rgb(102, 255, 153); font-size:30px">'+meaning[0]+'</span>'
            found_meaning = '<span style="color:rgb(102, 255, 153); font-size:30px">'+meaning[1]+'</span>'
        else:
            found_vocab = '<span style="color:rgb'+ rgb_lst[idx] +'; font-size:15px">'+meaning[0]+'</span>'
            found_meaning = '<span style="color:rgb'+ rgb_lst[idx] +'; font-size:15px">'+meaning[1]+'</span>'
        new_text = found_vocab + ' : ' + found_meaning
        text = text + new_text + '<br>'
    return text


def main():
    vocab_lst = read_txt('vocab.txt')
    output = open('output.txt', "w", encoding="utf8")
    fail_output = open('fail_output.txt', "w", encoding="utf8")
    for vocab in vocab_lst:
        meaning_lst = search_vocab(vocab)
        if meaning_lst is not None:
            # print(search_vocab(vocab))
            meaning_text = text_convert(meaning_lst, vocab)
            vocab = '<span style="color:rgb(233, 253, 226); font-size:60px">'+vocab+'</span>'
            output.write(vocab + '@' + meaning_text + '\n')
        else:
            fail_output.write(vocab + '\n')

    output.close()

    # search_vocab('carrot')


if __name__ == '__main__':
    main()
