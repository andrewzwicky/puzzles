using System.Collections.Generic;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using Problem34;
using System;

namespace Problem34Test
{

   [TestClass]
   public class Problem34Test
   {

      [TestMethod]
      public void FactorialTestZero()
      {
         Problem34_Accessor target = new Problem34_Accessor();
         int n;
         int expected;
         Dictionary<int, int> expectedFactorials = new Dictionary<int, int>();

         n = 0;
         expected = 1;

         Assert.AreEqual(expected, Problem34_Accessor.Factorial(n));
      }

      [TestMethod]
      public void FactorialTestOne()
      {
         Problem34_Accessor target = new Problem34_Accessor();
         int n;
         int expected;
         Dictionary<int, int> expectedFactorials = new Dictionary<int, int>();

         n = 1;
         expected = 1;
         
         Assert.AreEqual(expected, Problem34_Accessor.Factorial(n));
      }

      [TestMethod]
      public void FactorialTestTwo()
      {
         Problem34_Accessor target = new Problem34_Accessor();
         int n;
         int expected;
         Dictionary<int, int> expectedFactorials = new Dictionary<int, int>();

         n = 2;
         expected = 2;

         Assert.AreEqual(expected, Problem34_Accessor.Factorial(n));
      }

      [TestMethod]
      public void FactorialTestThree()
      {
         Problem34_Accessor target = new Problem34_Accessor();
         int n;
         int expected;
         Dictionary<int, int> expectedFactorials = new Dictionary<int, int>();

         n = 3;
         expected = 6;

         Assert.AreEqual(expected, Problem34_Accessor.Factorial(n));
      }

      [TestMethod]
      public void FactorialTestFour()
      {
         Problem34_Accessor target = new Problem34_Accessor();
         int n;
         int expected;
         Dictionary<int, int> expectedFactorials = new Dictionary<int, int>();

         n = 4;
         expected = 24;

         Assert.AreEqual(expected, Problem34_Accessor.Factorial(n));
      }

      [TestMethod]
      public void FactorialTestFive()
      {
         Problem34_Accessor target = new Problem34_Accessor();
         int n;
         int expected;
         Dictionary<int, int> expectedFactorials = new Dictionary<int, int>();

         n = 5;
         expected = 120;

         Assert.AreEqual(expected, Problem34_Accessor.Factorial(n));
      }

      [TestMethod()]
      public void SplitDigitsTest()
      {
         Problem34_Accessor target = new Problem34_Accessor(); // TODO: Initialize to an appropriate value
         int n = 123;
         int[] expected = new int[] { 1, 2, 3 };
         int[] actual = Problem34_Accessor.SplitDigits(n);
         
         CollectionAssert.AreEqual(expected, actual);
      }

      [TestMethod()]
      public void SplitDigitsTest2()
      {
         Problem34_Accessor target = new Problem34_Accessor(); // TODO: Initialize to an appropriate value
         int n = 1234234;
         int[] expected = new int[] { 1, 2, 3, 4, 2, 3, 4 };
         int[] actual = Problem34_Accessor.SplitDigits(n);

         CollectionAssert.AreEqual(expected, actual);
      }
   }
}
