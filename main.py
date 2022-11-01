from string import ascii_lowercase
import pandas as pd
import streamlit as st
import enchant
import random
import math
import numpy as np

st.set_page_config(layout="wide")
st.title("Caesar-Verschlüsselung")
caesar_mode = st.radio("Mode", ['phonetisches Alphabet (26 Buchstaben)', 'Unicode'])
st.subheader("Encode")
encode_text_input = st.text_input("Enter text to encode:")

if caesar_mode == 'phonetisches Alphabet (26 Buchstaben)':
    encode_index = st.slider("Select index to encode:", 0, len(ascii_lowercase) - 1)

elif caesar_mode == 'Unicode':
    encode_index = st.slider("Select index to encode:", 0, 1114111)

endoce_button = st.button("Encode")

if endoce_button:
    encode_text = ''
    if caesar_mode == 'phonetisches Alphabet (26 Buchstaben)':
        encode_text_cleaned = encode_text_input.replace(
            'ä', 'ae').replace('Ä', 'Ae').replace('ö', 'oe').replace('Ö', 'Oe').replace(
            'ü', 'ue').replace('Ü', 'Ue').replace('ß', 'ss')
        for char in encode_text_cleaned:
            if char.isalpha():
                if char.isupper():
                    encode_text += ascii_lowercase[(ascii_lowercase.index(char.lower()) + encode_index) % len(ascii_lowercase)].upper()
                elif char.islower():
                    encode_text += ascii_lowercase[(ascii_lowercase.index(char) + encode_index) % len(ascii_lowercase)]
            else:
                encode_text += char

    elif caesar_mode == 'Unicode':
        for char in encode_text_input:
            try:
                encode_text += chr((ord(char) + encode_index) % 1114111)
            except:
                encode_text += char

    st.success(encode_text)

st.markdown('---')

st.subheader("Decode")
decode_text_input = st.text_input("Enter text to decode:")

decode_index = st.slider('Index', 0, len(ascii_lowercase) - 1)
decode_button = st.button("Decode")
dictsolve = st.button("Solve by searching in dictionary")
charsolve = st.button("Solve by looking at the letter distribution")
language = st.selectbox(
    'language',
    enchant.list_languages(),
)

d = enchant.Dict(language)

letter_distribution = {
    'a': 6.51,
    'b': 1.89,
    'c': 3.06,
    'd': 5.08,
    'e': 17.4,
    'f': 1.66,
    'g': 3.01,
    'h': 4.76,
    'i': 7.55,
    'j': 0.27,
    'k': 1.21,
    'l': 3.44,
    'm': 2.53,
    'n': 9.78,
    'o': 2.51,
    'p': 0.79,
    'q': 0.02,
    'r': 7,
    's': 7.27,
    't': 6.15,
    'u': 4.35,
    'v': 0.67,
    'w': 1.89,
    'x': 0.03,
    'y': 0.04,
    'z': 1.13
}

if decode_button:
    decode_text = ''
    for char in decode_text_input:
        if char.isalpha():
            if char.isupper():
                decode_text += ascii_lowercase[(ascii_lowercase.index(char.lower()) - decode_index) % len(ascii_lowercase)].upper()
            elif char.islower():
                decode_text += ascii_lowercase[(ascii_lowercase.index(char) - decode_index) % len(ascii_lowercase)]
        else:
            decode_text += char
    st.success(decode_text)

if dictsolve:
    solveMap = {}
    for i in range(len(ascii_lowercase) - 1):
        solve_text = ''
        for char in decode_text_input:
            if char.isalpha():
                if char.isupper():
                    solve_text += ascii_lowercase[(ascii_lowercase.index(char.lower()) - i) % len(ascii_lowercase)].upper()
                if char.islower():
                    solve_text += ascii_lowercase[(ascii_lowercase.index(char) - i) % len(ascii_lowercase)]
            else:
                solve_text += char

        solve_words = solve_text.encode("ascii", "ignore").decode().split(' ')

        for word in solve_words:
            if d.check(word):
                if i not in solveMap.keys():
                    solveMap[i] = {
                        'idx': 1,
                    }
                else:
                    solveMap[i]['idx'] += 1

        if i in solveMap.keys():
            solveMap[i]['str'] = solve_text

    if len(solveMap) > 0:
        solveMapKeys = sorted(
            solveMap.keys(),
            key=lambda x: solveMap[x]['idx'],
            reverse=True
        )
        for key in solveMapKeys[:5]:
            st.text(
                f'{solveMap[key]["str"]} at index {key}')
    else:
        st.text("No solution found")

