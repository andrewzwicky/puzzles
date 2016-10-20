using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Problem34
{
   class Problem34
   {
      static Dictionary<int, int> factorials = new Dictionary<int, int>();

      static void Main(string[] args)
      {
         int total = 0;

         for (int i = 3; i < int.MaxValue; i++)
         {
            int[] digits = SplitDigits(i);
            int[] digitsFactorial = digits.Select(digit => Factorial(digit)).ToArray();
            int sum = digitsFactorial.Sum();

            if (i == sum)
            {
               Console.WriteLine(i);
               total += i;
            }

            if (digits.Length * Factorial(9) < i)
            {
               break;
            }
         }

         Console.WriteLine(string.Format("Total: {0}", total));
      }

      static int Factorial(int n)
      {
         int result;

         if (!factorials.TryGetValue(n, out result))
         {
            if (n == 1 || n == 0)
            {
               result = 1;
            }
            else
            {
               result = n * Factorial(n - 1);
            }

            factorials.Add(n, result);
         }

         return result;
      }

      static int[] SplitDigits(int n)
      {
         return n.ToString()
                 .ToCharArray()
                 .Select(digit => (int)Char.GetNumericValue(digit))
                 .ToArray();
      }
   }
}
