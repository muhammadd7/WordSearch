# #Character Recognition using python's builtn OCR
# imgn = cv2.imread('E:/CUI data/Semester 6/Digital Image Processing/Project/Final/BoardCells/cell1.jpg')
import pickle
import numpy as np
from skimage.transform import resize
from skimage.feature import hog
import re
import cv2
import os
from tkinter import messagebox
import pandas as pd
import sys 
from tkinter import * 
from tkinter import ttk
import tkinter as tk
from tkinter.constants import LEFT, TOP

numbers = re.compile(r'(\d+)')
def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts
    
myLetters = []
for filename in sorted(os.listdir('BoardCells'), key=numericalSort):
        img = cv2.imread(os.path.join('BoardCells/',filename))
        
        resized_img = resize(img, (16,16)) 
        fd, hog_image = hog(resized_img, pixels_per_cell=(3,3), cells_per_block=(2, 2), visualize=True, multichannel=True)
        
        X = fd
        nX_test = np.delete(X, -1)
        X_test = nX_test.reshape(1,-1)

        pickled_model_svm = pickle.load(open('SVM_Model.pkl', 'rb'))
        predicted_svm = pickled_model_svm.predict(X_test)


        pickled_model_dt = pickle.load(open('DT_Model.pkl', 'rb'))
        predicted_dt = pickled_model_dt.predict(X_test)


        pickled_model_knn = pickle.load(open('KNN_Model.pkl', 'rb'))
        predicted_knn = pickled_model_knn.predict(X_test)

        if ((predicted_svm == predicted_knn) or (predicted_svm == predicted_dt)):
            myLetters.append(predicted_svm)
        elif ((predicted_dt == predicted_knn)):
            myLetters.append(predicted_dt)
        else:
            myLetters.append(predicted_dt)

index = 0
letters = np.zeros(shape=(15, 15), dtype=myLetters[0].dtype)

for i in range(15):
    for j in range(15):
        letters[i,j] = myLetters[index]
        index = index + 1


root = Tk()
			
root.geometry('1000x500')	
root.title("Scramble Puzzle ")
Label(root, text ="Scramble Puzzle Solver", font=150).pack()

class WordSearch(object):
      
      def __init__(self):
        self.word = StringVar()

      def ViewWords(self, letters):
                  
            dframe = pd.DataFrame(letters)

            txt = Text(root) 
            txt.pack() 

            class PrintToTXT(object): 
                  def write(self, s):     
                        txt.insert(END, s)
                  def flush(self):
                        pass
            sys.stdout = PrintToTXT() 

            print ('Characters found in the image are:') 

            print (dframe)

            Label(root, text="Enter Word to Search:").place(x=100, y=500)
            w = Entry(root, textvariable=self.word)
            w.place(x=250, y=500)

            
            submit = Button(root, text = 'Submit', command = lambda: self.FindWords(letters))
            submit.place(x=100,y=550) 

            
      def FindWords(self, letters):
            
            try: 
                  word = self.word.get()
                  self.find_word(letters, word)
            except:
                  print('Word not found')
            
      def find_word (self, wordsearch, word='Abcd'):
            """Trys to find word in wordsearch and prints result"""
            # Store first character positions in array
            print('word is: ', word)
            start_pos = []
            
            first_char = word[0]

            for i in range(0, len(wordsearch)):
                  for j in range(0, len(wordsearch[i])):
                        if (wordsearch[i][j] == first_char):
                              start_pos.append([i,j])
            # Check all starting positions for word
            for p in start_pos:
                  if self.check_start(wordsearch, word, p):
                        # Word found
                        return
            # Word not found
            print('Word Not Found')

      def check_start (self, wordsearch, word, start_pos):
            """Checks if the word starts at the startPos. Returns True if word found"""
            directions = [[-1,1], [0,1], [1,1], [-1,0], [1,0], [-1,-1], [0,-1], [1,-1]]
            # Iterate through all directions and check each for the word
            for d in directions:
                  if (self.check_dir(wordsearch, word, start_pos, d)):
                        return True

      def check_dir (self, wordsearch, word, start_pos, dir):
            """Checks if the word is in a direction dir from the start_pos position in the wordsearch. Returns True and prints result if word found"""
            found_chars = [word[0]] # Characters found in direction. Already found the first character
            current_pos = start_pos # Position we are looking at
            pos = [start_pos] # Positions we have looked at
            while (self.chars_match(found_chars, word)):
                  if (len(found_chars) == len(word)):
                        # If found all characters and all characters found are correct, then word has been found
                        print('')
                        print('Word Found')
                        print('')
                        # Draw wordsearch on command line. Display found characters and '-' everywhere else
                        for x in range(0, len(wordsearch)):
                              line = ""
                              for y in range(0, len(wordsearch[x])):
                                    is_pos = False
                                    for z in pos:
                                          if (z[0] == x) and (z[1] == y):
                                                is_pos = True
                                    if (is_pos):
                                          line = line + " " + wordsearch[x][y]
                                    else:
                                          line = line + " -"
                              print(line)
                        print('')
                        return True;
                  # Have not found enough letters so look at the next one
                  current_pos = [current_pos[0] + dir[0], current_pos[1] + dir[1]]
                  pos.append(current_pos)
                  if (self.is_valid_index(wordsearch, current_pos[0], current_pos[1])):
                        found_chars.append(wordsearch[current_pos[0]][current_pos[1]])
                  else:
                        # Reached edge of wordsearch and not found word
                        return

      def chars_match (self, found, word):
            """Checks if the leters found are the start of the word we are looking for"""
            index = 0
            for i in found:
                  if (i != word[index]):
                        return False
                  index += 1
            return True

      def is_valid_index (self, wordsearch, line_num, col_num):
            """Checks if the provided line number and column number are valid"""
            if ((line_num >= 0) and (line_num < len(wordsearch))):
                  if ((col_num >= 0) and (col_num < len(wordsearch[line_num]))):
                        return True
            return False

a = WordSearch()
a.ViewWords(letters)


root.mainloop()