if charsolve:
    solveMap = {}
    for i in range(len(ascii_lowercase) - 1):
        solve_text = ''
        for char in decode_text_input:
            if char.isalpha():
                if char.isupper():
                    solve_text += ascii_lowercase[(ascii_lowercase.index(char.lower()) - i) % len(ascii_lowercase)].upper()
                if char.islower():
                    solve_text += ascii_lowercase[(ascii_lowercase.index(char) - i) % len(ascii_lowercase)]
            else:
                solve_text += char
        
        solve_text_ascii = solve_text.encode("ascii", "ignore").decode().replace(' ', '')
        solve_text_distribution = {k: 0 for k in ascii_lowercase}
        for l in solve_text_ascii:
            if l.lower() in solve_text_distribution.keys():
                solve_text_distribution[l.lower()] += 1
        solve_text_distribution = {k: v / len(solve_text_ascii) * 100 for k, v in solve_text_distribution.items()}
        solveMap[i] = {'str': solve_text, 'idx': sum([abs(letter_distribution[k] - solve_text_distribution[k]) for k in letter_distribution.keys()])}
    
    solveMapKeys = sorted(
        solveMap.keys(),
        key=lambda x: solveMap[x]['idx'],
        reverse=False
    )
    for key in solveMapKeys[:5]:
        st.text(
            f'{solveMap[key]["str"]} at index {key}')


st.title("Vigenere Cipher")
st.subheader("Encode")
encode_text_input_vi = st.text_input("Enter text to encode:", key="encode_text_input_vi")
encode_text_cleaned_vi = encode_text_input_vi.replace(
    'ä', 'ae').replace('Ä', 'Ae').replace('ö', 'oe').replace('Ö', 'Oe').replace(
    'ü', 'ue').replace('Ü', 'Ue').replace('ß', 'ss')
encode_word_vi = st.text_input("Enter word to use for encoding:")
endoce_button_vi = st.button("Encode", key="encode_button_vi")

if endoce_button_vi:
    encode_text_vi = ''
    for i, char in enumerate(encode_text_cleaned_vi):
        encode_index_vi = ascii_lowercase.index(encode_word_vi[i % len(encode_word_vi)]) + 1

        if char.isalpha():
            if char.isupper():
                encode_text_vi += ascii_lowercase[(ascii_lowercase.index(char.lower()) + encode_index_vi) % len(ascii_lowercase)].upper()
            elif char.islower():
                encode_text_vi += ascii_lowercase[(ascii_lowercase.index(char) + encode_index_vi) % len(ascii_lowercase)]
        else:
            encode_text_vi += char
    st.success(encode_text_vi)

st.markdown('---')

st.subheader("Decode")
decode_text_input_vi = st.text_input("Enter text to decode:", key="decode_text_input_vi")
decode_word_vi = st.text_input("Enter word to use for decoding:")
decode_button_vi = st.button("Decode", key="decode_button_vi")

if decode_button_vi:
    decode_text_vi = ''
    for i, char in enumerate(decode_text_input_vi):
        decode_index_vi = ascii_lowercase.index(decode_word_vi[i % len(decode_word_vi)]) + 1

        if char.isalpha():
            if char.isupper():
                decode_text_vi += ascii_lowercase[(ascii_lowercase.index(char.lower()) - decode_index_vi) % len(ascii_lowercase)].upper()
            elif char.islower():
                decode_text_vi += ascii_lowercase[(ascii_lowercase.index(char) - decode_index_vi) % len(ascii_lowercase)]
        else:
            decode_text_vi += char
    st.success(decode_text_vi)

def gcd(a, b):
    """
    Performs the Euclidean algorithm and returns the gcd of a and b
    """
    if (b == 0):
        return a
    else:
        return gcd(b, a % b)

