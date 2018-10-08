import sys

class Vigenere:
    def __init__(self):
        self.mode = sys.argv[1]
        self.key = sys.argv[2]
        self.inputFileName = sys.argv[3]
        self.outputFileName = sys.argv[4]

    def importData(self):
        with open(self.inputFileName) as file:
            data = file.read()
        return data

    def exportData(self, data):
        with open(self.outputFileName, 'w') as file:
            file.write(data)

    def transform(self):
        # creating integer list based on key values
        integer_key = [ord(i) for i in self.key]
        # importing text
        text = self.importData()
        # creating integer list based on text values
        integer_text = [ord(i) for i in text]
        output = ''
        # iteration as many times as the length of the input text (or in this case integer list)
        for i in range(len(integer_text)):
            # choosing proper integer_key value, we need this because key is shorter that text
            val = integer_key[i % len(self.key)]
            # if we use decreption we will want to add negative values to integer_text values
            if self.mode == '-d':
                val *= -1
            # add up integer text value and corresponding key integer values
            # modulo take care of not exceeding the character scope
            v = (integer_text[i] - 32 + val) % 95
            # convert every single value from integer to character
            output += chr(v + 32)
        self.exportData(output)

def main():
    v = Vigenere()
    v.transform()

if __name__ == "__main__":
    main()