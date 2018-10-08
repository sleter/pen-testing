import sys

class PermCypher:
    def __init__(self):
        self.mode = sys.argv[1]
        self.key = sys.argv[2]
        self.key = [int(i) for i in self.key]
        self.inputFileName = sys.argv[3]
        self.outputFileName = sys.argv[4]

    def importData(self):
        with open(self.inputFileName) as file:
            data = file.read()
        return data

    def exportData(self, data):
        with open(self.outputFileName, 'w') as file:
            file.write(data)
    
    def encrypt(self, data):
        data = "".join(data.split(" "))
        out = ""
        for _ in range(0, len(data)%len(self.key)*-1%len(self.key)):
            data += "X"
        for offset in range(0, len(data), len(self.key)):
            for e in [a-1 for a in self.key]:
                out += data[offset+e]
            out += " "
        return out[:-1].replace(" ","")

    def inverse_key(self):
        inverse = []
        for position in range(min(self.key),max(self.key)+1,1):
            inverse.append(self.key.index(position)+1)
        print('inversed_key: '+str(inverse))
        return inverse

    def decrypt(self, data):
        self.key = self.inverse_key()
        return self.encrypt(data).replace(" ","")
    
    def translate(self):
        data = self.importData()
        if self.mode == '-d':
            self.exportData(self.decrypt(data))
        elif self.mode == '-e':
            self.exportData(self.encrypt(data))



def main():
    pc = PermCypher()
    pc.translate()


if __name__ == "__main__":
    main()
