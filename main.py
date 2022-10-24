from string import ascii_lowercase
import pandas as pd
import streamlit as st
import enchant
import random
import math
import numpy as np

st.title("Caeser-Verschlüsselung")
st.subheader("Encode")
encode_text_input = st.text_input("Enter text to encode:")
encode_text_cleaned = encode_text_input.replace(
    'ä', 'ae').replace('Ä', 'Ae').replace('ö', 'oe').replace('Ö', 'Oe').replace(
    'ü', 'ue').replace('Ü', 'Ue').replace('ß', 'ss')
encode_index = st.slider("Select index to encode:", 0, len(ascii_lowercase) - 1)
endoce_button = st.button("Encode")

if endoce_button:
    encode_text = ''
    for char in encode_text_cleaned:
        if char.isalpha():
            if char.isupper():
                encode_text += ascii_lowercase[(ascii_lowercase.index(char.lower()) + encode_index) % len(ascii_lowercase)].upper()
            elif char.islower():
                encode_text += ascii_lowercase[(ascii_lowercase.index(char) + encode_index) % len(ascii_lowercase)]
        else:
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

letter_distribution_de = {
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

letter_distribution_en = {
    'a': 8.2,
    'b': 1.5,
    'c': 2.8,
    'd': 4.3,
    'e': 13,
    'f': 2.2,
    'g': 2,
    'h': 6.1,
    'i': 7,
    'j': 0.15,
    'k': 0.77,
    'l': 4,
    'm': 2.4,
    'n': 6.7,
    'o': 7.5,
    'p': 1.9,
    'q': 0.095,
    'r': 6,
    's': 6.3,
    't': 9.1,
    'u': 2.8,
    'v': 0.98,
    'w': 2.4,
    'x': 0.15,
    'y': 2,
    'z': 0.074
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
        for key in solveMapKeys:
            st.text(
                f'{solveMap[key]["str"]} at index {key}')
    else:
        st.text("No solution found")

if charsolve:
    # solveMap = {
    #     k:0 for k in ascii_lowercase
    # }
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
        solve_text_distribution = {}
        for l in solve_text_ascii:
            if l in solve_text_distribution.keys():
                solve_text_distribution[l] += 1
    
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
encode_message_rsa = st.text_input("Enter message to encode:", key="encode_message_rsa", value="hallo")
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

with st.expander("Aufgaben Modulo"):
    st.text("""
# 1. Aufgaben:
# a) 27 mod 4
print(27 % 4) # 4 * 6 + 3 = 27

# b) 26 mod 5
print(26 % 5) # 5 * 5 + 1 = 26

# c) 18 mod 3
print(18 % 3) # 3 * 6 + 0 = 18

# g) 100037 mod 10
print(100037 % 10) # 10 * 10003 + 7 = 100037

# 2. Aufgaben:
# a) sei k eine gerade Zahl. Berechne k mod 2.
print(2 % 2) # 2 * 1 + 0 = 2
print(4 % 2) # 2 * 2 + 0 = 4
# Eine gerade Zahl ist per Definition durch 2 teilbar. Daher ist der Rest 0.

# b) sei k eine ungerade Zahl. Berechne k mod 2.
print(1 % 2) # 2 * 0 + 1 = 1
print(3 % 2) # 2 * 1 + 1 = 3
# Eine ungerade Zahl ist per Definition nicht durch 2 teilbar. Daher ist der Rest 1.

# 3. Aufgaben:
# a) Vergleiche  25 mod 4  und  (20 mod 4 + 5 mod 4) mod 4
print(25 % 4, (20 % 4 + 5 % 4) % 4) # 1, 1

# b) Vergleiche  25 mod 4  und  (19 mod 4 + 6 mod 4) mod 4
print(25 % 4, (19 % 4 + 6 % 4) % 4) # 1, 1

# c) Vergleiche  26 mod 4  und  (2 mod 4·13 mod 4) mod 4
print(26 % 4, (2 % 4 * 13 % 4) % 4) # 2, 2

# d) Vergleiche  7**3 mod 4  und  (7 mod 4)**3 mod 4
print(7**3 % 4, (7 % 4)**3 % 4) # 3, 3

### Regeln
# (a + b) mod m = (a mod m + b mod m) mod m
print((25 + 12) % 4, (25 % 4 + 12 % 4) % 4) # 1, 1
# (a - b) mod m = (a mod m - b mod m) mod m
print((25 - 12) % 4, (25 % 4 - 12 % 4) % 4) # 1, 1
# (a * b) mod m = (a mod m * b mod m) mod m
print((25 * 12) % 4, (25 % 4 * 12 % 4) % 4) # 0, 0
# (a ** b) mod m = (a mod m) ** b mod m
print((25 ** 12) % 4, (25 % 4) ** 12 % 4) # 1, 1

# 4. Aufgaben:
# a) Es sei n irgendeine natürliche Zahl, die mit den Ziffern ...34 endet. Berechne n mod 4
print(34 % 4, (12100 + 34) % 4) # 2
# b) Wie kann man leicht überprüfen, ob eine Zahl durch 4 teilbar ist?
# n mod 4 != 0
print(24 % 4)

# 5. Aufgaben
# Es ist 10 Uhr am Vormittag (Mittwoch) und du hast in 50 Stunden einen Terminbeim Zahnarzt und in 70 Stunden einen Computerkurs. Wann finden die Terminestatt?
print((10 + 50) % 24, (10 + 70) % 24) # 12, 8
# Der Zahnarzttermin ist am Freitag um 12 Uhr und der Computerkurs am Samstag um 8 Uhr.
        """
    )

with st.expander("Aufgaben Restklassen"):
    st.text("""
# Restklassen
# [a]m = {b aus Z | es existiert K aus Z für das gilt: b = k * m + a} = {b | b identisch mit a mod m}
# Die Restklasse einer ganzen Zahlamodulo einer Zahlmist die Menge all derZahlen, die bei Division durchmdenselben (positiven)Restlassenwiea. Die Restklassevonamodulombezeichnet man als [a]m, und es gilt

# Aufgaben 1.
# a) Versuche die obige Tabelle in Worte zu fassen.
# Die Tabelle zeigt die Restklassen modulo 6

# b) Fertige eine entsprechende Tabelle für m = 5 an.
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

    st.text("""
# # c) Bestimme [0]3,[1]3 und [1]4.
# # [0]3 = [:, -6, -3, 0, 3, 6, :]
# # [1]3 = {b aus Z | es gibt K aus Z mit b = k * 3 + 1} = [:, -5, -2, 1, 4, 7, :]
# # [1]4 = [:, -7, -3, 1, 5, 9, :]

# # d) Gib drei verschiedene Repräsentanten der Restklassen [3]7 und [2]8 an.
# # [3]7 = [:, -11, 3, 10, :]
# # [2]8 = [:, -10, 2, 10, :]

# # e) Kennst Du Anwendungen von Restklassen im täglichen Leben?
# # Uhrzeit, Wochentage, Kalender, ...

1. Zeige, dass für alle Repräsentanten a aus [4]7 und b aus [5]7 gilt: a+b aus [2]7. Benutze dafür, dass sich a und b schreiben lassen als a=7·k1+4 und b=7·k2+5 mit ganzen Zahlen k1 und k2 und ermittle, welchen Rest a+b bei Division durch 7 hat.
# [4]7 = [:, -3, 4, 11, :]
# [5]7 = [:, -2, 5, 12, :]
# (4 + 5) % 7 = 9 % 7 = 2

# [2]7 = [:, -5, 2, 9, :]
# Für a gilt: a = 7 * k1 + 4
# Für b gilt: b = 7 * k2 + 5
# Für a + b gilt: a + b = (7 * k1 + 4) + (7 * k2 + 5) = 7 * (k1 + k2) + 9 = 7 * k3 + (9 % 7) = 7 * k3 + 2 mit k3 = k1 + k2

2. Zeige, dass für alle Repräsentanten a aus [4]7 und b aus [5]7 gilt: a·b aus [6]7. Benutze dafür, dass sich a und b schreiben lassen als a=7·k1+4 und b=7·k2+5 mit ganzen Zahlen k1 und k2 und ermittle, welchen Rest a·b bei Division durch 7 hat.
# [4]7 = [:, -3, 4, 11, :]
# [5]7 = [:, -2, 5, 12, :]
# (4 * 5) % 7 = 20 % 7 = 6

# [6]7 = [:, -1, 6, 13, :]
# Für a gilt: a = 7 * k1 + 4
# Für b gilt: b = 7 * k2 + 5
# Für a * b gilt: 
#   a * b = (7 * k1 + 4) * (7 * k2 + 5) = 49 * k1 * k2 + 35 * k1 + 28 * k2 + 20 
#         = 49 * k3 + 35 * k1 + 28 * k2 + 20 = 7 * (7 * k3 + 5 * k1 + 4 * k2) + 20 | mit k3 = k1 * k2
#         = 7 * k4 + (20 % 7) = 7 * k4 + 6 mit k4 = 7 * k3 + 5 * k1 + 4 * k2    

3. Leicht darstellen kann man Addition und Multiplikation von Restklassen mit Tabellen. Wenn aus dem Zusammenhang klar ist, welche Restklassen man betrachtet, kann man die Symbole [ ]m auch weglassen.

a) Zeige, dass für die Restklassen modulo 3 folgende Additions- und Multiplikationstabelle gilt:
    Der Rest n bei der Addition entsteht aus (3 * k1 + n1) + (3 * k2 + n2) | Für n muss somit gelten: n = (n1 + n2) % 3
    Der Rest n bei der Multiplikation entsteht aus (3 * k1 + n1) * (3 * k2 + n2) | Für n muss somit gelten: n = (n1 * n2) % 3
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

    multiplikationsTable3a = np.zeros((3, 3))
    for row in range(3):
        for col in range(3):
            multiplikationsTable3a[row][col] = (row * col) % 3
    
    st.dataframe(
        pd.DataFrame(
            multiplikationsTable3a
        )
    )

    st.text("""
    b) Ermittle Additions- und Multiplikationstabelle für die Restklassen modulo 6.
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

    multiplikationsTable6b = np.zeros((6, 6))
    for row in range(6):
        for col in range(6):
            multiplikationsTable6b[row][col] = (row * col) % 6

    st.dataframe(
        pd.DataFrame(
            multiplikationsTable6b
        )
    )

with st.expander("Modulares Potenzieren"):
    st.text("""
    (a·b) mod m = (a mod m·b mod m) mod m
    (a**b) mod m = (a mod m)**b mod m

    7**4 mod 12 = 7**2 * 7**2 mod 12 = 7**2 mod 12 * 7**2 mod 12 = 7 mod 12 * 7 mod 12 = 7 * 7 mod 12 = 49 mod 12 = 1
    """)