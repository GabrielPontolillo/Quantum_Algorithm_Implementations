using System;
using System.Collections.Generic;

using Microsoft.Quantum.Simulation.Core;
using Microsoft.Quantum.Simulation.Simulators;

namespace QuantumFourierTransform
{
    class Driver
    {
        static void Main(string[] args)
        {
            using (var qsim = new QuantumSimulator())
            {
                //Result[] resArr = new Result[100]; 
                Dictionary<string, int> resCount = new Dictionary<string, int>();
                for (int i = 0; i < 100000; i++){
                    String resString = runQFTGenerator.Run(qsim).Result.ToString();
                    int value;
                    if(resCount.TryGetValue(resString, out value)){
                        resCount[resString] = value+1;
                    } else {
                        resCount.Add(resString, value+1);
                    }
                    //var measurementResult = runQFTGenerator.Run(qsim).Result;
                    //get the first qubit
                    //resArr[i] = measurementResult[1];
                }
                foreach (KeyValuePair<string, int> vals in resCount){
                    Console.WriteLine("Key = {0}, Value = {1}", vals.Key, vals.Value);
                }
                /*int ctr0 = 0;
                int ctr1 = 0;
                foreach (Result res in resArr){
                    if (res == ResultConst.Zero){
                        ctr0++;
                    } else if (res == ResultConst.One){
                        ctr1++;
                    }
                }
                System.Console.WriteLine(ctr0);
                System.Console.WriteLine(ctr1);*/
            }
        }
    }
}