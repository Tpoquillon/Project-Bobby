#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 14:33:33 2019

@author: tpoquillon
"""
import Agent
import Genome
import Game
import time
import math

w=Game.Game()
w.File_to_map("Sauter.txt")
G=Genome.Genome(25,3)
G.SetMap_From_Txt("Bobby")
A=Agent.Agent(4,4,G,w.Grid)
w.AddAgent(A)
w.printgridstep()
input('Print enter to continue')


