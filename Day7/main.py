def text_to_morse_code(text):
    """
    :type text: str
    :rtype: str

    converts text to morse code
    """

    # wow, what a fun dict of morse code
    morse_code_dict = {"a": ".-", "b": "-...", "c": "-.-.", "d": "-..", "e": ".", "f": "..-.", "g": "--.", "h": "....",
                       "i": "..", "j": ".---", "k": "-.-", "l": ".-..", "m": "--", "n": "-.", "o": "---", "p": ".--.",
                       "q": "--.-", "r": ".-.", "s": "...", "t": "-", "u": "..-", "v": "...-", "w": ".--", "x": "-..-",
                       "y": "-.--", "z": "--..", "1": ".----", "2": "..---", "3": "...--", "4": "....-", "5": ".....",
                       "6": "-....", "7": "--...", "8": "---..", "9": "----.", "0": "-----", ".": ".-.-.-",
                       ",": "--..--", "?": "..--..", "'": ".----.", "/": "-..-.", "(": "-.--.", ")": "-.--.-",
                       "&": ".-...", ":": "---...", ";": "-.-.-.", "=": "-...-", "+": ".-.-.", "-": "-....-",
                       "_": "..--.-", "\"": ".-..-.", "$": "...-..-", "!": "-.-.--", "@": ".--.-.", " ": "/"}

    parseable_text = []

    for char in list(text.lower()):
        if char in morse_code_dict:
            parseable_text.append(char)

    morse_code = [morse_code_dict[char] for char in parseable_text]

    morse_code = " ".join(morse_code)

    return morse_code


print(text_to_morse_code("Hello There"))
