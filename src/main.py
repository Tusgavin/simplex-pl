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

   # print(tableau)

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

def getAuxFPIForm(A, b, c, numberOfRestrictions):
   ident = np.identity(numberOfRestrictions, dtype=np.float)
   new_vars = np.zeros((numberOfRestrictions), dtype=np.float)
   zero_c = np.zeros((c.shape[0]), dtype=np.float)

   for i in range(0, numberOfRestrictions):
      new_vars[i] = 1

   negative_b_indexes = []

   b_fpi_aux = np.copy(b)

   for i in range(0, b.shape[0]):
      if b[i] <= 0:
         negative_b_indexes.append(i)
         b_fpi_aux[i] = b[i] * (-1)

   A_fpi_aux = np.concatenate((A, ident), axis=1)

   for i in range(0, numberOfRestrictions):
      if i in negative_b_indexes:
         A_fpi_aux[i,:] = A_fpi_aux[i,:] * (-1)

   c_fpi_aux = np.concatenate((zero_c, new_vars), axis=None)

   return (A_fpi_aux, b_fpi_aux, c_fpi_aux, negative_b_indexes)

def getTableau(A_fpi, b_fpi, c_fpi, numberOfRestrictions, numberOfVariables, aux=False, negative_b_indexes=[]):
   tableau = np.zeros((numberOfRestrictions + 1, 2*numberOfRestrictions + numberOfVariables + 1))
   veroIdent = np.identity(numberOfRestrictions, dtype=np.float)
   veroTop = np.zeros(numberOfRestrictions)

   vero = np.vstack([veroIdent, veroTop])

   if len(negative_b_indexes) != 0:
      for i in range(numberOfRestrictions):
         if i in negative_b_indexes:
            vero[i,:] = vero[i,:] * (-1)

   for i in range(0, A_fpi.shape[0]):
      for j in range(0, A_fpi.shape[1]):
         tableau[i][j] = A_fpi[i][j]

   if aux:
      for i in range(0, c_fpi.shape[0]):
         tableau[numberOfRestrictions][i] = c_fpi[i]
   else:
      for i in range(0, numberOfVariables):
         tableau[numberOfRestrictions][i] = c_fpi[i] * (-1)

   if aux:
      for i in range(0, numberOfRestrictions):
         tableau[i][2*numberOfRestrictions + numberOfVariables] = b_fpi[i]
   else:
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
   indexC = findColumnToPivot(tableau, numberOfRestrictions)
   if indexC == -1:
      return "optimal"
   else:
      indexP = findMinimumRatioInColumn(tableau, indexC, numberOfRestrictions)
      if indexP == -1:
         return "limitless"

def getObjectiveValue(tableau):
   return tableau[tableau.shape[0] - 1][tableau.shape[1] - 1]

def getSolution(tableau, numberOfRestrictions, numberOfVariables):
   solution = []

   # if aux:
   #    for i in range(numberOfRestrictions, tableau.shape[1] - 1):
   #       if tableau[tableau.shape[0] - 1][i] == 0:
   #          index = np.where(tableau[:, i] == 1)
   #          if len(index[0]) == 1:
   #             solution.append(tableau[index[0][0]][tableau.shape[1] - 1])
   #          else:
   #             solution.append(0)
   #       else:
   #          solution.append(0)
   # else:
   for i in range(numberOfRestrictions, numberOfRestrictions + numberOfVariables):
      if tableau[tableau.shape[0] - 1][i] == 0:
         index = np.where(tableau[:, i] == 1)
         if len(index[0]) == 1:
            solution.append(tableau[index[0][0]][tableau.shape[1] - 1])
         else:
            solution.append(0)
      else:
         solution.append(0)

   return np.array(solution)

def getCertificate(tableau, type, numberOfRestrictions):
   certificate = []

   if type == 'optimal':
      for i in range(0, numberOfRestrictions):
         certificate.append(tableau[tableau.shape[0] - 1][i])

   return np.array(certificate)

