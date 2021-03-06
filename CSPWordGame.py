'''
Word Puzzles
Ryley Higa, James Jia, Shaksham Saini

'''
import urllib2
from operator import itemgetter, attrgetter

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
    
    def getLetters(self, category, position, otherLetters = (None, None, None)):
        letters = []
        firstLetter = otherLetters[0]
        secondLetter = otherLetters[1]
        thirdLetter = otherLetters[2]
        for word in self.dictionary[category]:
            if ((word[0] == firstLetter or firstLetter == None) and (word[1] == secondLetter or secondLetter == None) and \
                (word[2] == thirdLetter or thirdLetter == None)):
                newLetter = word[position]
                if not newLetter in letters: 
                    letters.append(newLetter)
        return letters
            
    def getWords(self, category = None, otherLetters = (None, None, None)):
        words = []
        firstLetter = otherLetters[0]
        secondLetter = otherLetters[1]
        thirdLetter = otherLetters[2]
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
        self.constraints = {}
        for line in data:
            variableList = []
            if i == 0:
                self.size = int(line)
                for j in range(1,self.size+1):
                    self.valTracker[j] = []
            else:
                labels = line.split(":")
                category = labels[0]
                self.constraints[category] = []
                entries = labels[1].split(",")
                entries[-1] = entries[-1].replace("\r\n","")
                position = 0
                for entry in entries:
                    #constrain possible values
                    key = int(entry)
                    if not self.valTracker[key]: 
                        self.valTracker[key] = dictionary.getLetters(category, position)
                    else:
                        self.valTracker[key] = intersection(self.valTracker[key], dictionary.getLetters(category, position))
                    position += 1
                    
                    variableList.append(key)
                    
                    self.constraints[category].append(int(entry))
            i += 1

class WordCSP:
    def __init__(self, url, dictionary):
        data = urllib2.urlopen(url)
        i = 0
        self.valTracker = {}
        self.constraints = {}
        self.possibleCategories = {} # number of possible word categories at entry
        for line in data:
            variableList = []
            if i == 0:
                self.size = int(line)
                for j in range(1,self.size+1):
                    self.possibleCategories[j] = 0
#                    self.constrainedCategories[j-1] = (0,0)
            else:
                labels = line.split(":")
                category = labels[0]
                self.constraints[category] = []
                entries = labels[1].split(",")
                entries[-1] = entries[-1].replace("\r\n","")
                position = 0
                for entry in entries:
                    #constrain possible values
                    key = int(entry)
                    if not self.possibleCategories[key]:
                        self.possibleCategories[key] = 1
                    else:
                        self.possibleCategories[key] += 1 
#                    if not self.valTracker[key]: 
#                        self.valTracker[key] = dictionary.getWords(category)
#                    else:
#                        self.valTracker[key] = intersection(self.valTracker[key], dictionary.getWords(category))
                    position += 1
                    
                    variableList.append(key)
                    
                    self.constraints[category].append(int(entry))
            i += 1
        
        self.constrainedCategories = [[0,0,{},0] for k in range(i-1)]  # most constrained to least constrained
        i = 0
        
        self.test = 0
        data = urllib2.urlopen(url)
        
        for line in data:
            if i == 0:
                self.test = 1
            else:
                self.test += 1
                labels = line.split(":")
                category = labels[0]
                entries = labels[1].split(",")
                entries[-1] = entries[-1].replace("\r\n","")
                self.constrainedCategories[i-1][0] = category
                self.constrainedCategories[i-1][3] = -len(dictionary.getWords(category))
                for entry in entries:
                    key = int(entry)
                    self.constrainedCategories[i-1][1] += self.possibleCategories[key]
                self.constrainedCategories[i-1][2] = entries
            i += 1

        self.constrainedCategories = sorted(self.constrainedCategories, key=itemgetter(1, 3), reverse=True)
            