def xgcd(a, b):
    """
    Performs the extended Euclidean algorithm
    Returns the gcd, coefficient of a, and coefficient of b
    """
    x, old_x = 0, 1
    y, old_y = 1, 0

    while (b != 0):
        quotient = a // b
        a, b = b, a - quotient * b
        old_x, x = x, old_x - quotient * x
        old_y, y = y, old_y - quotient * y

    return a, old_x, old_y

def generate_prime(prime, start, end):
    while True:
        n = random.randint(start, end)

        if n==0 or n==1 or n==4 or n==6 or n==8 or n==9:
            continue
        if n==2 or n==3 or n==5 or n==7 and n!=prime:
            return n

        s = 0
        d = n-1
        while d%2==0:
            d>>=1
            s+=1
        assert(2**s * d == n-1)
    
        def trial_composite(a):
            if pow(a, d, n) == 1:
                return False
            for i in range(s):
                if pow(a, 2**i * d, n) == n-1:
                    return False
            return True  
    
        for i in range(8):
            no_prime = False
            a = random.randrange(2, n)
            if trial_composite(a):
                no_prime = True
                break

        if no_prime:
            continue

        if n!=prime:
            return n

def generate_e(phi):
    while True:
        e = random.randint(2, phi - 1)
        if (math.gcd(e, phi) == 1):
            return e

st.title("RSA")
gen_rsa = st.button("Generate new keys", key="generate_new_keys")

if 'rsa_p' not in st.session_state or gen_rsa:
    st.session_state['rsa_p'] = generate_prime(0, 10**300, 10**301)
    st.session_state['rsa_q'] = generate_prime(st.session_state['rsa_p'], 10**300, 10**301)
    st.session_state['rsa_n'] = st.session_state['rsa_p'] * st.session_state['rsa_q']
    st.session_state['rsa_phi'] = (st.session_state['rsa_p'] - 1) * (st.session_state['rsa_q'] - 1)
    st.session_state['rsa_e'] = generate_e(st.session_state['rsa_phi'])
    st.session_state['rsa_d'] = pow(st.session_state['rsa_e'], -1, st.session_state['rsa_phi']) 

    # rsa_a, rsa_x, rsa_y = xgcd(st.session_state['rsa_e'], st.session_state['rsa_phi'])
    # if (rsa_x < 0):
    #     st.session_state['rsa_d'] = rsa_x + st.session_state['rsa_phi']
    # else:
    #     st.session_state['rsa_d'] = rsa_x

st.text(
f"""
p: {st.session_state['rsa_p']}
q: {st.session_state['rsa_q']}
n: {st.session_state['rsa_n']}
phi: {st.session_state['rsa_phi']}
e: {st.session_state['rsa_e']}
d: {st.session_state['rsa_d']}
""")

st.subheader("Encode")
encode_message_rsa = st.text_input("Enter message to encode:", key="encode_message_rsa")
encode_button_rsa = st.button("Encode", key="encode_button_rsa")

if encode_button_rsa:
    encode_message_ascii_rsa = [ord(char) for char in encode_message_rsa]
    encode_message_ascii_rsa = [pow(c, st.session_state['rsa_e'], st.session_state['rsa_n']) for c in encode_message_ascii_rsa]
    st.success(" ".join([str(c) for c in encode_message_ascii_rsa]))

st.subheader("Decode")
decode_message_rsa = st.text_input("Enter message to decode:", key="decode_message_rsa")
decode_button_rsa = st.button("Decode", key="decode_button_rsa")

if decode_button_rsa:
    decode_message_ascii_rsa = [int(c) for c in decode_message_rsa.split(" ")]
    decode_message_ascii_rsa = [pow(c, st.session_state['rsa_d'], st.session_state['rsa_n']) for c in decode_message_ascii_rsa]
    st.success("".join([chr(c) for c in decode_message_ascii_rsa]))

