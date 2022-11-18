from string import ascii_lowercase
import pandas as pd
import streamlit as st
import enchant
import random
import math
import numpy as np
from sympy import isprime

st.set_page_config(layout="wide", page_title="Kryptographie", page_icon="🔐")
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
            try:
                if char.isupper():
                    encode_text += ascii_lowercase[(ascii_lowercase.index(char.lower()) + encode_index) % len(ascii_lowercase)].upper()
                elif char.islower():
                    encode_text += ascii_lowercase[(ascii_lowercase.index(char) + encode_index) % len(ascii_lowercase)]
                else:
                    encode_text += char
            except:
                encode_text += char

    elif caesar_mode == 'Unicode':
        for char in encode_text_input:
            try:
                encode_text += chr((ord(char) + encode_index) % 1114112)
            except:
                encode_text += char

    st.success(encode_text)

st.markdown('---')

st.subheader("Decode")
decode_text_input = st.text_input("Enter text to decode:")

if caesar_mode == 'phonetisches Alphabet (26 Buchstaben)':
    decode_index = st.slider('Index', 0, len(ascii_lowercase) - 1)

elif caesar_mode == 'Unicode':
    decode_index = st.slider('Index', 0, 1114111)

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
    if caesar_mode == 'phonetisches Alphabet (26 Buchstaben)':
        decode_text_cleaned = decode_text_input.replace(
            'ä', 'ae').replace('Ä', 'Ae').replace('ö', 'oe').replace('Ö', 'Oe').replace(
            'ü', 'ue').replace('Ü', 'Ue').replace('ß', 'ss')
        for char in decode_text_cleaned:
            try:
                if char.isupper():
                    decode_text += ascii_lowercase[(ascii_lowercase.index(char.lower()) - decode_index) % len(ascii_lowercase)].upper()
                elif char.islower():
                    decode_text += ascii_lowercase[(ascii_lowercase.index(char) - decode_index) % len(ascii_lowercase)]
                else:
                    decode_text += char
            except:
                decode_text += char

    elif caesar_mode == 'Unicode':
        for char in decode_text_input:
            try:
                decode_text += chr((ord(char) - decode_index) % 1114112)
            except:
                decode_text += char

    st.success(decode_text)

if dictsolve:
    try:
        solveMap = {}
        for i in range(len(ascii_lowercase) - 1):
            solve_text = ''
            for char in decode_text_input:
                try:
                    if char.isupper():
                        solve_text += ascii_lowercase[(ascii_lowercase.index(char.lower()) - i) % len(ascii_lowercase)].upper()
                    elif char.islower():
                        solve_text += ascii_lowercase[(ascii_lowercase.index(char) - i) % len(ascii_lowercase)]
                    else:
                        solve_text += char
                except:
                    solve_text += char

            solve_words = solve_text.encode("ascii", "ignore").decode().split(' ')

            for word in solve_words:
                if d.check(word):
                    solveMap[i] = {'idx': solveMap.get(i, {'idx': 0})['idx'] + 1}

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
    except:
        st.warning("Not working with Unicode")

if charsolve:
    try:
        solveMap = {}
        for i in range(len(ascii_lowercase) - 1):
            solve_text = ''
            for char in decode_text_input:
                try:
                    if char.isupper():
                        solve_text += ascii_lowercase[(ascii_lowercase.index(char.lower()) - i) % len(ascii_lowercase)].upper()
                    elif char.islower():
                        solve_text += ascii_lowercase[(ascii_lowercase.index(char) - i) % len(ascii_lowercase)]
                    else:
                        solve_text += char
                except:
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
    except:
        st.warning("Not working with Unicode")

with st.expander("Caesar Code"):
    st.code("""
encode_text_cleaned = encode_text_input.replace(
    'ä', 'ae').replace('Ä', 'Ae').replace('ö', 'oe').replace('Ö', 'Oe').replace(
    'ü', 'ue').replace('Ü', 'Ue').replace('ß', 'ss') # Gleiche das deutsche Alphabet mit dem Caesar Alphabet ab

encode_text = ''
for char in encode_text_cleaned: # Iteriere über jeden Buchstaben im gesäuberten Text
    if char.isalpha(): # Überprüfe ob es sich um einen Buchstaben handelt
        if char.isupper(): # Überprüfe ob es sich um einen Großbuchstaben handelt
            # Finde den Buchstaben im Alphabet und füge nun den um den Index verschobenen Buchstaben zum verschlüsselten Text hinzu
            encode_text += ascii_lowercase[(ascii_lowercase.index(char.lower()) + encode_index) % len(ascii_lowercase)].upper()
        elif char.islower(): # Überprüfe ob es sich um einen Kleinbuchstaben handelt
            # Finde den Buchstaben im Alphabet und füge nun den um den Index verschobenen Buchstaben zum verschlüsselten Text hinzu
            encode_text += ascii_lowercase[(ascii_lowercase.index(char) + encode_index) % len(ascii_lowercase)]
    else: # Wenn es sich nicht um einen Buchstaben handelt, füge ihn einfach zum verschlüsselten Text hinzu
        encode_text += char

print(encode_text) # Gib den verschlüsselten Text aus
""", language="python")

