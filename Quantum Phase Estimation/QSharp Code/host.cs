using System;

using Microsoft.Quantum.Simulation.Core;
using Microsoft.Quantum.Simulation.Simulators;
using System.Linq;

namespace QPE_Qsharp
{
    class Driver
    {
        const int RUNS = 1000;
        const int ESTIMATION_QUBIT_AMT = 5;

        static void Main(string[] args)
        {
            using (var qsim = new QuantumSimulator())
            {
                String[] resArr = new String[RUNS]; 
                for (int i = 0; i < RUNS; i++){
                    var measurementResult = runQPEGenerator.Run(qsim).Result;
                    String resStr = "";
                    foreach (Result res in measurementResult){
                        if (res == ResultConst.Zero){
                            resStr = "0" + resStr;
                        } else if ( res == ResultConst.One){
                            resStr = "1" + resStr;
                        }
                    }
                    resArr[i] = resStr;
                }

                int[] intArr = new int[RUNS];
                int ctr = 0;
                foreach(var binStr in resArr){
                    intArr[ctr] = Convert.ToInt32(binStr,2);
                    ctr++;
                }

                var query = (from item in intArr
                    group item by item into g
                    orderby g.Count() descending
                    select new { Item = g.Key, Count = g.Count() }).First();

                Console.WriteLine(query);
                Console.WriteLine(query.Item);
                Console.WriteLine((double)query.Item / Math.Pow((double)2.0, (double)ESTIMATION_QUBIT_AMT));
            }
        }
    }
}