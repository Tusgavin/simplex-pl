import numpy as np

def pivot(tableau, elementPivotIndexes):
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

def getOptimizationInputValues(numberOfRestrictions):
   c = [int(x) for x in input().split()]

   A = []
   b = []
   
   for _ in range(0, numberOfRestrictions):
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
   ident = np.identity(numberOfRestrictions, dtype=np.float)
   new_vars = np.zeros((numberOfRestrictions), dtype=np.float)

   A_fpi = np.concatenate((A, ident), axis=1)
   c_fpi = np.concatenate((c, new_vars), axis=None)
   b_fpi = np.copy(b)

   return (A_fpi, b_fpi, c_fpi)

def getTableau(A_fpi, b_fpi, c_fpi, numberOfRestrictions, numberOfVariables):
   tableau = np.zeros((numberOfRestrictions + 1, numberOfRestrictions + numberOfVariables + 1))
   veroIdent = np.identity(numberOfRestrictions, dtype=np.float)
   veroTop = np.zeros(numberOfRestrictions)

   vero = np.vstack([veroIdent, veroTop])

   for i in range(0, numberOfRestrictions):
      for j in range(0, numberOfVariables + numberOfRestrictions):
         tableau[i][j] = A_fpi[i][j]

   for i in range(0, numberOfVariables):
      tableau[numberOfRestrictions][i] = c_fpi[i] * (-1)

   for i in range(0, numberOfRestrictions):
      tableau[i][numberOfRestrictions + numberOfVariables] = b_fpi[i]

   tableauWithVero = np.concatenate((vero, tableau), axis=1)

   return tableauWithVero

def findColumnToPivot(tableau, numberOfRestrictions):   
   for i in range(numberOfRestrictions, tableau.shape[1] - 1):
      if tableau[tableau.shape[0] - 1][i] < 0:
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

def checkTableau(tableau, numberOfRestrictions):
   for i in range(numberOfRestrictions, tableau.shape[1] - 1):
      if tableau[tableau.shape[0] - 1][i] < 0:
         return 'not optimal'
   
   return 'optimal'

def getObjectiveValue(tableau):
   return tableau[tableau.shape[0] - 1][tableau.shape[1] - 1]

def getSolution(tableau, type):
   return []

def getCertificate(tableau, type):
   return []

def analyzeTableau(tableau, numberOfRestrictions):
   PLType = checkTableau(tableau, numberOfRestrictions)

   if PLType == 'optimal':
      print('otima')
      objectiveValue = getObjectiveValue(tableau)
      print(objectiveValue)
      solution = getSolution(tableau, 'optimality')
      print(solution)
      certificate = getCertificate(tableau, 'optimality')
      print(certificate)

   elif PLType == 'unfeasible':
      print('inviavel')
      certificate = getCertificate(tableau, 'unfeasibility')
   
   elif PLType == 'limitless':
      print('ilimitada')
      solution = getSolution(tableau, 'limitlessness')
      certificate = getCertificate(tableau, 'limitlessness')

def main():
   numberOfRestrictions, numberOfVariables = [int(x) for x in input().split()]

   (A, b, c) = getOptimizationInputValues(numberOfRestrictions)

   (A_fpi, b_fpi, c_fpi) = getFPIForm(A, b, c, numberOfRestrictions)

   tableau = getTableau(A_fpi, b_fpi, c_fpi, numberOfRestrictions, numberOfVariables)

   iteration = 0

   while 1:
      iteration += 1

      print('>> Iteration: ', iteration);
      print('Tableau: \n', tableau)

      columnToPivot = findColumnToPivot(tableau, numberOfRestrictions)
      if columnToPivot == -1:
         break;

      rowOfElementPivot = findMinimumRatioInColumn(tableau, columnToPivot, numberOfRestrictions)
      if rowOfElementPivot == -1:
         break;

      elementPivotIndexes = (rowOfElementPivot, columnToPivot)

      pivot(tableau, elementPivotIndexes)

   print('>> Término:')
   print('Tableau: \n', tableau)

   analyzeTableau(tableau, numberOfRestrictions)

if __name__ == "__main__":
   main()