st.title("Vigenere Cipher")
vigenere_mode = st.radio("Mode", ('phonetisches Alphabet (26 Buchstaben)', 'Unicode'), key='vigenere_mode')
st.subheader("Encode")
encode_text_input_vi = st.text_input("Enter text to encode:", key="encode_text_input_vi")
encode_word_vi = st.text_input("Enter word to use for encoding:")
endoce_button_vi = st.button("Encode", key="encode_button_vi")

if endoce_button_vi:
    encode_text_vi = ''
    if vigenere_mode == 'phonetisches Alphabet (26 Buchstaben)':
        encode_text_cleaned_vi = encode_text_input_vi.replace(
            'ä', 'ae').replace('Ä', 'Ae').replace('ö', 'oe').replace('Ö', 'Oe').replace(
            'ü', 'ue').replace('Ü', 'Ue').replace('ß', 'ss')
        encode_word_vi_cleaned = "".join([char for char in encode_word_vi.lower() if char in ascii_lowercase])
        if len(encode_word_vi_cleaned) > 0:
            for i, char in enumerate(encode_text_cleaned_vi):
                encode_index_vi = ascii_lowercase.index(encode_word_vi_cleaned[i % len(encode_word_vi_cleaned)]) + 1
                try:
                    if char.isupper():
                        encode_text_vi += ascii_lowercase[(ascii_lowercase.index(char.lower()) + encode_index_vi) % len(ascii_lowercase)].upper()
                    elif char.islower():
                        encode_text_vi += ascii_lowercase[(ascii_lowercase.index(char) + encode_index_vi) % len(ascii_lowercase)]
                    else:
                        encode_text_vi += char
                except:
                    encode_text_vi += char
        else:
            encode_text_vi = encode_text_input_vi

    elif vigenere_mode == 'Unicode':
        if len(encode_word_vi) > 0:
            for i, char in enumerate(encode_text_input_vi):
                encode_index_vi = ord(encode_word_vi[i % len(encode_word_vi)]) + 1
                try:
                    encode_text_vi += chr((ord(char) + encode_index_vi) % 1114112)
                except:
                    encode_text_vi += char
        else:
            encode_text_vi = encode_text_input_vi

    st.success(encode_text_vi)

st.markdown('---')

st.subheader("Decode")
decode_text_input_vi = st.text_input("Enter text to decode:", key="decode_text_input_vi")
decode_word_vi = st.text_input("Enter word to use for decoding:")
decode_button_vi = st.button("Decode", key="decode_button_vi")

if decode_button_vi:
    decode_text_vi = ''
    if vigenere_mode == 'phonetisches Alphabet (26 Buchstaben)':
        decode_word_vi_cleaned = "".join([char for char in decode_word_vi.lower() if char in ascii_lowercase])
        if len(decode_word_vi_cleaned) > 0:
            for i, char in enumerate(decode_text_input_vi):
                decode_index_vi = ascii_lowercase.index(decode_word_vi_cleaned[i % len(decode_word_vi_cleaned)]) + 1
                try:
                    if char.isupper():
                        decode_text_vi += ascii_lowercase[(ascii_lowercase.index(char.lower()) - decode_index_vi) % len(ascii_lowercase)].upper()
                    elif char.islower():
                        decode_text_vi += ascii_lowercase[(ascii_lowercase.index(char) - decode_index_vi) % len(ascii_lowercase)]
                    else:
                        decode_text_vi += char
                except:
                    decode_text_vi += char
        else:
            decode_text_vi = decode_text_input_vi

    elif vigenere_mode == 'Unicode':
        if len(decode_word_vi) > 0:
            for i, char in enumerate(decode_text_input_vi):
                decode_index_vi = ord(decode_word_vi[i % len(decode_word_vi)]) + 1
                try:
                    decode_text_vi += chr((ord(char) - decode_index_vi) % 1114112)
                except:
                    decode_text_vi += char
        else:
            decode_text_vi = decode_text_input_vi
            
    st.success(decode_text_vi)

with st.expander("Vigenere Code"):
    st.code("""
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
print(encode_text_vi)
    """, language="python")

def gcd(a, b):
    """
    Berechne den größten gemeinsamen Teiler von a und b mit dem Euklidischen Algorithmus.
    """
    if (b == 0):
        return a
    else:
        return gcd(b, a % b)

