# Quantum Phase Estimation
> Make sure to repeat the estimation a sufficient amount of times to increase the consistency of the tests:  Shots ≈ 10000

### *A phase estimated using more qubits should be closer to the real phase of a qubit compared to a phase estimated with a lesser amount of qubits.*

- **Precondition:**

Amount of qubits for QPE run 1 : n

Amount of qubits for QPE run 2 : m

Where m > n

Randomly selected angle between 0 and 2π  : θ<sub>1</sub>

- **Operation:**

QPE( n, θ<sub>1</sub> ) : (most frequent result)  estThetaN

QPE( m, θ<sub>1</sub> ) : (most frequent result)  estThetaM

- **Output:**

assertTrue( ABS( estThetaN - θ<sub>1</sub> ) >= ABS( estThetaM - θ<sub>1</sub> ) ) 

---

### *The estimated phase should be accurate to 2<sup>-n</sup> radians.*

- **Precondition:**

Amount of qubits for QPE : n

Randomly selected angle between 0 and 2π  : θ<sub>1</sub>

- **Operation:**

QPE( n, θ<sub>1</sub> ) : (most frequent result)  estThetaN

- **Output:**

assertTrue(  ABS( estThetaN - θ<sub>1</sub> ) <= 2<sup>-n</sup> ) 

---
### *The QPE algorithm should return the exact phase if the input qubits' phase is an exact multiple of π/2<sup>n-1</sup>*

- **Precondition:**

Amount of qubits for QPE : n

Randomly selected angle between 0 and 2π  : θ<sub>1</sub>

Where θ<sub>1</sub> is an exact multiple of π/2<sup>n-1</sup> 

Amount of repetitions: Shots 

- **Operation:**

QPE( n, θ<sub>1</sub> ) : (most frequent result)  estThetaN

- **Output:**

assertEqual( estThetaN, θ<sub>1</sub> )

assertEqual( count( estThetaN ), Shots )

> The bottom assertions check that the results returned from the algorithm are exact and correct, for every shot 
---
### *The estimated phase should be between 0 and 2π radians*

- **Precondition:**

Amount of qubits for QPE : n

Randomly selected angle between 0 and 2π  : θ<sub>1</sub>
- **Operation:**

QPE( n, θ<sub>1</sub> ) : estThetaN

- **Output:**

assertTrue(estThetaN >= 0)

assertTrue(estThetaN <= 1)

> estThetaN returns a proportion of 2π, in the above example estThetaN⋅2π >= 0 and estThetaN⋅2π >= θ<sub>1</sub> would also be appropriate for our current implementation