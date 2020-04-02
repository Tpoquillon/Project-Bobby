#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 08:23:06 2019

@author: tpoquillon
"""
import numpy as np

class Genome:
  """
  Attributes
    ----------
    O_ : int 
      the range of the output vector
    I_ : int 
      the range of the input vector
    H_ : int
      the range of the hidden vector
    Hidden_ : np_Array
      the hidden boolean vector describing the state of each hidden node.
      1 is active and 0 is inactive
    Map_ : np_Array
      the conection matrice linking the input , output  and hidden vector.
      this is the brain of our AI
      
    Methodes
    --------   
    Copy_Genome(model)
      Modifies the current genom to be a copy of the Genom oject "model"
    Set_Map(Matrix)
      Matrix Setter by copy of an np_Array
    Processing (input)
      Product decision vector (output vector) based on a its state 
      (hidden vector) and environment (input vector) with the connection 
      matrix
    Add_Gene()
      This method adds a new gene, an intermediary hidden node between the 
      input and the output. It increases the lenght of Hidden and H by one   
    Remote_Last_Gene()
      Removes the last gene and reduces the genome's length by 1
    Add_Genes(N)
      Adds a selected (N) number of genes
    Add_Connection(i,j,v)
      Adds a connection (directed edge ij) of a chosen value v in the chosen 
      position in the Connections Matrix (Map_)
    Add_Random_Connection(v)
      Adds a connection between to random nodes
    SetMap_From_Txt(textfilename)
      Matrix Setter by copy of a text file
    PutMap_Into_Txt(txtfilename)
      Saves the Genom's map in a text file 
  """
  
  
  def __init__(self,I=25,O=3):  
    """
    Default Contructor
    
    Parameters
    ----------
    self : class
      Object Genome created here

    I : int
      The length of the input vector
    O : int
      The length of the output vector, a list of int
      
    Examples
    --------
    >>> import import numpy as np
    >>> gm=Genome(3,4)
    >>> gm=Genome(3,10)
    >>> gm.Map_
    array([[0., 0., 0., 0.],
       [0., 0., 0., 0.],
       [0., 0., 0., 0.]])
    >>> gm.O_
    4
    >>> gm.I_
    3
    >>> gm.H_
    0
    >>> gm.Hidden_
    array([], dtype=float64)
  
    

    
    
    """
    self.O_=O  #range of the Output vector
    
    self.I_=I  #range of the Input vector
    
    self.H_=0  #range of the Hidden vector
    
    self.Hidden_=np.array([])  #Hidden vector
    
    self.Map_=np.zeros((I,O))  #Conection Matrix
    
  def Copy_Genom(self,model):
    """
    Modifies the current genom to be a copy of the Genom object "model"

    Parameters
    ----------
    self : class
      Object Genome that is created
    model : class
      Object Genome to copy

    Examples
    --------
    >>>import import numpy as np
    >>>gm3=Genome(3,2)
    >>>gm4.Copy_Genom(gm3)
    >>> gm4.Map_
    array([[0., 0., 0., 0.],
       [0., 0., 0., 0.],
       [0., 0., 0., 0.]])
    >>> gm4.O_
    4
    >>> gm4.I_
    3
    >>> gm4.H_
    0
    >>> gm4.Hidden_
    array([], dtype=float64)
    
    """    
    self.O_=model.O_  
    
    self.I_=model.I_  
    
    self.H_=model.H_ 
    
    self.Hidden_=model.Hidden_[:]  
    
    self.Map_=np.copy(model.Map_) 



  def Set_Map(self,Matrix):
    """
    Matrix Setter by copy
    
    Parameters
    ----------
    self : class
      Object Genome
    Matrix : np_Array
      The matrix of conecion
      
    Examples
    --------
    >>>import import numpy as np
    >>>gm2=Genome(2,2)
    >>>gm2.Set_Map(np.array([[1, 2], [3, 4]]))
    >>>gm2.Map_
    np.array([[1, 2], [3, 4]])

    """
    self.H_=len(Matrix)-self.I_
    self.Hidden_=np.zeros((1,self.H_))
    self.Map_=np.matrix.copy(Matrix)

  def Processing(self,Input):
    """
    Product decision vector (output vector) based on a its state 
    (hidden vector) and environment (input vector) with the connection 
    matrix
    
    Parameters
    ----------
    self : class
      Object Genome
    Input : np_Array
      A vector describing the environment

    Returns
    --------
    np_Array
      a list of decision (output vector)
    
    Examples
    --------
    >>>import import numpy as np
    >>>gm3=Genome(2,4)
    >>>gm3.Set_Map(np.array([[0,1,0,1],[1,0,1,0]]))
    >>>gm3.Processing(np.array([0,1]))
    np.array([True,False,True,False])
    """
    Out=(np.concatenate((Input,self.Hidden_),axis=None).dot(self.Map_))>0  
    self.Hidden_=1*Out[self.O_:self.O_+self.H_]
    return Out[0:self.O_]

  def Add_Gene(self):
    """
    This method adds a new gene, an intermediary hidden node between the input 
    and the output. 
    It increases the lenght of Hidden and H by one

    Parameters
    ----------
    self : class
      Object Genome
    
    Examples
    --------
    >>>import import numpy as np
    >>>gm5=Genome(2,4)
    >>>gm5.Add_Gene()
    >>>gm5.H_
    1
    >>>gm5.Hidden_
    np.array([0])
    """

    self.H_+=1
    self.Hidden_=np.zeros((1,self.H_))
    M=np.zeros((self.I_+self.H_,self.O_+self.H_))
    M[0:self.I_+self.H_-1,0:self.O_+self.H_-1]=self.Map_
    self.Map_=M
    
  def Remote_Last_Gene(self):
    """
    Removes the last gene and reduces the genome's length by 1

    Parameters
    ----------
    self : class
      Object Genome
    
    Examples
    --------
    >>>import import numpy as np
    >>>gm5=Genome(2,4)
    >>>gm5.Add_Gene()
    >>>gm5.Add_Gene()
    >>>gm5.Remote_Last_Gene()
    >>>gm5.H_
    1
    >>>gm5.Hidden_
    np.array([0])
    """
    if self.H_!=0:
      self.H_=self.H_-1
      self.Hidden_=np.zeros((1,self.H_))
      M=np.zeros((self.I_+self.H_,self.O_+self.H_))
      M=self.Map_[0:self.I_+self.H_,0:self.O_+self.H_]
      self.Map_=M   
    
  def Add_Genes(self, Number_Of_Genes):
    """
    Adds a selected number of genes
    
    Parameters
    ----------
    self : class
      Object Genome

    Number_Of_Genes : int
      The number of gene to insert in the Genome
    
    Examples
    --------
    >>>import import numpy as np
    >>>gm6=Genome(2,4)
    >>>gm6.Set_Map(np.array([[0,1,0,1],[1,0,1,0]]))
    >>>gm6.Add_Genes(3)
    >>>gm6.H_
    3
    >>>gm5.Hidden_
    np.array([[0,0,0],[0,0,0],[0,0,0]])
    >>>gm6.O_
    4
    >>>gm6.I_
    2
    >>>gm6.Map_
    np.array([[0,1,0,1,0,0,0],[1,0,1,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]])
    """

    for i in range(Number_Of_Genes):
      self.Add_Gene() 
      
  def Add_Connection(self,Source,Target,Value=1):
    """
    Adds a connection (directed edge) of a chosen value in the chosen position 
    in the Connections Matrix (Map_)
    
    Parameters
    ----------
    self : class
      Object Genome

    Source : int
      row position in Map_, the beginning of the edge connection

    Target : int
      column position in Map_, the end of the  edge connection

    Value : int
      the weight of the edge connection. By default, equal to 1
    
    Examples
    --------
    >>>import import numpy as np
    >>>gm7=Genome(2,4)
    >>>gm7.Add_Connection(0,3,-8)
    >>>gm7.Map_[0,3]
    -8
    """
    self.Map_[Source,Target]=Value
    
  def Add_Random_Connection(self,Value=1):
    """
    Add a connection at a random position in Map_ for a choosen value

    Parameters
    ----------
    self : class
      Object Genome
    Value : int
      the weight of the edge connection. By default, equal to 1
      
    Examples
    --------
    >>>import import numpy as np
    >>>gm8=Genome(1,4)
    >>>gm8.Add_Random_Connection()
    >>>for i in range(4):
    ... if gm8.Map_[0,i]==1:
    ...   print(True)
    True
    >>>gm8.Add_Random_Connection(-2.5)
    >>>for i in range(4):
    ... if gm8.Map_[0,i]==-2.5:
    ...   print(True)
    True
   
    """
    self.Add_Connection(int(np.random.random()*(self.H_+self.I_)),int(np.random.random()*(self.H_+self.O_)),Value) # Add a connection of a chosen value in a random position in the Connections Matrix 
   
  def SetMap_From_Txt(self,namefile):
    """
    Retrieves a matrix in a txt file and atrributes it to 
    the Map_ attribute of the current Genome object
  
    Parameters
    ----------
    self : class
      Object Genome
    
    namefile : str
      The name of the file which contains the Matrix
    """
    self.Set_Map(np.loadtxt(namefile))
    
  def PutMap_Into_Txt(self, namefile):
    """
    Retrieves the Map_ of the current Genome object and writes it into a file txt
  
    Parameters
    ----------
    self : class
      Object Genome
    namefile : str
      The name of the file which will be created and stock the Matrix
    """
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

   
   