def xgcd(e, phi):
    """
    Berechne das multiplikative Inverse von a mod b mit dem erweiterten Euklidischen Algorithmus.
    """
    xgcd_table = np.array([[phi, 1, 0], [e, 0, 1]])
    while xgcd_table[-1, 0] != 1:
        xgcd_table = np.vstack((
            xgcd_table, [
                xgcd_table[-2, 0] % xgcd_table[-1, 0], 
                xgcd_table[-2, 1] - xgcd_table[-1, 1] * (xgcd_table[-2, 0] // xgcd_table[-1, 0]), 
                xgcd_table[-2, 2] - xgcd_table[-1, 2] * (xgcd_table[-2, 0] // xgcd_table[-1, 0])
            ]
        ))
    return xgcd_table[-1, 2] % phi

def MillerRabin(n):
    d = n - 1
    j = 0
    while d % 2 == 0:
        d //= 2
        j += 1
    a = random.randint(2, n - 2)
    x = pow(a, d, n)
    if x == 1 or x == n - 1:
        return True
    for i in range(j - 1):
        x = pow(x, 2, n)
        if x == n - 1:
            return True
        if x == 1:
            return False
    return False

def generate_prime(prime, start, end):
    while True:
        n = random.randint(start, end)
        if isprime(n) and n != prime:
            for i in range(12):
                if not MillerRabin(n):
                    break
            return n

def generate_e(phi):
    while True:
        e = random.randint(2, phi - 1)
        if (math.gcd(e, phi) == 1):
            return e

st.title("RSA")
rsa_body = st.container()
with st.expander("RSA Dokumentation"):
    st.write(r"""
Das RSA-Verfahren (Rivest-Shamir-Adleman) ist der häufigst verwendete Vertreter, der asymetrischen Verschlüsselung.
Die Methode gilt noch heute als sicher, obwohl sie bereits 1977 vorgestellt wurde.
Der Aufbau besteht demnach aus einem öffentlichen Schlüssel zur Verschlüsselung und einem privaten Schlüssel, der zur Entschlüsselung verwendet wird.

### Schlüsselgenerierung
Im ersten Schritt müssen die beiden Primzahlen $p$ und $q$ ermittelt werden. Größere Primzahlen machen das Verfahren sicherer, weshalb ich schlussendlich Primzahlen basierend auf zufälligen Zahlen mit 300 Stellen generiere.
Die bekannteste Methode zur Primzahlgenerierung, die auch für sehr große Zahlen nutzbar ist, ist der Miller-Rabin Primzahltest.

Zur Erklärung soll für die ungerade Zahl $n$ überprüft werden, ob sie eine Primzahl ist.\
Dazu wird eine zufällige Zahl $a$ gewählt, für die gilt $2 \leq a \leq n-2$.\
Dann berechnet man $d$ und $j$ so, dass $n - 1 = d \cdot 2^j$ mit $d$ ungerade ist.\
Nun werden die Bedingungen $a^d \equiv 1 \pmod{n}$ und $a^{d\cdot2^r} \equiv -1 \pmod{n}$ für $r$ mit $0 \leq r \leq j-1$ überprüft.\
Da dieser Test stochastisch ist, kann es sein, dass $n$ mit einer kleinen Wahrscheinlichkeit fälschlicherweise als Primzahl erkannt wird. Deshalb führe ich den Test mehrmals durch.
Zur Beschleunigung filtere ich die Zahlen, die überprüft werden anfänglich mit der $isprime()$ Funktion der sympy Bibliothek.
    """)
    st.code(r"""
def MillerRabin(n):
    d = n - 1
    j = 0
    while d % 2 == 0:
        d //= 2
        j += 1
    a = random.randint(2, n - 2)
    x = pow(a, d, n)
    if x == 1 or x == n - 1:
        return True
    for i in range(j - 1):
        x = pow(x, 2, n)
        if x == n - 1:
            return True
        if x == 1:
            return False
    return False

def generate_prime(prime, start, end):
    while True:
        n = random.randint(start, end)
        if isprime(n) and n != prime:
            for i in range(12):
                if not MillerRabin(n):
                    break
            return n
    """, language="python")
    st.write(r"""
Im nächsten Schritt wird der sogenannte RSA-Modul $N$ berechnet für den gilt $N = p \cdot q$.
Und $\varphi(N)$ also die Eulersche $\varphi$-Funktion von $N$ für die gilt $\varphi(N) = (p-1) \cdot (q-1)$.

Nun kann der Verschlüsselungsexponent $e$ ermittelt werden. Es gilt $1<e<\varphi(N)$. Zusätzlich muss $e$ teilerfremd zu $\varphi(N)$ sein, also gilt $gcd(e, \varphi(n)) = 1$.\
Der größte gemeinsame Teiler von $e$ und $\varphi(N)$ kann mit dem Euklidischen Algorithmus berechnet werden.
    """)
    st.code(r"""
def gcd(a, b):
    if (b == 0):
        return a
    else:
        return gcd(b, a % b)

def generate_e(phi):
    while True:
        e = random.randint(2, phi - 1)
        if (gcd(e, phi) == 1):
            return e
    """, language="python")
    st.write(r"""
Alternativ lässt sich auch die effizientere $math.gcd(e, \varphi(N))$ Funktion verwenden.

###### Der öffentliche Schlüssel ist nun das Zahlenpaar ($N$, $e$).

Für den privaten Schlüssel brauchen wir den Entschlüsselungsexponenten $d$.
Es gilt $(e \cdot d) \: mod \: \varphi(N) = 1$.\
$d$ ist also das multiplikative Inverse von $e$ bezüglich des Moduls $\varphi(N)$.
Dies lässt sich mit dem erweiterten Euklidischen Algorithmus ermitteln.
    """)
    st.code(r"""
def xgcd(e, phi):
    xgcd_table = np.array([[phi, 1, 0], [e, 0, 1]])
    while xgcd_table[-1, 0] != 1:
        xgcd_table = np.vstack((
            xgcd_table, [
                xgcd_table[-2, 0] % xgcd_table[-1, 0], 
                xgcd_table[-2, 1] - xgcd_table[-1, 1] * (xgcd_table[-2, 0] // xgcd_table[-1, 0]), 
                xgcd_table[-2, 2] - xgcd_table[-1, 2] * (xgcd_table[-2, 0] // xgcd_table[-1, 0])
            ]
        ))
    return xgcd_table[-1, 2] % phi
    """, language="python")
    st.write(r"""
Alternativ lässt sich auch die effizientere $pow(e, -1, phi)$ Funktion verwenden.

###### Der private Schlüssel ist nun das Zahlenpaar ($N$, $d$).

### Verschlüsselung und Entschlüsselung
Um eine Nachricht $m$ zu verschlüsseln, wird die Verschlüsselungsfunktion $c = m^e \pmod{N}$ verwendet.
    """)
    st.code(r"""
ascii_message = [ord(char) for char in message]
encoded_ascii_message = [pow(m, e, N) for m in ascii_message]
encoded_message = " ".join([str(c) for c in encoded_ascii_message])
    """, language="python")
    st.write(r"""
Um eine verschlüsselte Nachricht $c$ zu entschlüsseln, wird die Entschlüsselungsfunktion $m = c^d \pmod{N}$ verwendet.
    """)
    st.code(r"""
encoded_ascii_message = [int(c) for c in encoded_message.split(" ")]
decoded_ascii_message = [pow(c, d, N) for c in encoded_ascii_message]
message = "".join([chr(c) for c in decode_message_ascii_rsa])
    """, language="python")
    st.write(r"""
### Beispiel
$p = 17$\
$q = 19$\
$N = p \cdot q = 17 \cdot 19 = 323$\
$\varphi(N) = (p-1) \cdot (q-1) = (17-1) \cdot (19-1) = 16 \cdot 18 = 288$\
$e = 7$ weil $gcd(7, 288) \equiv 1$\
$d = 247$ weil $(7 \cdot 247) \: mod \: 288 = 1$

Der öffentliche Schlüssel ist nun das Zahlenpaar ($N$, $e$) = ($323$, $7$).\
Der private Schlüssel ist nun das Zahlenpaar ($N$, $d$) = ($323$, $247$).

Verschlüsselung:\
$m = 42$\
$c = m^e \pmod{N} = 42^7 \pmod{323} = 253$

Entschlüsselung:\
$m = c^d \pmod{N} = 253^{247} \pmod{323} = 42$
    """)

rsa_erklaerung = st.expander("RSA Erklärung")

st.title("Mathe Aufgaben")
with st.expander("1. Modulo"):
    st.write(r"""
#### Aufgabe 1:
a) 27 mod 4 = 3 | print(27 % 4) $\rightarrow$ 4 $\cdot$ 6 + 3 = 27\
b) 26 mod 5 = 1 | print(26 % 5) $\rightarrow$ 5 $\cdot$5 + 1 = 26\
c) 18 mod 3 = 0 | print(18 % 3) $\rightarrow$ 3 $\cdot$ 6 + 0 = 18\
d) 18 mod 7 = 4 | print(18 % 7) $\rightarrow$ 7 $\cdot$ 2 + 4 = 18\
e) 21 mod 9 = 3 | print(21 % 9) $\rightarrow$ 9 $\cdot$ 2 + 3 = 21\
f) 37 mod 10 = 7 | print(37 % 10) $\rightarrow$ 10 $\cdot$ 3 + 7 = 37\
g) 100037 mod 10 = 7 | print(100037 % 10) $\rightarrow$ 10 $\cdot$ 10003 + 7 = 100037\
h) 107 mod 4 = 3 | print(107 % 4) $\rightarrow$ 4 $\cdot$ 26 + 3 = 107\
i) 1 mod 2 = 1 | print(1 % 2) $\rightarrow$ 2 $\cdot$ 0 + 1 = 1\
j) 3 mod 2 = 1 | print(3 % 2) $\rightarrow$ 2 $\cdot$ 1 + 1 = 3

#### Aufgabe 2:
a) sei k eine gerade Zahl. Berechne k mod 2\
2 % 2 = 0 $\rightarrow$ 2 $\cdot$ 1 + 0 = 2\
4 % 2 = 0 $\rightarrow$ 2 $\cdot$ 2 + 0 = 4
###### Eine gerade Zahl ist per Definition durch 2 teilbar. Daher ist der Rest 0.

b) sei k eine ungerade Zahl. Berechne k mod 2.\
1 % 2 = 1 $\rightarrow$ 2 $\cdot$ 0 + 1 = 1\
3 % 2 = 1 $\rightarrow$ 2 $\cdot$ 1 + 1 = 3
###### Eine ungerade Zahl ist per Definition nicht durch 2 teilbar. Daher ist der Rest 1.

#### Aufgabe 3:
a) Vergleiche  25 mod 4  und  (20 mod 4 + 5 mod 4) mod 4\
print(25 % 4, (20 % 4 + 5 % 4) % 4) $\rightarrow$ 1, 1 | identisch

b) Vergleiche  25 mod 4  und  (19 mod 4 + 6 mod 4) mod 4\
print(25 % 4, (19 % 4 + 6 % 4) % 4) $\rightarrow$ 1, 1 | identisch

c) Vergleiche  26 mod 4  und  (2 mod 4 $\cdot$ 13 mod 4) mod 4\
print(26 % 4, (2 % 4 $\cdot$ 13 % 4) % 4) $\rightarrow$ 2, 2 | identisch

d) Vergleiche  7$^{3}$ mod 4  und  (7 mod 4)$^3$ mod 4\
print(7$^3$ % 4, (7 % 4)$^{3}$ % 4) $\rightarrow$ 3, 3 | identisch

#### Regeln
(a + b) mod m = (a mod m + b mod m) mod m\
print((25 + 12) % 4, (25 % 4 + 12 % 4) % 4) $\rightarrow$ 1, 1

(a - b) mod m = (a mod m - b mod m) mod m\
print((25 - 12) % 4, (25 % 4 - 12 % 4) % 4) $\rightarrow$ 1, 1

(a $\cdot$ b) mod m = (a mod m $\cdot$ b mod m) mod m\
print((25 $\cdot$ 12) % 4, (25 % 4 $\cdot$ 12 % 4) % 4) $\rightarrow$ 0, 0

(a$^{b}$) mod m = (a mod m)$^{b}$ mod m\
print((25$^{12}$) % 4, (25 % 4)$^{12}$ % 4) $\rightarrow$ 1, 1

#### Aufgabe 4:
a) Es sei n irgendeine natürliche Zahl, die mit den Ziffern ...34 endet. Berechne n mod 4\
34 mod 4 = 2 | print(34 % 4) $\rightarrow$ 4 $\cdot$ 8 + 2 = 34\
12134 mod 4 = 2 | print(12134 % 4) $\rightarrow$ 4 $\cdot$ 3033 + 2 = 12134

b) Wie kann man leicht überprüfen, ob eine Zahl durch 4 teilbar ist?\
Die Zahl n ist durch 4 teilbar, wenn der Modulo 4 Rest 0 ergibt. $\rightarrow$ n mod 4 != 0 | z.B. print(24 % 4)

#### Aufgabe 5:
Es ist 10 Uhr am Vormittag (Mittwoch) und du hast in 50 Stunden einen Terminbeim Zahnarzt und in 70 Stunden einen Computerkurs. Wann finden die Terminestatt?\
Zahnarzt: 10 Uhr + 50 Stunden = 60 Uhr $\rightarrow$ 60 Uhr mod 24 = 12 Uhr\
Computerkurs: 10 Uhr + 70 Stunden = 80 Uhr $\rightarrow$ 80 Uhr mod 24 = 8 Uhr\
Der Zahnarzttermin ist am Freitag um 12 Uhr und der Computerkurs am Samstag um 8 Uhr.
        """)

with st.expander("2. Restklassen"):
    st.write(r"""
Restklassen
[a]$_{m}$ = {b $\in$ $\mathbf{Z}$ | $\exists$K $\in$ $\mathbf{Z}$ : b = k $\cdot$ m + a}\
Die Restklasse [a]$_{m}$ ist die Menge aller Zahlen b, die bei Modulo m den Rest a haben.

#### Aufgabe 1:
a) Versuche die obige Tabelle in Worte zu fassen.\
Die Tabelle zeigt die Restklassen mit m = 6.\
Die Spalten stellen jeweils einen unterschiedlichen Rest a dar.\
Die Reihe stellt ein unterschiedliches Vielfaches k dar.\
Für die einzelnen Felder gilt somit: b = k $\cdot$ m + a

b) Fertige eine entsprechende Tabelle für m = 5 an.
    """)

    st.table(
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
[0]$_{3}$ = {b aus Z | es gibt K aus Z mit b = k $\cdot$ 3 + 0} = [:, -6, -3, 0, 3, 6, :]\
[1]$_{3}$ = {b aus Z | es gibt K aus Z mit b = k $\cdot$ 3 + 1} = [:, -5, -2, 1, 4, 7, :]\
[1]$_{4}$ = {b aus Z | es gibt K aus Z mit b = k $\cdot$ 4 + 1} = [:, -7, -3, 1, 5, 9, :]

d) Gib drei verschiedene Repräsentanten der Restklassen [3]$_{7}$ und [2]$_{8}$ an.\
[3]$_{7}$ = [:, -11, 3, 10, :]\
[2]$_{8}$ = [:, -10, 2, 10, :]

e) Kennst Du Anwendungen von Restklassen im täglichen Leben?\
Mögliche Anwendungen wären die Uhrzeit, Wochentage und Kalender.

###### 1. Zeige, dass für alle Repräsentanten a $\in$ [4]$_{7}$ und b $\in$ [5]$_{7}$ gilt: a + b $\in$ [2]$_{7}$. Benutze dafür, dass sich a und b schreiben lassen als a = 7 $\cdot$ k$_{1}$ + 4 und b = 7 $\cdot$ k$_{2}$ + 5 mit ganzen Zahlen k$_{1}$ und k$_{2}$ und ermittle, welchen Rest a + b bei Division durch 7 hat.
[4]$_{7}$ = [:, -3, 4, 11, :]\
[5]$_{7}$ = [:, -2, 5, 12, :]\
Bei der Addition gilt: (4 + 5) % 7 = 9 % 7 = 2\
Das Ergebnis lautet also: [2]$_{7}$ = [:, -5, 2, 9, :]

Für a gilt: a = 7 $\cdot$ k$_{1}$ + 4\
Für b gilt: b = 7 $\cdot$ k$_{2}$ + 5\
Für a + b gilt: a + b = (7 $\cdot$ k$_{1}$ + 4) + (7 $\cdot$ k$_{2}$ + 5) = 7 $\cdot$ (k$_{1}$ + k$_{2}$) + 9\
Unter Betrachtung des Restes bei Division durch 7 ergibt sich: 7 $\cdot$ (k$_{1}$ + k$_{2}$) + 9 % 7 = 7 $\cdot$ (k$_{1}$ + k$_{2}$) + 2\
Mit k$_{3}$ = k$_{1}$ + k$_{2}$ ergibt sich: 7 $\cdot$ k$_{3}$ + 2\
Somit entsteht die Restklasse [2]$_{7}$.

###### 2. Zeige, dass für alle Repräsentanten a $\in$ [4]$_{7}$ und b $\in$ [5]$_{7}$ gilt: a $\cdot$ b $\in$ [6]$_{7}$. Benutze dafür, dass sich a und b schreiben lassen als a = 7 $\cdot$ k$_{1}$ + 4 und b = 7 $\cdot$ k$_{2}$ + 5 mit ganzen Zahlen k$_{1}$ und k$_{2}$ und ermittle, welchen Rest a $\cdot$ b bei Division durch 7 hat.
[4]$_{7}$ = [:, -3, 4, 11, :]\
[5]$_{7}$ = [:, -2, 5, 12, :]\
Bei der Multiplikation gilt: (4 $\cdot$ 5) % 7 = 20 % 7 = 6\
Das Ergebnis lautet also: [6]$_{7}$ = [:, -1, 6, 13, :]

Für a gilt: a = 7 $\cdot$ k$_{1}$ + 4\
Für b gilt: b = 7 $\cdot$ k$_{2}$ + 5\
Für a $\cdot$ b gilt: a $\cdot$ b = (7 $\cdot$ k$_{1}$ + 4) $\cdot$ (7 $\cdot$ k$_{2}$ + 5) = 49 $\cdot$ k$_{1}$ $\cdot$ k$_{2}$ + 35 $\cdot$ k$_{1}$ + 28 $\cdot$ k$_{2}$ + 20\
Unter Betrachtung des Restes bei Division durch 7 ergibt sich: 49 $\cdot$ k$_{1}$ $\cdot$ k$_{2}$ + 35 $\cdot$ k$_{1}$ + 28 $\cdot$ k$_{2}$ + 20 % 7 = 49 $\cdot$ k$_{1}$ $\cdot$ k$_{2}$ + 35 $\cdot$ k$_{1}$ + 28 $\cdot$ k$_{2}$ + 6\
Mit k$_{3}$ = 7 $\cdot$ k$_{1}$ $\cdot$ k$_{2}$ + 5 $\cdot$ k$_{1}$ + 4 $\cdot$ k$_{2}$ ergibt sich: 7 $\cdot$ k$_{3}$ + 6\
Somit entsteht die Restklasse [6]$_{7}$.

3. Leicht darstellen kann man Addition und Multiplikation von Restklassen mit Tabellen. Wenn aus dem Zusammenhang klar ist, welche Restklassen man betrachtet, kann man die Symbole [ ]$_{m}$ auch weglassen.

a) Zeige, dass für die Restklassen modulo 3 folgende Additions- und Multiplikationstabelle gilt:\
Der Rest n bei der Addition entsteht aus (3 $\cdot$ k$_{1}$ + n$_{1}$) + (3 $\cdot$ k$_{2}$ + n$_{2}$) | Für n muss somit gelten: n = (n$_{1}$ + n$_{2}$) % 3
Der Rest n bei der Multiplikation entsteht aus (3 $\cdot$ k$_{1}$ + n$_{1}$) $\cdot$ (3 $\cdot$ k$_{2}$ + n$_{2}$) | Für n muss somit gelten: n = (n$_{1}$ $\cdot$ n$_{2}$) % 3

