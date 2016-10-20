using System;
using System.Collections.Generic;
using System.Text.RegularExpressions;
using System.Linq;
using System.Text;
using System.IO;
using System.Diagnostics;

namespace DP2015_12_18
{
   class Program
   {
      static void Main(string[] args)
      {
         DateTime start = DateTime.Now;

         string queryfile = @"C:\Users\AZ55845\Desktop\query10k.txt";
         string ipfile =    @"C:\Users\AZ55845\Desktop\ips300k.txt";

         QueryDatabase queryDB = new QueryDatabase(queryfile);
         IPDatabase ipsDB = new IPDatabase(ipfile);

         Dictionary<string, List<uint>> results = new Dictionary<string, List<uint>>();

         foreach (uint ip in queryDB.queries)
         {
            IPDatabase.IPRange match;
            string name;

            try
            {
               match = ipsDB.ips.Where(range => (ip >= range.min && ip <= range.max)).OrderBy(range => range.size).First();
               name = match.name;
            }
            catch (InvalidOperationException)
            {
               match = null;
               name = "<unknown>";
            }

            if (!results.ContainsKey(name))
            {
               results[name] = new List<uint>();
            }

            results[name].Add(ip);
         }

         foreach (KeyValuePair<string, List<uint>> KVP in results.OrderByDescending(key => key.Value.Count))
         {

            Console.WriteLine(string.Format("{0} - {1}" , KVP.Value.Count, KVP.Key));
            // foreach (uint ip in KVP.Value)
            // {
            //    Console.WriteLine(Database.DecryptIP(ip));
            // }
         }

         
         Console.WriteLine(string.Format("{0} s",DateTime.Now.Subtract(start).TotalSeconds));
      }
   }

   class Database
   {
      static char[] ipSeparator = new char[] { '.' };
      
      public Database(string dbFile)
      {

      }

      static protected uint EncryptIP(List<uint> IPnums)
      {
         uint result = 0;

         result += IPnums[0] << 24;
         result += IPnums[1] << 16;
         result += IPnums[2] << 8;
         result += IPnums[3] << 0;

         return result;
      }

      static public string DecryptIP(uint ipInt)
      {
         uint[] sections = new uint[4];
         uint[] masks = new uint[4] { 0xFF000000, 0xFF0000, 0xFF00, 0xFF };
         uint[] shifts = new uint[4] { 24, 16, 8, 0 };

         for (int i = 0; i < 4; i++)
         {
            sections[i] = (ipInt & masks[i]) >> (int)shifts[i];
         }

         return string.Join(".", sections);
      }

      static protected List<uint> ParseIP(string IP)
      {
         return IP.Split(ipSeparator).Select(section => uint.Parse(section)).ToList();
      }
   }

   class QueryDatabase : Database
   {
      public List<uint> queries;

      public QueryDatabase(string dbFile)
         : base(dbFile)
      {
         queries = File.ReadAllLines(dbFile).Select(ip => ParseIP(ip)).Select(ipNums => EncryptIP(ipNums)).ToList();
      }
   }

   class IPDatabase : Database
   {
      static char[] rangeSeparator = new char[] { ' ' };

      public class IPRange
      {
         public uint min;
         public uint max;
         public uint size;
         public string name;
      }

      public List<IPRange> ips = new List<IPRange>();

      public IPDatabase(string dbfile) : base(dbfile)
      {
         foreach (string line in File.ReadAllLines(dbfile))
         {
            string[] components = line.Split(rangeSeparator,3);
            IPRange result = new IPRange();
            result.min = EncryptIP(ParseIP(components[0]));
            result.max = EncryptIP(ParseIP(components[1]));
            result.name = components[2];
            result.size = result.max - result.min;
            
            ips.Add(result);
         }
      }
   }
}
