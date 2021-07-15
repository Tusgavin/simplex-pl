import numpy as np

def pivot(tableau, elementPivotIndexes):
   print('Tableau logo após entrar na função: \n', tableau)

   for i in range(0, tableau.shape[0]):
      for j in range(0, tableau.shape[1]):
         if i != elementPivotIndexes[0] and j != elementPivotIndexes[1]:
            tableau[i][j] -= tableau[elementPivotIndexes[0]][j] * tableau[i][elementPivotIndexes[1]] / tableau[elementPivotIndexes[0]][elementPivotIndexes[1]]

   for i in range(0, tableau.shape[0]):
      if i != elementPivotIndexes[0]:
         tableau[i][elementPivotIndexes[1]] = 0.0
   
   for i in range(0, tableau.shape[1]):
      if i != elementPivotIndexes[1]:
         tableau[elementPivotIndexes[0]][i] /= tableau[elementPivotIndexes[0]][elementPivotIndexes[1]]
   
   tableau[elementPivotIndexes[0]][elementPivotIndexes[1]] = 1.0

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

   iteration = 0

   while 1:
      iteration += 1

      print('>> Iteration: ', iteration);

      columnToPivot = findColumnToPivot(tableau)
      if columnToPivot == -1:
         print('> Tratar quando não haver coluna para pivotear')
         break;

      rowOfElementPivot = findMinimumRatioInColumn(tableau, columnToPivot, numberOfRestrictions)
      if rowOfElementPivot == -1:
         print('> Tratar quando elementos da colunas para pivotear são menores ou iguais a zero')
         break;

      elementPivotIndexes = (rowOfElementPivot, columnToPivot)

      pivot(tableau, elementPivotIndexes)

   print('## Tableau final: \n', tableau)

if __name__ == "__main__":
   main()