Additionstabelle:
    """)

    additionTable3a = np.zeros((3, 3), dtype=int)
    for row in range(3):
        for col in range(3):
            additionTable3a[row][col] = (row + col) % 3

    st.table(
        pd.DataFrame(
            additionTable3a
        )
    )

    st.write(r"""
Multiplikationstabelle:
    """)

    multiplikationsTable3a = np.zeros((3, 3), dtype=int)
    for row in range(3):
        for col in range(3):
            multiplikationsTable3a[row][col] = (row * col) % 3
    
    st.table(
        pd.DataFrame(
            multiplikationsTable3a
        )
    )

    st.write(r"""
b) Ermittle Additions- und Multiplikationstabelle für die Restklassen modulo 6.

Additionstabelle:
    """)

    additionTable6b = np.zeros((6, 6), dtype=int)
    for row in range(6):
        for col in range(6):
            additionTable6b[row][col] = (row + col) % 6
        
    st.table(
        pd.DataFrame(
            additionTable6b
        )
    )

    st.write(r"""
Multiplikationstabelle:
    """)

    multiplikationsTable6b = np.zeros((6, 6), dtype=int)
    for row in range(6):
        for col in range(6):
            multiplikationsTable6b[row][col] = (row * col) % 6

    st.table(
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
a) 8$^{9}$ mod 7 = 1$^{9}$ mod 7 = 1

b) 6$^{9}$ mod 7 = (-1)$^{9}$ mod 7 = 6

c) 54$^{16}$ mod 55 = (-1)$^{16}$ mod 55 = 1

d) 3$^{333}$ mod 26 = (3$^{3}$)$^{100}$ mod 26\
    = (3$^{3}$ % 26)$^{100}$ mod 26\
    = 1$^{100}$ mod 26 = 1

e) 2$^{268}$ mod 17 = (2$^{4}$)$^{67}$ mod 17\
    = (2$^{4}$ % 17)$^{67}$ mod 17\
    = (-1)$^{67}$ mod 17\
    = (-1) % 17 = 16

f) 2$^{269}$ mod 17 = (2$^{268}$ $\cdot$ 2) mod 17\
    = (2$^{268}$ mod 17 $\cdot$ 2 mod 17) mod 17\
    = (16 $\cdot$ 2) mod 17 = 15

g) 2$^{27}$0 mod 19 = (2$^{9}$)$^{30}$ mod 19\
    = (2$^{9}$ % 19)$^{30}$ mod 19\
    = (-1)$^{30}$ mod 19 = 1

h) 2$^{271}$ mod 19 = (2$^{270}$ $\cdot$ 2) mod 19\
    = (2$^{270}$ mod 19 $\cdot$ 2 mod 19) mod 19\
    = (1 $\cdot$ 2) mod 19 = 2

i) 3$^{333}$ mod 15 = (3 $\cdot$ 3$^{332}$) mod 15\
    = (3 $\cdot$ (3$^{4}$)$^{83}$) mod 15\
    = (3 $\cdot$ 81$^{83}$) mod 15\
    = (3 $\cdot$ 6$^{83}$) mod 15\
    = (3 mod 15 $\cdot$ 6$^{83}$ mod 15) mod 15\
    = 3 $\cdot$ 6 mod 15 = 3 | Weil 6$^{k}$ mod 15 = 6
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
a) ggT: 24 und 9\
24 mod 9 = 6 $\rightarrow$ 9 mod 6 = 3 $\rightarrow$ 6 mod 3 = 0 $\rightarrow$ ggT(24, 9) = 3\
Somit ist der größte gemeinsame Teiler von 24 und 9 3.

b) ggT: 36 und 18\
36 mod 18 = 0 $\rightarrow$ ggT(36, 18) = 18\
Somit ist der größte gemeinsame Teiler von 36 und 18 18.

c) ggT: 75 und 45\
75 mod 45 = 30 $\rightarrow$ 45 mod 30 = 15 $\rightarrow$ 30 mod 15 = 0 $\rightarrow$ ggT(75, 45) = 15\
Somit ist der größte gemeinsame Teiler von 75 und 45 15.

d) ggT: 720 und 288\
720 mod 288 = 144 $\rightarrow$ 288 mod 144 = 0 $\rightarrow$ ggT(720, 288) = 144\
Somit ist der größte gemeinsame Teiler von 720 und 288 144.

e) ggT: 1071 und 1029\
1071 mod 1029 = 42 $\rightarrow$ 1029 mod 42 = 21 $\rightarrow$ 42 mod 21 = 0 $\rightarrow$ ggT(1071, 1029) = 21\
Somit ist der größte gemeinsame Teiler von 1071 und 1029 21.
    """)

