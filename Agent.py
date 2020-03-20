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
  def __init__(self,x,y,myGenome,grid):#Constructor which takes an existing genome, a grid and a position wanted for the Agent on this grid
    """
    Default Contructor
    
    Parameters
    ----------
    self : class
      Object Agent created here
    x : int
      the x position of the Agent on the Environment_
    y : int
      the y position of the Agent on the Environment_
    myGenome : Genome
      the Genome of the Agent
    grid : numpy.ndarray
      the Environment_ of the Agent
      

    """
    self.posX_=x
    self.posY_=y
    self.Genome_= Genome.Genome(myGenome.I_,myGenome.O_)
    self.Genome_.Set_Map(myGenome.Map_)
    self.Environment_=np.matrix.copy(grid)
    self.decision_=[False,False,False]
    self.Alive= True
    self.Double_Jump=False
    
    

  def Jump(self):
    """
    Jump methode, that looks if the Agent wants to jump and if it can.
    If so, it then performs the action by changing its positions
    
    Parameters
    ----------
    self : class
    the Agent
    
    Return
    ----------
    True if the Agent performed the action
    
    """
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
    """
    MvForward methode, that looks if the Agent wants to moove forward and if it
    can.
    If so, it performs the action by changing its positions
    
    Parameters
    ----------
    self : class
    the Agent
    
    Return
    ----------
    True if the Agent performed the action
    
    """
    
    if(self.decision_[1] and not(self.decision_[2]) and self.Environment_[self.posY_,self.posX_+1]!=1):
      self.posX_=self.posX_+1
      return True
      
  def MvBackward(self):
    """
    MvBackward methode, that looks if the Agent wants to moove backward and if
    it can.
    If so, it performs the action by changing its positions
    
    Parameters
    ----------
    self : class
    the Agent
    
    Return
    ----------
    True if the Agent performed the action
    
    """
    if(self.decision_[2] and not(self.decision_[1]) and self.Environment_[self.posY_,self.posX_-1]!=1):
      self.posX_=self.posX_-1
      return True
      
  def Fall(self):
    """
    Fall methode, that looks if the Agent shall fell
    If so, it makes it fall by changing its positions
    
    Parameters
    ----------
    self : class
    the Agent
    
    Return
    ----------
    True if the Agent performed the action
    """
    if(self.Environment_[self.posY_+1,self.posX_]==0):
      self.posY_=self.posY_+1
      if self.posY_==len(self.Environment_[:,0])-2:
        self.Alive=False
      return True
    
  def Make_Decision(self):
    """
    Make_Decision methode, that uses the Agent Environment_ and Genome_ to updat
    its decision_. See Genome.Processing
    
    Parameters
    ----------
    self : class
    the Agent
    
    Return
    ----------
    None
    """
    self.decision_ = self.Genome_.Processing (np.concatenate(self.Environment_ [self.posY_-2 : self.posY_+3, self.posX_-2:self.posX_+3]))
  
  def Mutate(self,mute_max,add_conect_prob): #Methode qui permet de muter le génome d'un Agent jusque à mute_max fois, ajoutant des conections ou des gènes
    """
    Randomly mutate the Agent Genome_. 
    See Genome.Add_Random_Connection , Genome.Add_Gene 
    and Genome.Remote_Last_Gene
    
    Parameters
    ----------
    self : class
    the Agent
    
    mute_max : int
    max number of mutations
    
    add_conect_prob : float
    the probability of adding a new gene in the Genome_ instead of modifying an
    already existant one during a mutation.
    
    Return
    ----------
    None
    """
    nb_mut=int(np.random.random()*mute_max) #le nombre de mutation que va subir le génome de l'Agent
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
