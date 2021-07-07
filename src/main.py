import numpy as np

def main():
   number_of_restrictions, number_of_variables = [int(x) for x in input().split()]

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


if __name__ == "__main__":
   main()