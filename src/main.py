import numpy as np

def pivot(A, b, c, leaving_index, entering_index):
   print(A, b, c, leaving_index, entering_index)

def getOptimizationInputValues(numberOfVariables):
   c = [int(x) for x in input().split()]

   A = []
   b = []
   
   for _ in range(0, numberOfVariables):
      A_i_b = [int(x) for x in input().split()]
      
      b_i = A_i_b[-1]
      del A_i_b[-1]
      
      A.append(A_i_b)
      b.append(b_i)

   A = np.array(A, dtype=np.float)
   b = np.array(b, dtype=np.float)
   c = np.array(c, dtype=np.float)

   return (A, b, c)

def getFPIForm(A, b, c, numberOfRestrictions):
   ident = np.identity(numberOfRestrictions, dtype=np.float);
   new_vars = np.zeros((numberOfRestrictions), dtype=np.float);

   A_fpi = np.concatenate((A, ident), axis=1)
   c_fpi = np.concatenate((c, new_vars), axis=None)
   b_fpi = np.copy(b)

   return (A_fpi, b_fpi, c_fpi)

def getTableau(A_fpi, b_fpi, c_fpi, numberOfRestrictions, numberOfVariables):
   tableau = np.zeros((numberOfRestrictions + 1, numberOfRestrictions + numberOfVariables + 1))

   for i in range(0, numberOfRestrictions):
      for j in range(0, numberOfVariables + numberOfRestrictions):
         tableau[i][j] = A_fpi[i][j]

   for i in range(0, numberOfVariables):
      tableau[numberOfRestrictions][i] = c_fpi[i]

   for i in range(0, numberOfRestrictions):
      tableau[i][numberOfRestrictions + numberOfVariables] = b_fpi[i]

   return tableau

def findColumnToPivot(tableau):   
   for i in range(0, tableau.shape[1] - 1):
      if tableau[tableau.shape[0] - 1][i] > 0:
         return i
   
   return -1

def findMinimumRatioInColumn(tableau, columnIndex, numberOfRestrictions):
   indexOfPivotElement = -1

   for i in range(0, numberOfRestrictions):
      if tableau[i][columnIndex] <= 0:
         continue
      elif indexOfPivotElement == -1:
         indexOfPivotElement = i
      elif (tableau[i][tableau.shape[1] - 1] / tableau[i][columnIndex]) < (tableau[indexOfPivotElement][tableau.shape[1] - 1] / tableau[indexOfPivotElement][columnIndex]):
         indexOfPivotElement = i

   return indexOfPivotElement

def main():
   numberOfRestrictions, numberOfVariables = [int(x) for x in input().split()]

   (A, b, c) = getOptimizationInputValues(numberOfVariables)

   (A_fpi, b_fpi, c_fpi) = getFPIForm(A, b, c, numberOfRestrictions)

   print('# Matriz A em FPI: \n', A_fpi)
   print('# Vetor c em FPI: \n', c_fpi)
   print('# Vetor b em FPI: \n', b_fpi)

   tableau = getTableau(A_fpi, b_fpi, c_fpi, numberOfRestrictions, numberOfVariables)

   print('# Tableau formado: \n', tableau)

   columnToPivot = findColumnToPivot(tableau)
   rowOfElementPivot = findMinimumRatioInColumn(tableau, columnToPivot, numberOfRestrictions)

   elementPivot = (rowOfElementPivot, columnToPivot)

   print('# Indexes of element to pivot (ROW, COLUMN): \n', elementPivot)

   # objective_value = 0
   # iter = 0
   # non_basis_variables_index = [x for x in range(0, numberOfVariables)]
   # basis_variables_index = [x for x in range(numberOfVariables, numberOfVariables + numberOfRestrictions)]

if __name__ == "__main__":
   main()