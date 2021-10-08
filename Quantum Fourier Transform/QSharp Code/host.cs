using System;

using Microsoft.Quantum.Simulation.Core;
using Microsoft.Quantum.Simulation.Simulators;

namespace MyQFT
{
    class Driver
    {
        static void Main(string[] args)
        {
            using (var qsim = new QuantumSimulator())
            {
                Result[] resArr = new Result[100]; 
                for (int i = 0; i < 100; i++){
                    var measurementResult = runQFTGenerator.Run(qsim).Result;
                    //get the first qubit
                    resArr[i] = measurementResult[0];
                }
                int ctr0 = 0;
                int ctr1 = 0;
                foreach (Result res in resArr){
                    if (res == ResultConst.Zero){
                        ctr0++;
                    } else if (res == ResultConst.One){
                        ctr1++;
                    }
                }
                System.Console.WriteLine(ctr0);
                System.Console.WriteLine(ctr1);
            }
        }
    }
}