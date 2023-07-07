import random
chemicals = ["H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne", "Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar", "K", "Ca", "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn", "Ga", "Ge", "As", "Se", "Br", "Kr", "Rb", "Sr", "Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "In", "Sn", "Sb", "Te", "I", "Xe", "Cs", "Ba", "La", "Ce", "Pr", "Nd", "Pm", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu", "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg", "Tl", "Pb", "Bi", "Po", "At", "Rn", "Fr", "Ra", "Ac", "Th", "Pa", "U", "Np", "Pu", "Am", "Cm", "Bk", "Cf", "Es", "Fm", "Md", "No", "Lr", "Rf", "Db", "Sg", "Bh", "Hs", "Mt", "Ds", "Rg", "Cn", "Nh", "Fl", "Mc", "Lv", "Ts", "Og"]
CHEMICALS = [i.lower() for i in chemicals]
#ANSWER = "MONGOLSKO"
ANSWER = "KKKKK"

with open("chemicals.txt", "r") as f:
    WORDS = f.read().split("\n")[:-1]
# Filter only 5+length words
#WORDS = [i for i in WORDS if len(i) >= 5]


def protons(element: str) -> int:
    """Returns the number of protons in an element.

        Args:
            element (str): The element to find the number of protons for.

        Returns:
            int: The number of protons in the element. -1 is returned when element is not found.
    """
    element = element.lower()
    if element in CHEMICALS:
        return CHEMICALS.index(element) + 1
    return -1


def char_to_num(character: str) -> int:
    """ Translates character to number.

        Args:
            character (str): The character to translate.

        Returns:
            int: The number the character represents.
    """
    return ord(character.lower()) - 96


def go(word: str, formulae: str, answer: int, nice: str) -> tuple:
    """ Tries to create a formulae from word.

        Args:
            word (str): The word to create a formulae from.
            formulae (str): The current formulae.
            answer (int): The answer we have to achieve.
            nice (str): The nice formulae.

        Returns:
            str: The formulae created if it has correct answer..
    """
    if not word:
        if eval(formulae) == answer:
            return formulae, nice
        return None
    operators = ("+", "-", "*")
    first_op = ("", "- ")
    for length in (1, 2):
        if len(word) < length:
            continue
        if (prot := protons(word[:length])) != -1:
            if not formulae:
                for op in first_op:
                    if (result := go(word[length:], f"{op}{prot}", answer, f"{op}{word[:length]}")) is not None:
                        return result
            else:
                for op in operators:
                    if (result := go(word[length:], f"{formulae} {op} {prot}", answer, f"{nice} {op} {word[:length]}")) is not None:
                        return result


for i in ANSWER:
    while True:
        word = random.choice(WORDS)
        reply = go(word, "", char_to_num(i), "")
        if reply is not None:
            formulae, nice = reply
            WORDS.remove(word)
            print(" NEXT WORD")
            print(f"{formulae} == {char_to_num(i)}")
            print(f"{nice} == {i}")
            break