st.title("Mathe Aufgaben")
with st.expander("1. Modulo"):
    st.write(r"""
#### Aufgabe 1:
a) 27 mod 4 = 3 | print(27 % 4) $\rightarrow$ 4 * 6 + 3 = 27\
b) 26 mod 5 = 1 | print(26 % 5) $\rightarrow$ 5 * 5 + 1 = 26\
c) 18 mod 3 = 0 | print(18 % 3) $\rightarrow$ 3 * 6 + 0 = 18\
d) 18 mod 7 = 4 | print(18 % 7) $\rightarrow$ 7 * 2 + 4 = 18\
e) 21 mod 9 = 3 | print(21 % 9) $\rightarrow$ 9 * 2 + 3 = 21\
f) 37 mod 10 = 7 | print(37 % 10) $\rightarrow$ 10 * 3 + 7 = 37\
g) 100037 mod 10 = 7 | print(100037 % 10) $\rightarrow$ 10 * 10003 + 7 = 100037\
h) 107 mod 4 = 3 | print(107 % 4) $\rightarrow$ 4 * 26 + 3 = 107\
i) 1 mod 2 = 1 | print(1 % 2) $\rightarrow$ 2 * 0 + 1 = 1\
j) 3 mod 2 = 1 | print(3 % 2) $\rightarrow$ 2 * 1 + 1 = 3

#### Aufgabe 2:
a) sei k eine gerade Zahl. Berechne k mod 2\
2 % 2 = 0 $\rightarrow$ 2 * 1 + 0 = 2\
4 % 2 = 0 $\rightarrow$ 2 * 2 + 0 = 4
###### Eine gerade Zahl ist per Definition durch 2 teilbar. Daher ist der Rest 0.

b) sei k eine ungerade Zahl. Berechne k mod 2.\
1 % 2 = 1 $\rightarrow$ 2 * 0 + 1 = 1\
3 % 2 = 1 $\rightarrow$ 2 * 1 + 1 = 3
###### Eine ungerade Zahl ist per Definition nicht durch 2 teilbar. Daher ist der Rest 1.

#### Aufgabe 3:
a) Vergleiche  25 mod 4  und  (20 mod 4 + 5 mod 4) mod 4\
print(25 % 4, (20 % 4 + 5 % 4) % 4) $\rightarrow$ 1, 1 | identisch\

b) Vergleiche  25 mod 4  und  (19 mod 4 + 6 mod 4) mod 4\
print(25 % 4, (19 % 4 + 6 % 4) % 4) $\rightarrow$ 1, 1 | identisch\

c) Vergleiche  26 mod 4  und  (2 mod 4·13 mod 4) mod 4\
print(26 % 4, (2 % 4 * 13 % 4) % 4) $\rightarrow$ 2, 2 | identisch\

d) Vergleiche  7**3 mod 4  und  (7 mod 4)**3 mod 4\
print(7 ** 3 % 4, (7 % 4) ** 3 % 4) $\rightarrow$ 3, 3 | identisch\

#### Regeln
(a + b) mod m = (a mod m + b mod m) mod m\
print((25 + 12) % 4, (25 % 4 + 12 % 4) % 4) $\rightarrow$ 1, 1

(a - b) mod m = (a mod m - b mod m) mod m\
print((25 - 12) % 4, (25 % 4 - 12 % 4) % 4) $\rightarrow$ 1, 1

(a * b) mod m = (a mod m * b mod m) mod m\
print((25 * 12) % 4, (25 % 4 * 12 % 4) % 4) $\rightarrow$ 0, 0

(a ** b) mod m = (a mod m) ** b mod m\
print((25 ** 12) % 4, (25 % 4) ** 12 % 4) $\rightarrow$ 1, 1

#### Aufgabe 4:
a) Es sei n irgendeine natürliche Zahl, die mit den Ziffern ...34 endet. Berechne n mod 4\
34 mod 4 = 2 | print(34 % 4) $\rightarrow$ 4 * 8 + 2 = 34\
12134 mod 4 = 2 | print(12134 % 4) $\rightarrow$ 4 * 3033 + 2 = 12134

b) Wie kann man leicht überprüfen, ob eine Zahl durch 4 teilbar ist?\
Die Zahl n ist durch 4 teilbar, wenn die letzte Ziffer 0, 4, 8 oder 2 ist.\
Der Modulo Rest muss 0 sein. $\rightarrow$ n mod 4 != 0 | z.B. print(24 % 4)

#### Aufgabe 5:
Es ist 10 Uhr am Vormittag (Mittwoch) und du hast in 50 Stunden einen Terminbeim Zahnarzt und in 70 Stunden einen Computerkurs. Wann finden die Terminestatt?\
Zahnarzt: 10 Uhr + 50 Stunden = 60 Uhr $\rightarrow$ 60 Uhr mod 24 = 12 Uhr\
Computerkurs: 10 Uhr + 70 Stunden = 80 Uhr $\rightarrow$ 80 Uhr mod 24 = 8 Uhr\
Der Zahnarzttermin ist am Freitag um 12 Uhr und der Computerkurs am Samstag um 8 Uhr.
        """
    )

