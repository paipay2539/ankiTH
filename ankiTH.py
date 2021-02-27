from bs4 import BeautifulSoup
import requests


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


def text_convert(meaning_lst):
    text = ''
    for meaning in meaning_lst:
        # print(meaning[1])
        text = text + meaning[0] + ' : ' + meaning[1] + '<br>'
    return text


def main():
    vocab_lst = read_txt('vocab.txt')
    file2 = open('output.txt', "w", encoding="utf8")
    for vocab in vocab_lst:
        meaning_lst = search_vocab(vocab)
        if meaning_lst is not None:
            # print(search_vocab(vocab))
            meaning_text = text_convert(meaning_lst)
            file2.write(vocab + ';' + meaning_text + '\n')
    file2.close()

    # search_vocab('carrot')


if __name__ == '__main__':
    main()
