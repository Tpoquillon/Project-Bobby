#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 08:23:06 2019

@author: tpoquillon
"""
import numpy as np

class Genome:
  def __init__(self,I=25,O=3):  #Default Contructor
    
    self.O_=O  #range of the Output vector
    
    self.I_=I  #range of the Input vector
    
    self.H_=0  #range of the Hidden vector
    
    self.Hidden_=np.array([])  #Hidden vector
    
    self.Map_=np.zeros((I,O))  #Conection Matrix
    
  def Copy_Genom(self,model):  #modify the current genom to be a copy of the Genom ojevt "model"
    
    self.O_=model.O_  
    
    self.I_=model.I_  
    
    self.H_=model.H_ 
    
    self.Hidden_=model.Hidden_[:]  
    
    self.Map_=np.copy(model.Map_) 



  def Set_Map(self,Matrix):  #Matrix Setter by copy
    self.H_=len(Matrix)-self.I_
    self.Hidden_=np.zeros((1,self.H_))
    self.Map_=np.matrix.copy(Matrix)

  def Processing(self,Input):  #Product vector of decision based on a vector of actions passed as a parameter
    Out=(np.concatenate((Input,self.Hidden_),axis=None).dot(self.Map_))>0  
    self.Hidden_=1*Out[self.O_:self.O_+self.H_]
    return Out[0:self.O_]

  def Add_Gene(self):#This methode add a new gene, an intermediary hiden node between the input and the output. It improve the lenght of Hiden and H by one
    self.H_+=1
    self.Hidden_=np.zeros((1,self.H_))
    M=np.zeros((self.I_+self.H_,self.O_+self.H_))
    M[0:self.I_+self.H_-1,0:self.O_+self.H_-1]=self.Map_
    self.Map_=M
    
  def Remote_Last_Gene(self):#enlève le dernier gène, diminue la taille du génome de 1
    if self.H_!=0:
      self.H_=self.H_-1
      self.Hidden_=np.zeros((1,self.H_))
      M=np.zeros((self.I_+self.H_,self.O_+self.H_))
      M=self.Map_[0:self.I_+self.H_,0:self.O_+self.H_]
      self.Map_=M   
    
  def Add_Genes(self, Number_Of_Genes):# add a selected number of genes
    for i in range(Number_Of_Genes):
      self.Add_Gene() 
      
      
  
  def Add_Connection(self,Source,Target,Value=1): # Add a connection of a chosen value in the chosen position in the Connections Matrix 
    self.Map_[Source,Target]=Value
    
  def Add_Random_Connection(self,Value=1):
    self.Add_Connection(int(np.random.random()*(self.H_+self.I_)),int(np.random.random()*(self.H_+self.O_)),Value) # Add a connection of a chosen value in a random position in the Connections Matrix 
   
  def SetMap_From_Txt(self,namefile):#retrieves a matrix in a txt file and atrributes it to the Map_ attribute of the current Genom object
   self.Set_Map(np.loadtxt(namefile))
    
  def PutMap_Into_Txt(self, namefile):#retrieves the Map_ of the current Genom object and writes it into a file txt
   namefile=namefile+".txt"
   np.savetxt(namefile, self.Map_, fmt='%d')
    
    
if __name__ == '__main__':
  print("1: Constructor test")
  gm1=Genome(3,10)
  print(gm1.Map_==np.zeros((3,10)), gm1.O_==10, gm1.I_==3,gm1.H_==0, gm1.Hidden_==np.array([]))
  print("2: Set_Map test")
  gm2=Genome(2,2)
  gm2.Set_Map(np.array([[1, 2], [3, 4]]))
  print(gm2.Map_==np.array([[1, 2], [3, 4]]))
  print("3: Processing test")
  gm3=Genome(2,4)
  gm3.Set_Map(np.array([[0,1,0,1],[1,0,1,0]]))
  print(gm3.Processing(np.array([0,1]))==np.array([True,False,True,False]))
  print(gm3.Processing(np.array([1,0]))==np.array([False,True,False,True]))
  
  print("4: Copy_Genom test")
  gm4=Genome(14,12)
  gm4.Copy_Genom(gm3)
  gm4.Set_Map(np.array([[1, 2], [3, 4]]))
  print(gm4.Map_)
  print(gm3.Map_)
  print(gm4.Processing(np.array([0,1]))==np.array([True,False]))
  print(gm4.Processing(np.array([1,0]))==np.array([False,True]))
  
  print("5: Add_Gene test")
  gm5=Genome(2,4)
  gm5.Add_Gene()
  print(gm5.H_==1,gm5.Hidden_==np.array([0]))
  print("6: Add_Genes test")
  gm6=Genome(2,4)
  gm6.Set_Map(np.array([[0,1,0,1],[1,0,1,0]]))
  gm6.Add_Genes(3)
  print(gm6.H_==3,gm5.Hidden_==np.zeros(3),gm6.O_==4,gm6.I_==2)
  print(gm6.Map_==np.array([[0,1,0,1,0,0,0],[1,0,1,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]]))
  print("7: Add_Connection test")
  gm7=Genome(2,4)
  gm7.Add_Connection(0,3,-8)
  print(gm7.Map_[0,3]==-8)
  print("8: Add_Random_Connection test")
  gm8=Genome(1,4)
  gm8.Add_Random_Connection()
  for i in range(4):
    if gm8.Map_[0,i]==1:
      print(True)
  gm8.Add_Random_Connection(-2.5)
  for i in range(4):
    if gm8.Map_[0,i]==-2.5:
      print(True)
      
  print("9: PutMap_Into_Txt and test")
  gm6.PutMap_Into_Txt("testgm6")
  print("done")
  gm9=Genome(2,4)
  gm9.SetMap_From_Txt("testgm6.txt")

   
   