with st.expander("8. multiplikatives Inverses"):
    st.write(r"""
#### Aufgabe 2: Finde die multiplikative Inverse von $a$ modulo $m$.
###### a) die multiplikative Inverse von $a = 15$ modulo $m = 26$
Gesucht ist $0 < b < 26 \in \mathbb{Z}$ für das gilt: $(b \cdot 15)$ mod $26 = 1$ oder $1 = b \cdot 15 + k \cdot 26$.
    """)
    st.image("8.a.png")
    st.write(r"""
Somit ist $b = 7$.\
Zur Kontrolle: $(7 \cdot 15)$ mod $26 = 1$.

###### b) die multiplikative Inverse von $a = 5$ modulo $m = 48$
Gesucht ist $0 < b < 48 \in \mathbb{Z}$ für das gilt: $(b \cdot 5)$ mod $48 = 1$ oder $1 = b \cdot 5 + k \cdot 48$.
    """)
    st.image("8.b.png")
    st.write(r"""
    Somit wäre $b = -19$.\
    Da $b$ jedoch positiv sein muss, wählen wir den nächsten positiven Wert in der Restklasse $[29]_{48}$ (Weil -19 mod 48 = 29), also gilt $b = 29$.\
    Zur Kontrolle: $(29 \cdot 5)$ mod $48 = 1$.
    """)