def analyzeTableau(tableau, numberOfRestrictions, numberOfVariables):
   PLType = checkTableau(tableau, numberOfRestrictions)

   if PLType == 'optimal':
      print('otima')
      objectiveValue = getObjectiveValue(tableau)
      print(objectiveValue)
      solution = getSolution(tableau, numberOfRestrictions, numberOfVariables)
      print(solution)
      certificate = getCertificate(tableau, PLType, numberOfRestrictions)
      print(certificate)

   elif PLType == 'unfeasible':
      print('inviavel')
      certificate = getCertificate(tableau, PLType)
   
   elif PLType == 'limitless':
      print('ilimitada')
      solution = getSolution(tableau, PLType, numberOfRestrictions, numberOfVariables)
      certificate = getCertificate(tableau, PLType, numberOfRestrictions)

def analyzeAuxTableau(auxTableau, numberOfRestrictions, numberOfVariables):
   PLType = checkTableau(auxTableau, numberOfRestrictions)

   if PLType == 'optimal':
      print('otima')
      objectiveValue = getObjectiveValue(tableau)
      print(objectiveValue)
      solution = getSolution(tableau, PLType, numberOfRestrictions, numberOfVariables)
      print(solution)
      certificate = getCertificate(tableau, PLType, numberOfRestrictions)
      print(certificate)

def simplexIterations(tableau, numberOfRestrictions):
   iteration = 0

   while 1:
      iteration += 1

      columnToPivot = findColumnToPivot(tableau, numberOfRestrictions)
      if columnToPivot == -1:
         break;

      rowOfElementPivot = findMinimumRatioInColumn(tableau, columnToPivot, numberOfRestrictions)
      if rowOfElementPivot == -1:
         break;

      elementPivotIndexes = (rowOfElementPivot, columnToPivot)

      pivot(tableau, elementPivotIndexes)

def auxCanonicalBase(tableauAux):
   for i in range(0, tableauAux.shape[0] - 1):
      tableauAux[tableauAux.shape[0] - 1,:] = tableauAux[tableauAux.shape[0] - 1,:] + (tableauAux[i,:] * (-1))

def main():
   numberOfRestrictions, numberOfVariables = [int(x) for x in input().split()]
   (A, b, c) = getOptimizationInputValues(numberOfRestrictions)
   (A_fpi, b_fpi, c_fpi) = getFPIForm(A, b, c, numberOfRestrictions)
   (A_fpi_aux, b_fpi_aux, c_fpi_aux, negative_b_indexes) = getAuxFPIForm(A_fpi, b_fpi, c_fpi, numberOfRestrictions)

   tableauAux = getTableau(A_fpi_aux, b_fpi_aux, c_fpi_aux, numberOfRestrictions, numberOfVariables, True, negative_b_indexes)
   # tableau = getTableau(A_fpi, b_fpi, c_fpi, numberOfRestrictions, numberOfVariables)

   # print(tableauAux)

   auxCanonicalBase(tableauAux)

   # print(tableauAux)

   simplexIterations(tableauAux, numberOfRestrictions)

   # print(tableauAux)

   subs_tableau = np.delete(tableauAux, tableauAux.shape[1] - 2, 1)
   subs_tableau = np.delete(subs_tableau, subs_tableau.shape[1] - 2, 1)


   for i in range(0, c_fpi.shape[0]):
      subs_tableau[subs_tableau.shape[0] - 1][numberOfRestrictions + i] = c_fpi[i] * (-1)

   for i in range(0, numberOfRestrictions):
      subs_tableau[subs_tableau.shape[0] - 1][i] = 0

   simplexIterations(subs_tableau, numberOfRestrictions)

   # print(subs_tableau)

   auxSolution = getSolution(subs_tableau, numberOfRestrictions, numberOfVariables);
   auxObjValue = getObjectiveValue(subs_tableau)
   certificate = getCertificate(subs_tableau, 'optimal', numberOfRestrictions)

   print(auxSolution)
   print(auxObjValue)
   print(certificate)

   # analyzeTableau(tableau, numberOfRestrictions, numberOfVariables)
      
if __name__ == "__main__":
   main()