with st.expander("2. Restklassen"):
    st.write(r"""
Restklassen
[a]$_{m}$ = {b $\in$ $\mathbf{Z}$ | $\exists$K $\in$ $\mathbf{Z}$ : b = k * m + a} = {b | b $\equiv$ a mod m}\
Die Restklasse einer ganzen Zahl a modulo einer Zahl m ist die Menge all der Zahlen, die bei Division durch denselben (positiven)

#### Aufgabe 1:
a) Versuche die obige Tabelle in Worte zu fassen.\
Die Tabelle zeigt die Restklassen von m = 6.\
Die Spalten stellen den Rest a dar.\
Für die einzelnen Felder gilt: b = k * m + a

b) Fertige eine entsprechende Tabelle für m = 5 an.
    """)

    st.dataframe(
        pd.DataFrame(
            data={
                '[0]5': ['5 * k', ':', '-10', '-5', '0', '5', '10', ':'],
                '[1]5': ['5 * k + 1', ':', '-9', '-4', '1', '6', '11', ':'],
                '[2]5': ['5 * k + 2', ':', '-8', '-3', '2', '7', '12', ':'],
                '[3]5': ['5 * k + 3', ':', '-7', '-2', '3', '8', '13', ':'],
                '[4]5': ['5 * k + 4', ':', '-6', '-1', '4', '9', '14', ':'],

            }
        )
    )

    st.write(r"""
c) Bestimme [0]$_{3}$, [1]$_{3}$ und [1]$_{4}$.\
[0]$_{3}$ = {b aus Z | es gibt K aus Z mit b = k * 3 + 0} = [:, -6, -3, 0, 3, 6, :]\
[1]$_{3}$ = {b aus Z | es gibt K aus Z mit b = k * 3 + 1} = [:, -5, -2, 1, 4, 7, :]\
[1]$_{4}$ = {b aus Z | es gibt K aus Z mit b = k * 4 + 1} = [:, -7, -3, 1, 5, 9, :]

d) Gib drei verschiedene Repräsentanten der Restklassen [3]$_{7}$ und [2]$_{8}$ an.\
[3]$_{7}$ = [:, -11, 3, 10, :]\
[2]$_{8}$ = [:, -10, 2, 10, :]

e) Kennst Du Anwendungen von Restklassen im täglichen Leben?\
Mögliche Anwendungen wären die Uhrzeit, Wochentage und Kalender.

###### 1. Zeige, dass für alle Repräsentanten a aus [4]$_{7}$ und b aus [5]$_{7}$ gilt: a+b aus [2]$_{7}$. Benutze dafür, dass sich a und b schreiben lassen als a=7·k1+4 und b=7·k2+5 mit ganzen Zahlen k1 und k2 und ermittle, welchen Rest a+b bei Division durch 7 hat.\
[4]$_{7}$ = [:, -3, 4, 11, :]\
[5]$_{7}$ = [:, -2, 5, 12, :]\
Hierfür gilt: (4 + 5) % 7 = 9 % 7 = 2

[2]$_{7}$ = [:, -5, 2, 9, :]\
Für a gilt: a = 7 * k1 + 4\
Für b gilt: b = 7 * k2 + 5\
Für a + b gilt: a + b = (7 * k1 + 4) + (7 * k2 + 5) = 7 * (k1 + k2) + 9 = 7 * k3 + (9 % 7) = 7 * k3 + 2 mit k3 = k1 + k2
Somit entsteht die Restklasse [2]$_{7}$.

###### 2. Zeige, dass für alle Repräsentanten a aus [4]$_{7}$ und b aus [5]$_{7}$ gilt: a·b aus [6]$_{7}$. Benutze dafür, dass sich a und b schreiben lassen als a=7·k1+4 und b=7·k2+5 mit ganzen Zahlen k1 und k2 und ermittle, welchen Rest a·b bei Division durch 7 hat.
[4]$_{7}$ = [:, -3, 4, 11, :]\
[5]$_{7}$ = [:, -2, 5, 12, :]\
Hierfür gilt: (4 * 5) % 7 = 20 % 7 = 6

[6]$_{7}$ = [:, -1, 6, 13, :]\
Für a gilt: a = 7 * k1 + 4\
Für b gilt: b = 7 * k2 + 5\
Für a * b gilt: \
a * b = (7 * k1 + 4) * (7 * k2 + 5) 
= 49 * k1 * k2 + 35 * k1 + 28 * k2 + 20\
= 49 * k3 + 35 * k1 + 28 * k2 + 20 = 7 * (7 * k3 + 5 * k1 + 4 * k2) + 20 | mit k3 = k1 * k2\
= 7 * k4 + (20 % 7) = 7 * k4 + 6 mit k4 = 7 * k3 + 5 * k1 + 4 * k2
Somit entsteht die Restklasse [6]$_{7}$.

3. Leicht darstellen kann man Addition und Multiplikation von Restklassen mit Tabellen. Wenn aus dem Zusammenhang klar ist, welche Restklassen man betrachtet, kann man die Symbole [ ]m auch weglassen.

a) Zeige, dass für die Restklassen modulo 3 folgende Additions- und Multiplikationstabelle gilt:\
Der Rest n bei der Addition entsteht aus (3 * k1 + n1) + (3 * k2 + n2) | Für n muss somit gelten: n = (n1 + n2) % 3
Der Rest n bei der Multiplikation entsteht aus (3 * k1 + n1) * (3 * k2 + n2) | Für n muss somit gelten: n = (n1 * n2) % 3

Additionstabelle:
    """)

    additionTable3a = np.zeros((3, 3))
    for row in range(3):
        for col in range(3):
            additionTable3a[row][col] = (row + col) % 3

    st.dataframe(
        pd.DataFrame(
            additionTable3a
        )
    )

    st.write(r"""
Multiplikationstabelle:
    """)

    multiplikationsTable3a = np.zeros((3, 3))
    for row in range(3):
        for col in range(3):
            multiplikationsTable3a[row][col] = (row * col) % 3
    
    st.dataframe(
        pd.DataFrame(
            multiplikationsTable3a
        )
    )

    st.write(r"""
b) Ermittle Additions- und Multiplikationstabelle für die Restklassen modulo 6.

Additionstabelle:
    """)

    additionTable6b = np.zeros((6, 6))
    for row in range(6):
        for col in range(6):
            additionTable6b[row][col] = (row + col) % 6
        
    st.dataframe(
        pd.DataFrame(
            additionTable6b
        )
    )

    st.write(r"""
Multiplikationstabelle:
    """)

    multiplikationsTable6b = np.zeros((6, 6))
    for row in range(6):
        for col in range(6):
            multiplikationsTable6b[row][col] = (row * col) % 6

    st.dataframe(
        pd.DataFrame(
            multiplikationsTable6b
        )
    )

