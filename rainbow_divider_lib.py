import pylab as plt


def rgba2rgb(rgba, background=(255, 255, 255)):
    rgb = ["", "", ""]
    r, g, b, a = rgba[0], rgba[1], rgba[2], rgba[3]
    R, G, B = background
    rgb[0] = r * a + (1.0 - a) * R
    rgb[1] = g * a + (1.0 - a) * G
    rgb[2] = b * a + (1.0 - a) * B
    return rgb


def rainbow_fill(divider, cmap=plt.get_cmap("jet")):
    rainbow_lst = []
    offset = 120
    for n in range(divider):
        color_rgba = cmap(n/divider)
        rgb = rgba2rgb(color_rgba)
        for idx in range(len(rgb)):
            rgb[idx] = int(rgb[idx]*255)
        '''
        if (rgb[0] + offset <= 255) or \
                (rgb[1] + offset <= 255) or \
                (rgb[2] + offset <= 255):
            rgb[0] = rgb[0] + offset
            rgb[1] = rgb[1] + offset
            rgb[2] = rgb[2] + offset
        '''
        if rgb[0] + offset < 255:
            rgb[0] = rgb[0] + offset
        else:
            rgb[0] = 255
        if rgb[1] + offset < 255:
            rgb[1] = rgb[1] + offset
        else:
            rgb[1] = 255
        if rgb[2] + offset < 255:
            rgb[2] = rgb[2] + offset
        else:
            rgb[2] = 255

        rainbow_lst.append(rgb)
    return rainbow_lst


def rgb2str(rgb):
    output_str = []
    for i in rgb:
        output_str.append('('+str(i[0])+', '+str(i[1])+', '+str(i[2])+')')
    return output_str


def divider2str(divider, start_color='cold'):
    rgb_lst = rgb2str(rainbow_fill(divider))
    if start_color == 'hot':
        rgb_lst.reverse()
    return rgb_lst


def main():
    print(divider2str(100))


if __name__ == '__main__':
    main()
