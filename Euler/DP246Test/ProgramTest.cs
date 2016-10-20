using DP246;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using System;
using System.Collections.Generic;

namespace DP246Test
{
   [TestClass()]
   public class DP246Test
   {
      [TestMethod()]
      public void PossiblesTestSingle()
      {
         string numbers = "1";
         List<int[]> expected = new List<int[]> { new int[] { 1 } };
         List<int[]> actual;
         actual = Program_Accessor.Possibles(numbers);
         CollectionAssert.AreEquivalent(expected, actual);
      }

      [TestMethod()]
      public void PossiblesTestDouble()
      {
         string numbers = "12";
         List<int[]> expected = new List<int[]> { 
            new int[] { 1, 2 }, 
            new int[] { 12 } 
         };
         List<int[]> actual;
         actual = Program_Accessor.Possibles(numbers);
         CollectionAssert.AreEquivalent(expected, actual);
      }
   }
}