with st.expander("3. modulares Potenzieren"):
    st.write(r"""
#### Regeln
(a $\cdot$ b) mod m = (a mod m $\cdot$ b mod m) mod m\
(a$^{b}$) mod m = (a mod m)$^{b}$ mod m

#### Aufgabe 1:
Für 7$^{4}$ mod 12 gilt die Form (a$^{b}$) mod m\
Diese wurde in (a$^{\frac{b}{2}}$ $\cdot$ a$^{\frac{b}{2}}$) mod m umgewandelt.\
Nach der ersten Regel lässt sich dies nun in (a$^{\frac{b}{2}}$ mod m $\cdot$ a$^{\frac{b}{2}}$ mod m) mod m umwandeln\
Somit: (49 mod 12 $\cdot$ 49 mod 12) mod 12 = (1 $\cdot$ 1) % 12 = 1

Für 82$^{17}$ mod 20 gilt die Form (a$^{b}$) mod m\
Im nächsten Schritt wurde nach der zweiten oberen Regel das a=82 durch a=2 gekürzt, da sie sich in der selben Restklasse befinden. | 82 mod 20 = 2 $\rightarrow%$ 20 $\cdot$ 4 + 2 | 2 mod 20 = 2\
Nun wird der Term wieder in ein Produkt aufgeteilt, wodurch sich die erste obere Regel anwenden lässt.
Jetzt kann auch 16 durch -4 ersetzt werden, da sie sich in der selben Restklasse befinden. | 16 mod 20 = 16 $\rightarrow%$ 20 $\cdot$ 0 + 16 | -4 mod 20 = 16\
Somit: (-4)$^{2}$ $\cdot$ 2 mod 20 = (16 $\cdot$ 2) mod 20 = 32 mod 20 = 12

#### Aufgabe 2:
a) 8 ** 9 mod 7 = 1 ** 9 mod 7 = 1

b) 6 ** 9 mod 7 = (-1) ** 9 mod 7 = 6

c) 54 ** 16 mod 55 = (-1) ** 16 mod 55 = 1

d) 3 ** 333 mod 26 = (3 ** 3) ** 100 mod 26\
    = (3 ** 3 % 26) ** 100 mod 26\
    = 1 ** 100 mod 26 = 1

e) 2 ** 268 mod 17 = (2 ** 4) ** 67 mod 17\
    = (2 ** 4 % 17) ** 67 mod 17\
    = (-1) ** 67 mod 17\
    = (-1) % 17 = 16

f) 2 ** 269 mod 17 = (2 ** 268 * 2) mod 17\
    = (2 ** 268 mod 17 * 2 mod 17) mod 17\
    = (16 * 2) mod 17 = 15

g) 2 ** 270 mod 19 = (2 ** 9) ** 30 mod 19\
    = (2 ** 9 % 19) ** 30 mod 19\
    = (-1) ** 30 mod 19 = 1

h) 2 ** 271 mod 19 = (2 ** 270 * 2) mod 19\
    = (2 ** 270 mod 19 * 2 mod 19) mod 19\
    = (1 * 2) mod 19 = 2

i) 3 ** 333 mod 15 = (3 * 3 ** 332) mod 15\
    = (3 * (3 ** 4) ** 83) mod 15\
    = (3 * 81 ** 83) mod 15\
    = (3 * 6 ** 83) mod 15\
    = (3 mod 15 * 6 ** 83 mod 15) mod 15\
    = 3 * 6 mod 15 = 3 | Weil 6 ** k mod 15 = 6
    """)

