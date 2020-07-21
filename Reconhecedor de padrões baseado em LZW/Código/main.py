import random
import copy
import time

class KNNClassificator():
    
    def __init__(self):
        
        tabela_asc = {}
        
        for i in range(256):
            tabela_asc[i] = bytes([ord(chr(i))])

        self.dicionario = [copy.deepcopy(tabela_asc) for _ in range(40)]
        
        self.state = 0        

    def predicao(self, Imgs, labels, k):   
        
        self.state = 1 
        
        predicoes = []
        
        for pessoa in range(len(Imgs)):
            
            compressionRates = []

            for category in range(len(self.dicionario)):
                compressionRates.append(self.LZWCompression(Imgs[pessoa], k, self.dicionario[category]))                
            
            predicoes.append(compressionRates.index(sorted(compressionRates)[0]))

        count = 0
        
        for i in range(len(labels)):
            if labels[i] == predicoes[i]:
                count += 1

        n = (count*100/len(labels))

        return n

    def Fit(self, Imgs, k):
        
        self.state = 0   
       
        for pessoa in range(len(Imgs)):
            
            for image in range(len(Imgs[pessoa])):
                self.LZWCompression(Imgs[pessoa][image], k, self.dicionario[pessoa])

    def crossValidation(self, Imgs):
        randomImgs = []
        labels = []

        for i in range(len(Imgs)):
            index = random.choice(range(len(Imgs[i])))
            randomImgs.append(Imgs[i].pop(index))
            labels.append(i)
  
        return randomImgs, labels

    def getKeysByValue(self, dictOfElements, valueToFind):
        ListaItens = dictOfElements.items()
        for item  in ListaItens:
            if item[1] == valueToFind:
                return item[0]
        return  -1
        
    def LZWCompression(self, image, k, dicionario):
        index = []
        table_size = len(dicionario)
        MAX = 2**k
    
        
        firstRound = True
        for pixel in image:
            if(firstRound):
                byte = bytes([ord(chr(pixel))])
                s = b''
        
            index = self.getKeysByValue(dicionario,s+byte)
            
            if index != -1:
                s += byte
            else:
                index.append(self.getKeysByValue(dicionario,s))
                if table_size < MAX and self.state == 0:
                    dicionario[table_size] = s + byte
                    table_size += 1
                s = byte
                
            byte = bytes([ord(chr(pixel))])
            
            firstRound = False
        
        return len(index)

def AbrirImg():

    Img = []
    for i in range(1,41):
        Temp = []
        for j in range(1,11):
            with open("orl_faces/s"+str(i)+"/"+str(j)+".pgm", "rb") as binary_file:
                    Temp.append(bytearray(binary_file.read()))
        Img.append(Temp)
        
    return Img

def main():

	tempo = []
	acc = []
    
    for i in range(9,17):
        
        start_time = time.time()
        
        KNN = KNNClassificator()
        
        Imgs = AbrirImg()
        
        train = copy.deepcopy(Imgs)
        
        test, labels = KNN.crossValidation(train)
       
        KNN.Fit(train, i)
        
        n = KNN.predicao(test,labels,i)

        tempo.append(time.time() - start_time)
        
        acc.append(n)

if __name__ =="__main__":
    main()