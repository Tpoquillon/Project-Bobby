#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 14:31:27 2019

@author: tpoquillon
"""
import Agent
import Genome

import Game
filenames=["Grimper2","Reculer2"]

Dict={}
DictM={}
for filename in filenames:
  w=Game.Game()
  w.File_to_map(filename+".txt")
  Dict[filename]=w
  Gsucces=Genome.Genome(25,3)
  Gsucces.SetMap_From_Txt("Bobbies/Bobby67.txt")
  A=Agent.Agent(4,2,Gsucces,Dict[filename].Grid)
  w.AddAgent(A)
  w.Start()
  w.printgridstep()
  
  input("pause")
  w2=Game.Game(L=100,H=40)
  w2.Random_Level_generation(30,400)
  G2=Genome.Genome(25,3)
  G2.SetMap_From_Txt("Bobbies/Bobby122.txt")
  A2=Agent.Agent(4,2,G2,w2.Grid)
  w2.AddAgent(A)
  w2.Start()
  w2.printgridstep()
  input("pause")
  
  w.Pop=[]
  w.File_to_map("Reculer.txt")
  G=Genome.Genome()
  G.SetMap_From_Txt("Bobbies/BobbyTRicheur.txt")
  A2=Agent.Agent(4,2,G,w.Grid)
  w.AddAgent(A2)
  w.Start()
  w.printgridstep()
  input("pause")
  
  w.Pop=[]
  w.File_to_map("PoorBobby.txt")
  G=Genome.Genome()
  G.SetMap_From_Txt("Bobbies/BobbyBete.txt")
  A2=Agent.Agent(4,2,G,w.Grid)
  w.AddAgent(A2)
  w.Start()
  w.printgridstep()
  input("pause")