'''
Word Puzzles
Ryley Higa, James Jia, Shaksham Saini

'''
import urllib2

class wordDictionary:
    def __init__(self, url):
        #Turn into dictionary of the form (word category, list of words within that category)
        data = urllib2.urlopen(url)
        self.dictionary = {} 
        for line in data:
            words = line.split(":")
            category = words[0]
            wordList = words[1].split(", ")
            wordList[0] = wordList[0].replace('\t','')
            wordList[-1] = wordList[-1].replace('\r','').replace('\n','')
            self.dictionary[words[0]] = wordList
    
    def getLetters(self, category, position, firstLetter = None, secondLetter = None, thirdLetter = None):
        letters = []
        for word in self.dictionary[category]:
            if ((word[0] == firstLetter or firstLetter == None) and (word[1] == secondLetter or secondLetter == None) and \
                (word[2] == thirdLetter or thirdLetter == None)):
                newLetter = word[position]
                if not newLetter in letters: 
                    letters.append(newLetter)
        return letters
            
    def getWords(self, category = None, firstLetter = None, secondLetter = None, thirdLetter = None):
        words = []
        for word in self.dictionary[category]:
            if ((word[0] == firstLetter or firstLetter == None) and (word[1] == secondLetter or secondLetter == None) and \
                (word[2] == thirdLetter or thirdLetter == None)):
                words.append(word)
        return words
    
def intersection(L1, L2):
    newL = []
    for e in L1:
        if e in L2:
            newL.append(e)
    return newL
        

'''
Letter Formulation Problem
'''
class LetterCSP:
    def __init__(self, url, dictionary):
        data = urllib2.urlopen(url)
        i = 0
        self.valTracker = {}
        for line in data:
            if i == 0:
                self.size = int(line)
                for j in range(1,self.size+1):
                    self.valTracker[j] = []
            else:
                labels = line.split(":")
                category = labels[0]
                entries = labels[1].split(",")
                entries[-1] = entries[-1].replace("\r\n","")
                position = 0
                for entry in entries:
                    key = int(entry)
                    if not self.valTracker[key]: 
                        self.valTracker[key] = dictionary.getLetters(category, position)
                    else:
                        self.valTracker[key] = intersection(self.valTracker[key], dictionary.getLetters(category, position))
                    position += 1
                    
                print self.valTracker    
            i += 1
        
        

def letterBacktrack(assignment):
    
    


'''
Word Formulation Problems
'''

class WordCSP:
    
def wordBacktrack(assignement):
    