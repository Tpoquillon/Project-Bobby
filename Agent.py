#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 08:21:52 2019

@author: tpoquillon
"""

import numpy as np
import Genome
import math as mt
class Agent:
  def __init__(self,x,y,myGenome,grid):#Constructor which takes an existing genome, a grid and a position wanted for the agent on this grid
    self.posX_=x
    self.posY_=y
    self.Genome_= Genome.Genome(myGenome.I_,myGenome.O_)
    self.Genome_.Set_Map(myGenome.Map_)
    self.Environment_=np.matrix.copy(grid)
    self.decision_=[False,False,False]
    self.Alive= True
    self.Double_Jump=False
    
    
    
  def Jump(self):
    if(self.Environment_[self.posY_+1,self.posX_]==1):
      self.Double_Jump=True
    
    if(self.decision_[0] and self.Environment_[self.posY_+1,self.posX_]==1 and self.Environment_[self.posY_-1,self.posX_]!=1):
      self.posY_=self.posY_-1
      return True
    if(self.decision_[0] and self.Double_Jump and self.Environment_[self.posY_-1,self.posX_]!=1): #saute une deuxième fois
      self.posY_=self.posY_-1
      self.Double_Jump=False
      return True
    elif self.decision_[0] and self.Double_Jump: #ne saute pas mais ne tombe pas, consomme de dauble saut
      self.Double_Jump=False
      return True      
  def MvForward(self):
    if(self.decision_[1] and not(self.decision_[2]) and self.Environment_[self.posY_,self.posX_+1]!=1):
      self.posX_=self.posX_+1
      return True
      
  def MvBackward(self):
    if(self.decision_[2] and not(self.decision_[1]) and self.Environment_[self.posY_,self.posX_-1]!=1):
      self.posX_=self.posX_-1
      return True
      
  def Fall(self):
    if(self.Environment_[self.posY_+1,self.posX_]==0):
      self.posY_=self.posY_+1
      if self.posY_==len(self.Environment_[:,0])-2:
        self.Alive=False
      return True
    
  def Make_Decision(self):
    self.decision_ = self.Genome_.Processing (np.concatenate(self.Environment_ [self.posY_-2 : self.posY_+3, self.posX_-2:self.posX_+3]))
  
  def Mutate(self,mute_max,add_conect_prob): #Methode qui permet de muter le génome d'un Agent jusque à mute_max fois, ajoutant des conections ou des gènes
    nb_mut=int(np.random.random()*mute_max) #le nombre de mutation que va subir le génome de l'agent
    for i in range(nb_mut):
      if np.random.random()<add_conect_prob: #construit une conexion avec une probabilité égale à add_conect_prob
        self.Genome_.Add_Random_Connection(int(mt.floor( np.random.random()*2.5-0.5))) #Crée une connexion à une position aléatoire d'une valeur de 1, 0 ou -1 (1/3 de chance pour chaque)
      else: # sinon ajoute ou on suprime une gène .
        if np.random.random()>0.5:
          self.Genome_.Add_Gene()
        else:
          self.Genome_.Remote_Last_Gene()
  
  
    
if __name__ == '__main__':
  mat1=np.zeros((5,5))
  genom1=Genome.Genome(3,10)
  a=0
  b=0
  ag1=Agent(a,b,genom1,mat1)
  mat1[0,0]=3
  print(ag1.posX_==a,ag1.posY_==b,ag1.Genome_==genom1,ag1.Environment_,mat1,ag1.decision_==[0,0,0])
  print(ag1.Genome_)
  print(genom1)
  ag2=Agent(a,b,genom1,mat1)
  print(ag2.Genome_.Map_)
  ag2.Mutate(100,0.95)
  print(ag2.Genome_.Map_)
  print(int(-0.5))
