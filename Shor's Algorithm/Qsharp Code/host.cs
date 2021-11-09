using System;
using System.Collections.Generic;
using System.Numerics;

using Microsoft.Quantum.Simulation.Core;
using Microsoft.Quantum.Simulation.Simulators;


namespace Shors_Algorithm
{
    class Driver
    {
        static void Main(string[] args)
        {
            int a = 7;
            int N = 15;
            bool factor_found = false;
            int attempt = 0;
            using (var qsim = new QuantumSimulator())
            {
                while (!factor_found) {
                    attempt += 1;
                    Console.WriteLine("Attempt " + attempt);
                    String resString = "";
                    for (int i = 0; i < 8; i++) {
                        Result res = (Result)runShors.Run(qsim, a).Result[i];
                        if (res == Result.One){
                            resString +=  "1";
                        } else {
                            resString +=  "0";
                        }
                    }
                    BigInteger denominator = new BigInteger(Math.Pow(2, resString.Length));
                    BigInteger numerator = new BigInteger(Convert.ToInt32(resString, 2));
                    Console.WriteLine(numerator + "/" + denominator);
                    int r = getSimplifiedPhaseDenominator(numerator, denominator);
                    Console.WriteLine("Result: r = " + r);
                    if (r != 0){
                        int guessA = (int) BigInteger.GreatestCommonDivisor(new BigInteger(Math.Pow(a,r/2)-1),new BigInteger(N));
                        int guessB = (int) BigInteger.GreatestCommonDivisor(new BigInteger(Math.Pow(a,r/2)+1),new BigInteger(N));
                        int[] guesses = new int[2]{guessA, guessB};
                        foreach (int guess in guesses) {
                            if (guess != 1 && guess != N && (N % guess == 0)){
                                Console.WriteLine("*** Non-trivial factor found: " + guess + " ***");
                                factor_found = true;
                            }
                        }
                    }
                }
            }
        }

        private static int getSimplifiedPhaseDenominator(BigInteger numerator, BigInteger denominator){
            BigInteger gcd =  BigInteger.GreatestCommonDivisor(numerator,denominator);
            if (numerator > 0 ) {
                int order = (int) BigInteger.Divide(denominator, gcd);
                return order;
            } else {
                return 0;
            }
        }
    }
}