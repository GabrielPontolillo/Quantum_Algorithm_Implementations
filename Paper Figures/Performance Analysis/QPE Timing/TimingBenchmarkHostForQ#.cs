using System;
using System.Diagnostics;

using Microsoft.Quantum.Simulation.Core;
using Microsoft.Quantum.Simulation.Simulators;
using System.Linq;

namespace QPE_Qsharp
{
    class Driver
    {
        const int RUNS = 10000;
        const int ESTIMATION_QUBIT_AMT = 8;

        static void Main(string[] args)
        {
            var sw = new Stopwatch();

            long[] postProTimes = new long[10];
            /////////////////////////////
            /// DO POSTPROCESSING RUN ///
            /////////////////////////////
            for (int j = 0; j < 11; j++){
                sw.Reset();
                sw.Start();
                using (var qsim = new QuantumSimulator())
                {
                    String[] resArr = new String[RUNS]; 
                    for (int i = 0; i < RUNS; i++){
                        var measurementResult = runQPEGenerator.Run(qsim).Result;
                        //Console.WriteLine(measurementResult);
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

                    //Console.WriteLine(query);
                    //Console.WriteLine(query.Item);
                    //Console.WriteLine((double)query.Item / Math.Pow((double)2.0, (double)ESTIMATION_QUBIT_AMT));
                }
                sw.Stop();
                // ignore first loop for JIT compiling delay
                if (j != 0){
                    postProTimes[j-1] = sw.ElapsedMilliseconds;
                }
            }
            Console.WriteLine("With my postprocessing to get the final value");
            //long mean = postProTimes.Sum()/10;
            //Console.WriteLine("Average time taken for " + RUNS.ToString() + " shots: " + mean.ToString() + "ms");
            Console.WriteLine();
            Array.ForEach<long>(postProTimes, Console.WriteLine);
            

            ////////////////////////////////
            /// NOW DO NO POSTPROCESSING ///
            ////////////////////////////////
            /*
            long[] noPostProTimes = new long[10];
            for (int j = 0; j < 11; j++){
                sw.Reset();
                sw.Start();
                using (var qsim = new QuantumSimulator())
                {
                    String[] resArr = new String[RUNS]; 
                    for (int i = 0; i < RUNS; i++){
                        var measurementResult = runQPEGenerator.Run(qsim).Result;
                    }
                }
                sw.Stop();
                // ignore first loop for JIT compiling delay
                if (j != 0){
                    noPostProTimes[j-1] = sw.ElapsedMilliseconds;
                }
            }
            Console.WriteLine("With No Postprocessing");
            //long meanNoPostpro = noPostProTimes.Sum()/10;
            //Console.WriteLine("Average time taken for " + RUNS.ToString() + " shots: " + meanNoPostpro.ToString() + "ms");
            Array.ForEach<long>(noPostProTimes, Console.WriteLine);
            */
            
            /////////////////////////////////////////////////
            /// NOW ONLY LOOP FROM QS + NO POSTPROCESSING ///
            /////////////////////////////////////////////////
            /*
            long[] noPostProLoopInQsTimes = new long[10];
            for (int j = 0; j < 11; j++){
                sw.Reset();
                sw.Start();
                using (var qsim = new QuantumSimulator())
                {
                    var measurementResult = runQPEGeneratorLoop.Run(qsim).Result;
                }
                sw.Stop();
                // ignore first loop for JIT compiling delay
                if (j != 0){
                    noPostProLoopInQsTimes[j-1] = sw.ElapsedMilliseconds;
                }
            }
            Console.WriteLine("Calling the for loop from QS code");
            //long meanNoPostproLoopQs = noPostProLoopInQsTimes.Sum()/10;
            //Console.WriteLine("Average time taken for " + RUNS.ToString() + " shots: " + meanNoPostproLoopQs.ToString() + "ms");
            Array.ForEach<long>(noPostProLoopInQsTimes, Console.WriteLine);
            */
        }
    }
}