with st.expander("4. sym-asym Verschlüsselung"):
    st.write(r"""
#### Aufgabe 1: Was ist der Nachteil an der symmetrischen Verschlüsselung?
Bei der symmetrischen Verschlüsselung wird der selbe Schlüssel zum Verschlüsseln und Entschlüsseln verwendet, womit er vor Dritten vollständig geheim gehalten werden muss.
Somit entsteht das Problem, dass der Schlüssel schon im Vorhinein sicher zwischen dem Sender und Empfänger ausgetauscht worden sein muss, bevor es überhaupt zu einer Kommunikation kommen kann.

#### Aufgabe 2: Fasse die Schritte der asymmetrischen Verschlüsselung in Worte!
1. Der Sender (A) verschlüsselt eine Nachricht mit seinem Schlüssel und schickt diese ohne den eigenen Schlüssel an den Empfänger (B).
2. Der Empfänger (B) verschlüsselt die Nachricht ebenfalls mit seinem Schlüssel und schickt diese ohne den eigenen Schlüssel zurück an den Sender (A).
3. Der Sender (A) entschlüsselt sein eigenes Schloss mit seinem Schlüssel, wodurch die Nachricht nur noch mit dem Schlüssel des Empfängers (B) verschlüsselt ist. Nun schickt er die Nachricht wieder an den Empfänger (B).
4. Der Empfänger (B) entschlüsselt die Nachricht mit seinem Schlüssel und kann sie nun lesen.
    """)

