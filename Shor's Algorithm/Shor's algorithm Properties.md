# Shor's Algorithm
### An error will occur if we enter a non-prime number

 - Precondition:

A random non-prime integer below 15: *a*

An integer of value 0-7, as power for the controlled U gate: *p*

- Operation:

c_amod15( a, p )

- Output:

assertException( ValueError )

---

### The phase returned from QPE_amod_15 must be between 0 and 1

>Note that it's between 0 and 1, because it the function returns a proportion of the 2π rad phase

 
 - Precondition:

A random non-prime integer below 15: *a*

- Operation:

qpe_amod15( *a* ): *θ<sub>a</sub>*

- Output:

assertTrue( *θ<sub>a</sub>* >= 0 AND *θ<sub>a</sub>* <= 1)

---

### After Shor's algorithm has been applied, at least one factor of 15 will be returned 
 
 - Precondition:

A random non-prime integer below 15: *a*

- Operation:

findFactor( *a* ): factors

- Output:

assertTrue(*3* in factors OR *5* in factors)

---