gen_rsa = rsa_body.button("Generate new keys", key="generate_new_keys")

if 'rsa_p' not in st.session_state or gen_rsa:
    with rsa_body:
        with st.spinner('Generating new keys...'):
            st.session_state['rsa_p'] = generate_prime(0, 10**300, 10**301)
            st.session_state['rsa_q'] = generate_prime(st.session_state['rsa_p'], 10**300, 10**301)
            st.session_state['rsa_n'] = st.session_state['rsa_p'] * st.session_state['rsa_q']
            st.session_state['rsa_phi'] = (st.session_state['rsa_p'] - 1) * (st.session_state['rsa_q'] - 1)
            st.session_state['rsa_e'] = generate_e(st.session_state['rsa_phi'])
            st.session_state['rsa_d'] = pow(st.session_state['rsa_e'], -1, st.session_state['rsa_phi']) 

            # langsamere eigene Implementierung um das multiplikative Inverse zu berechnen
            # st.session_state['rsa_d'] = xgcd(st.session_state['rsa_e'], st.session_state['rsa_phi'])


rsa_body.text(
f"""
p: {st.session_state['rsa_p']}
q: {st.session_state['rsa_q']}
n: {st.session_state['rsa_n']}
phi: {st.session_state['rsa_phi']}
e: {st.session_state['rsa_e']}
d: {st.session_state['rsa_d']}
""")

