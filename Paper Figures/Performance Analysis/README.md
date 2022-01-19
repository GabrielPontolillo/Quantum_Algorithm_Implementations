# Benchmark PC specification to run the tests:

CPU: Ryzen 5 2600 stock 
RAM: 16 Gb @ 3000Mhz
GPU: Nvidia RTX 3060ti
Windows 10

Tests ran without background tasks running. 

Results:
Results given for 10 loops of 10,000 shots

## Qiskit:
Average time taken for 10000 shots: 99ms 


## Cirq: 
Average time taken for 10000 shots: 125ms 

## Q#:

With my postprocessing to get the final value
Average time taken for 10000 shots: 40505ms
With No Postprocessing to get the final value
Average time taken for 10000 shots: 39557ms
Calling the for loop from QS code
Average time taken for 10000 shots: 35487ms