with st.expander("5. Einwegfunktionen"):
    st.write(r"""
#### Aufgabe 1: Inwiefern entspricht ein Telefonbuch einer Einwegfunktion?
Ein Telefonbuch lässt sich als eine Funktion $f$ betrachten, die jedem Namen $x$ eine Telefonnummer $y$ zuordnet.
Bei der richtigen Benutzung ist es leicht, einem bestimmten Namen $x_{1}$ die zugehörige Telefonnummer $y_{1}$ zuzuordnen.
Andersherum ist es jedoch wahnsinnig zeitaufwendig, basierend auf der Telefonnummer $y_{1}$ den zugehörigen Namen $x_{1}$ zu finden, da man praktisch das gesamte Telefonbuch durchsuchen müsste.
Somit handelt es sich bei einem Telefonbuch um eine Einwegfunktion.

#### Aufgabe 2: Beschreibe, inwiefern die folgenden Vorgänge Einwegfunktionen entsprechen:
a) Erbsen und Linsen mischen\
Das vermischen von Erbsen und Linsen aus dem sortierten Zustand ist einfach, wärend das wiederherstellen des sortierten Zustandes aus dem gemischten Zustand sehr zeitaufwendig ist.
Somit handelt es sich bei dem Vermischen von Erbsen und Linsen um eine Einwegfunktion.

b) Farben mischen\
Das vermischen von Farben aus dem ungemischten Zustand ist einfach, wärend das wiederherstellen des ungemischten Zustandes aus dem gemischten Zustand im Regelfall unmöglich ist.
Somit handelt es sich bei dem Vermischen von Farben um eine Einwegfunktion.

c) Geld ausgeben\
Der Vorgang des Geldausgebens ist in die Richtung des Ausgebens einfach, während der Vorgang des Geldzurückbekommens sehr aufwendig ist.
Ist man zusätzlich daran interessiert z.B. einen speziellen Schein wiederzubekommen, so ist der Vorgang des Geldzurückbekommens praktisch unmöglich.
Somit handelt es sich bei dem Geldausgeben um eine Einwegfunktion.


d) Sand und Kies mischen\
Das vermischen von Sand und Kies aus dem sortierten Zustand ist einfach, wärend das wiederherstellen des sortierten Zustandes aus dem gemischten Zustand sehr zeitaufwendig ist.
Somit handelt es sich bei dem Vermischen von Sand und Kies um eine Einwegfunktion.

#### Aufgabe: Inwiefern kann ein Briefkasten als Bild für eine Trapdoor-Einwegfunktion angesehen werden?
Ohne einen Schlüssel handelt es sich bei dem Einwerfen eines Briefes in einen Briefkasten um eine Einwegfunktion, da der Brief nicht mehr herausgenommen werden kann.
Der Schlüssel stellt eine geheime Zusatzinformation (trapdoor) dar, über die der Brief einfach wieder herausgenommen werden kann.
Somit handelt es sich bei dem Einwerfen eines Briefes in einen Briefkasten um eine Trapdoor-Einwegfunktion.
    """)

with st.expander("6. RSA auf einen Blick"):
    st.image("rsa-beschriftet.png")

with st.expander("7. euklidischer Algorithmus"):
    st.write(r"""
#### Aufgabe 1: Bestimme den Euklidischen Algorithmus für den ggT
a) 24 und 9\
24 mod 9 = 6 $\rightarrow$ 9 mod 6 = 3 $\rightarrow$ 6 mod 3 = 0 $\rightarrow$ ggT(24, 9) = 3

b) 36 und 18\
36 mod 18 = 0 $\rightarrow$ ggT(36, 18) = 18

c) 75 und 45\
75 mod 45 = 30 $\rightarrow$ 45 mod 30 = 15 $\rightarrow$ 30 mod 15 = 0 $\rightarrow$ ggT(75, 45) = 15

d) 720 und 288\
720 mod 288 = 144 $\rightarrow$ 288 mod 144 = 0 $\rightarrow$ ggT(720, 288) = 144

e) 1071 und 1029\
1071 mod 1029 = 42 $\rightarrow$ 1029 mod 42 = 21 $\rightarrow$ 42 mod 21 = 0 $\rightarrow$ ggT(1071, 1029) = 21
    """)

with st.expander("8. multiplikatives Inverses"):
    st.write(r"""

    """)
