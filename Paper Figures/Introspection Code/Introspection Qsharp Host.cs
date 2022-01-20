using System;

using Microsoft.Quantum.Simulation.Core;
using Microsoft.Quantum.Simulation.Simulators;
using System.Linq;

namespace QPE_Qsharp
{
    class Driver
    {
        const int RUNS = 1000;
        const int ESTIMATION_QUBIT_AMT = 8;

        static void Main(string[] args)
        {
            using (var qsim = new QuantumSimulator())
            {
                var msmtres = runIntrospection.Run(qsim).Result;
            }
        }
    }
}