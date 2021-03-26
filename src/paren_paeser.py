#!/usr/bin/env python3


def parse_paren(src: str):
    buf = [[], []]
    depth = 0

    for s in src:
        if s in {'(', '（'}:
            depth += 1
            if depth == 1:
                buf[1].append([])
            elif 1 < depth:
                buf[min(1, depth)][-1].append(s)
        elif s in {')', '）'}:
            if 1 < depth:
                buf[min(1, depth)][-1].append(s)
            depth -= 1
        elif depth == 0:
            buf[0].append(s)
        else:
            buf[min(1, depth)][-1].append(s)

    return ''.join(buf[0]).strip(), tuple(''.join(li).strip() for li in buf[1])


if __name__ == '__main__':
    s1, s2 = parse_paren('Conference on Human Factors in Computing Systems (CHI 2020)')
    print(s1, s2)

    for s in s2:
        print('word: ' + s)
