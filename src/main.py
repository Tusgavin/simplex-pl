import numpy as np

def pivot(A, b, c, leaving_index, entering_index):
   print(A, b, c, leaving_index, entering_index)

def getOptimizationInputValues(number_of_variables):
   c = [int(x) for x in input().split()]

   A = []
   b = []
   
   for _ in range(0, number_of_variables):
      A_i_b = [int(x) for x in input().split()]
      
      b_i = A_i_b[-1]
      del A_i_b[-1]
      
      A.append(A_i_b)
      b.append(b_i)

   A = np.array(A, dtype=np.int)
   b = np.array(b, dtype=np.int)
   c = np.array(c, dtype=np.int)

   return (A, b, c)

def getFPIForm(A, b, c, number_of_restrictions):
   ident = np.identity(number_of_restrictions, dtype=np.int);
   new_vars = np.zeros((number_of_restrictions), dtype=np.int);

   A_fpi = np.concatenate((A, ident), axis=1)
   c_fpi = np.concatenate((c, new_vars), axis=None)
   b_fpi = np.copy(b)

   return (A_fpi, b_fpi, c_fpi)

def main():
   number_of_restrictions, number_of_variables = [int(x) for x in input().split()]

   (A, b, c) = getOptimizationInputValues(number_of_variables)

   (A_fpi, b_fpi, c_fpi) = getFPIForm(A, b, c, number_of_restrictions)

   if (c <= 0).all():
      print("otima")
      valor_obj = np.dot(b, c);
      print(valor_obj)
      print(b)
      print(c)

   for index, element in enumerate(c):
      if element > 0:
         if (A[:,index] <= 0).all():
            print("ilimitada")
            print(b)

if __name__ == "__main__":
   main()