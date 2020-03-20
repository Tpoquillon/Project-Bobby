#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 08:20:10 2019

@author: tpoquillon
"""

import numpy as np
import Agent
import Genome
import ViewWorld
import tkinter as tk
import time

class Game:
  
  #CONSTRUCTEUR  
  def __init__(self,H=9,L=100):
    """
    Default Contructor
    
    Parameters
    ----------
    self : class
      Object Game creat here

    H : int
      The heigt of the grid's game
    L : int
      The length of the grid's game
    """
    #Grid
    self.Grid=np.zeros((H,L),dtype=int)#The grid is a table full of zeros (H columns x L rows)
    self.Grid[H-2:H,:]=np.ones((2,L),dtype=int)#The grid has the 2 lines at the bottom full of ones (the floor)
    self.Grid[0:2,:]=np.ones((2,L),dtype=int)#The grid has the 2 lines at the top full of ones (the ceil)
    self.Grid[:,0:2]=np.ones((H,2),dtype=int)#The grid has the 2 columns at the lest full of ones (the left wall)
    self.Grid[:,L-2:L]=np.ones((H,2),dtype=int)#The grid has the 2 columns at the right full of ones (the right wall)
    #Pop
    self.Pop=[]#Pop is a list containing all the different agents : the population
    #Time
    self.Time=0#Time is counting how many time the agents have been run.
    #World
    self.lenth=L
    self.hight=H

  #AFFICHAGE  
  def initdraw(self):
    """
    Generate a game area
    
    Parameters
    ----------
    self : class
      Object Game
    """
    self.World=ViewWorld.CreateWorld()
    self.World.pack(padx=000,pady=000)
    self.B = tk.Button(master=self.World.frame, text="Run Bobby, RUUUN !", bg='yellow', fg='red', width=25, height = 5, command=lambda:self.run()).pack(side=tk.LEFT)
  
  def printgridstep(self):
    """
    Print the game area
    
    Parameters
    ----------
    self : class
      Object Game
    """
    self.initdraw()
    self.World.draw_grid(self.Grid)
    
  #TERRAIN  
  def MakePit(self,x): 
    """
    Creat a hole a the x position
    
    Parameters
    ----------
    self : class
      Object Game

    x : int
      The position where the hole is creat
    """
    self.Grid[2:,x]=np.zeros((len(self.Grid[2:,x])),dtype=int)

  def AddBlockStratum(self,xl,xr): #Ajoute une strate de bloques entre xl et xr
    """
    Add a layer of blocks between the position x1 and xr
    
    Parameters
    ----------
    self : class
      Object Game

    xl : int
      The start position of the layer

    xr : int
      The end position of the layer
    """
    H=len(self.Grid)
    for col in range(xl,xr+1):
      i=4
      while i<H and self.Grid[i][col]!=1:
        i+=1
      if i!=0 and i!=H:
        self.Grid[i-1][col]=1
        
  def Random_Level_generation(self,nbPit,nblayer):
    """
    Generate a random level with a nbPit hole and a nblayer layer
    
    Parameters
    ----------
    self : class
      Object Game

    nbPit : int
      The number of hole on the board

    nblayer : int
      The number of layer on the board
    """
    for i in range(nbPit):
      x=int(np.random.random()*(len(self.Grid[0,:])-5)+2)
      if self.Grid[len(self.Grid)-1,x-1]!=0 or self.Grid[len(self.Grid)-1,x+1]!=0:
        self.MakePit(x)
    dicti={}
    for i in range(nblayer):
      xl=int(np.random.random()*(len(self.Grid[0,:])-5)+2)
      xr=xl+int(np.random.random()*8)+1
      if self.Grid[len(self.Grid)-1,xl]!=0 and self.Grid[len(self.Grid)-1,xl-1]!=0 and xr<len(self.Grid[0,:])-2 and (xl not in dicti or dicti[xl]==1):
        self.AddBlockStratum(xl,xr)
        if xl in dicti:
          dicti[xl]=2
        if xl not in dicti:
          dicti[xl]=1
        
    return True
  
  
  def File_to_map(self,s):
    """
    Load a map from a text file (.txt)
    
    Parameters
    ----------
    self : class
      Object Game

    s : str
      the file name where the map is located
    """  
    self.Grid=np.loadtxt(s)
    self.lenth=len(self.Grid[0,:])
    self.hight=len(self.Grid[:,0])
    for agent in self.Pop:
      agent.Environment_=self.Grid
      
  #POPULATION
  def AddAgent(self,agent):
    """
    Add an agent at the population
    
    Parameters
    ----------
    self : class
      Object Game

    agent : class
      Object Agent, an individual who will try the map
    """
    self.Pop.append(agent)  
    agent.Environment_=self.Grid
    
  def SortByFitness(self):
    """
    Sort descending the population of individual depending the fitness, from the best to the worst
    
    Parameters
    ----------
    self : class
      Object Game
    """
    for agent in self.Pop:
      if not agent.Alive:
        agent.posX_=-100 #
    i = len(self.Pop)-1 #si les agent sont mort on set leurs posx (fitness) à -1
    while i!=0 : #algorithme de tri en fonction de posX_
      for j in range(i):
        if self.Pop[j].posX_-1*self.Pop[j].posY_<self.Pop[j+1].posX_-1*self.Pop[j+1].posY_:
          inter=self.Pop[j]
          self.Pop[j]=self.Pop[j+1]
          self.Pop[j+1]=inter   
      i=i-1

  def New_Generation(self,Methode=0,Indiv=50,Mute=10):
    """
    Create a new generation of individual from the descending sort population.
    Two methode are possible :
      - Methode 0 : only the best individual can have children, it is him genome who is mutate
      - Methode 1 : the 50% best individuals have children by mutation of them genome
    By default the choosen methode is the methode 0

    Parameters
    ----------
    self : class
      Object Game

    Methode : int
      The methode choose for the generation of indivual, can take the values 0 or 1, by default methode select is 0

    Indiv : int
      Number of individual at the new generation, by default 50

    Mute : int
      Number of mutation by genome desire, by default 10
    """    
    if Methode==0:
      Father=self.Pop[0]
      self.Pop=[]
      self.AddAgent(Father)
      for i in range(0,Indiv):
        G=Genome.Genome(25,3)
        G.Set_Map(self.Pop[0].Genome_.Map_[:,:])
        A=Agent.Agent(self.Pop[0].posX_,self.Pop[0].posY_,G,self.Grid)
        A.Mutate(Mute,0.95)
        self.AddAgent(A)
    if Methode==1:
      j=0
      PopBis=[]
      for agent in self.Pop:#chaque agent peut se reproduire dans la limite des places disponible. Les plus performent se reproduiront en premier
        if j<Indiv:
          PopBis.append(agent)
          j+=1
          if j<Indiv:
            G=Genome.Genome(25,3)
            G.Set_Map(agent.Genome_.Map_[:,:])
            A=Agent.Agent(agent.posX_,agent.posY_,G,self.Grid)
            A.Mutate(Mute,0.95)
            PopBis.append(A)
            j+=1
        else:
          break
      self.Pop=PopBis
    
  def Start(self):
    """
    Set up the begin of the game by positionning the individuals on the game area

    Parameters
    ----------
    self : class
      Object Game
    """
    self.Time=0
    for agent in self.Pop:
      agent.Alive=True
      agent.posX_=2
      agent.posY_=self.hight-5
      if agent.Genome_.H_!=0:
        agent.Genome_.Hidden_=np.zeros((1,agent.Genome_.H_))

#JEU
  def run(self):
    """
    Run the game, move all the individual once and print them

    Parameters
    ----------
    self : class
      Object Game
    """      
    self.Time+=1
      for Ag in self.Pop:
        if Ag.Alive:
          self.Grid[Ag.posY_,Ag.posX_]=0
          Ag.Make_Decision()
          if(not(Ag.Jump())):
            Ag.Fall()
          Ag.MvForward()
          Ag.MvBackward()
      for Ag in self.Pop:
        if Ag.Alive:
          self.Grid[Ag.posY_,Ag.posX_]=2
      self.World.draw_grid(self.Grid)
      for Ag in self.Pop:
        if Ag.Alive:
          self.Grid[Ag.posY_,Ag.posX_]=0
        
  def RunBlind(self): #run sans affichage
    """
    Run the game, move all the individual once whitout print them
    
    Parameters
    ----------
    self : class
      Object Game
    """
    self.Time+=1
    for Ag in self.Pop:
      if Ag.Alive:
        Ag.Make_Decision()
        if(not(Ag.Jump())):
          Ag.Fall()
        Ag.MvForward()
        Ag.MvBackward()
        
  def PopTest(self):
    """
    Check if the time is inferior to 2*length of the game area
    Check if some individual just make round trip without progress in the game area
    
    Parameters
    ----------
    self : class
      Object Game
    """
    while self.Time<2*self.lenth:
      self.RunBlind()
    self.Time=0
    for Ag in self.Pop: #élimination des individus tricheurs
        for i in range(5):
          if Ag.Alive:
            Ag.Fall()    

    

#EVOLUTION
  def FindBestAgent(self):
    """
    Find the best agent, the individual who arrived first
    
    Parameters
    ----------
    self : class
      Object Game
    """    
    best=0
    x=0
    for agent in range(len(self.Pop)):#finds a better one if it exists
      if(self.Pop[agent].Alive and self.Pop[agent].posX_>x):
        best=agent
        x=self.Pop[agent].posX_
    return [best,x]
  

  def EvolveByDivision(self,IndivMax,MutationsRate,Generation=500):
    """
    Calculate the time to solve the game
    Each individual can have children (if population is not full) but the individual with the best fitness begin
    
    Parameters
    ----------
    self : class
      Object Game
    IndivMax : int
      Maximal number of individual in the population
    MutatopnsRate : int
      Number of mutation
    Generation : int
      Number of generation create, by default equal to 500

    Returns
    -------
    int
      time made by a individual in the population after several mutation to complite the game
    """
    t=time.time()
    end=False;
    for i in range(Generation):
      self.PopTest()#fait résoudre le circuit à l'ensemble de la population
      self.SortByFitness()# tris les individus par fitness dans l'ordre décroissant
      if (self.Pop[0].posX_==len(self.Grid[0,:])-3):# verifie quaucun individu n'a complètement résolut le circuit
        end=True
      j=0
      PopBis=[]
      for agent in self.Pop:#chaque agent peut se reproduire dans la limite des places disponible. Les plus performent se reproduiront en premier
        if j<IndivMax:
          agent.posX_=4
          agent.posy_=2
          #agent.Mutate(MutationsRate,1)
          PopBis.append(agent)
          j+=1
          if j<IndivMax:
            G=Genome.Genome(25,3)
            """Add an agent to the list Pop"""
            G.Set_Map(agent.Genome_.Map_[:,:])
            A=Agent.Agent(4,2,G,self.Grid)
            A.Mutate(MutationsRate,1)
            PopBis.append(A)
            j+=1
      self.Pop=PopBis
      if end:
        return time.time()-t
    return time.time()-t

  def Evolve(self,Children,MutationsRate,Generation=500):
    """
    Calculate the time to solve the game
    Only the individual with the best fitness have child

    Parameters
    ----------
    self : class
      Object Game
    Children : int
      Number of children of the best individual
    MutatopnsRate : int
      Number of mutation
    Generation : int
      Number of generation create, by default equal to 500

    Returns
    -------
    int
      time made by a individual in the population after several mutation to complite the game
    """
    t=time.time()
    end=False
    for i in range(Generation):
      self.PopTest()
      Father=self.Pop[self.FindBestAgent()[0]]
      if (Father.posX_==len(self.Grid[0,:])-3):
        end=True 
      self.Pop=[]
      for j in range(Children):
        G=Genome.Genome(25,3)
        G.Set_Map(Father.Genome_.Map_[:,:])
        A=Agent.Agent(4,2,G,self.Grid)
        if j!=0:
          A.Mutate(MutationsRate,1)
        self.AddAgent(A)
      if end:
        return time.time()-t
    return time.time()-t

  def Evolution(self,Methode=0,Indiv=50,Mute=10,timeMax=10):#méthode d'évolution généralisée
    """
    Calculate the time to solve the game
    Two methode of children are possible :
      - Methode 0 : only the best individual can have children, it is him genome who is mutate
      - Methode 1 : the 50% best individuals have children by mutation of them genome

    Parameters
    ----------
    self : class
      Object Game
    Methode : int
      The methode choose for the generation of indivual, can take the values 0 or 1, by default methode select is 0
    Indiv : int
      The number of individual in the new population, by default equal to 50
    Mute : int
      Number of mutation, by default equal to 10
    timeMax : int
      Maximal time, if the game is not solve stop the function, by default equal to 10

    Returns
    -------
    int
      time made by a individual in the population after several mutation to complite the game
    int
      number of generation create to solve the game
    """  
    t=time.time()
    Finished=False
    generation=0
    while time.time()-t<timeMax and not Finished:
      self.Start()
      self.PopTest()
      self.SortByFitness()
      if self.Pop[0].posX_ == self.lenth-3:
        Finished=True
      else:
        self.New_Generation(Methode,Indiv,Mute)
        generation+=1
    return (time.time()-t,generation)

if __name__ == '__main__':  
  w1=Game(L=100,H=40)
  w1.Random_Level_generation(30,400)
  Galea=Genome.Genome(25,3)
  
  A1=Agent.Agent(4,2,Galea,w1.Grid)
  w1.AddAgent(A1)
  for i in range(2,61):
    w1.Pop[0].Genome_.SetMap_From_Txt("Bobbies/Bobby"+str(i)+".txt")
    w1.Start()
    w1.PopTest()
    if (w1.Pop[0].posX_==w1.lenth-3):
      print("Bobby"+str(i)+".txt is successfull")