rsa_body.subheader("Encode")
encode_message_rsa = rsa_body.text_input("Enter message to encode:", key="encode_message_rsa")
encode_button_rsa = rsa_body.button("Encode", key="encode_button_rsa")
encode_success_rsa = rsa_body.empty()

if encode_button_rsa:
    encode_message_ascii_rsa = [ord(char) for char in encode_message_rsa]
    encode_message_ascii_rsa = [pow(c, st.session_state['rsa_e'], st.session_state['rsa_n']) for c in encode_message_ascii_rsa]
    encode_success_rsa.code(" ".join([str(c) for c in encode_message_ascii_rsa]))

rsa_body.markdown("---")

rsa_body.subheader("Decode")
decode_message_rsa = rsa_body.text_input("Enter message to decode:", key="decode_message_rsa")
decode_button_rsa = rsa_body.button("Decode", key="decode_button_rsa")
decode_success_rsa = rsa_body.empty()

if decode_button_rsa:
    decode_message_ascii_rsa = [int(c) for c in decode_message_rsa.split(" ")]
    decode_message_ascii_rsa = [pow(c, st.session_state['rsa_d'], st.session_state['rsa_n']) for c in decode_message_ascii_rsa]
    decode_success_rsa.success("".join([chr(c) for c in decode_message_ascii_rsa]))

st.markdown(
    """
    <h1>Mein gesamter Code ist auf <a href="https://github.com/foersterrobert/Kryptographie">Github</a> verfügbar. :)<h1>
    """,
    unsafe_allow_html=True
)