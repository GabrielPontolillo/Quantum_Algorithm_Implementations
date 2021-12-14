# Quantum-Algorithm-Implementations

Contains code, descriptions of quantum algorithms in Qiskit, Q# and Cirq

---

## Beginning with Quantum computing: a comprehensive guide.

### Chapter 1: A little bit of quantum theory

For a very basic and short introduction look at the first few chapters of this site, from “The basics of quantum computing” to “What is a quantum algorithm”, don’t worry about the code in [this site](https://www.quantum-inspire.com/kbase/introduction-to-quantum-computing/), but the theory is good. 

Qiskit’s (IBM) lecture videos provide a very good introduction to quantum computing, they go through a lot of theory and explain the basics in a timely manner. They also go through quantum algorithms in a digestible manner for a beginner. 
I would recommend watching lectures **up to chapter 9**. 

- [Qiskit's course](https://qiskit.org/learn/intro-qc-qh/)

This course provides lecture notes and labs as well as the lectures, though I recommend that you take your own notes to better retain the details. In these videos they **mainly go through theory**, so you should watch these no matter what QC language you use.

I would also recommend [StackOverflow](https://stackoverflow.com/) for asking questions if you get stuck somewhere. Unfortunately, there are not many questions already asked on StackOverflow for quantum programming languages, that’s why I’d only recommend looking there if you have a specific question to ask.

You can also use a more specific [StackExchange](https://quantumcomputing.stackexchange.com/) for **quantum computing**, a lot of the threads go through high level theory instead of coding, but it's **more active than** the QC language tags on StackOverflow for [Qiskit](https://stackoverflow.com/questions/tagged/qiskit), [CirQ](https://stackoverflow.com/questions/tagged/cirq) and [Q#](https://stackoverflow.com/questions/tagged/q%23).

[This page](https://qiskit.org/textbook/ch-states/single-qubit-gates.html) on the Qiskit Documentation has been very useful for details on various **Single Qubit Gates**.

---

### Chapter 2: Installation Guide

#### General for Qiskit and CirQ

- [Install Python](https://www.python.org/downloads/) 
- [Install Anaconda](https://www.anaconda.com/products/individual) 
- [Manage Python Environments in Jupyter notebooks](https://stackoverflow.com/questions/37085665/in-which-conda-environment-is-jupyter-executing) Get the Conda tab like in the accepted answer: I ran `conda install nb_conda` in the *anaconda prompt*.

#### Qiskit

- [Install Qiskit](https://qiskit.org/documentation/getting_started.html) follow the guide for local install, make sure you create an environment like it recommends, otherwise some functions may not work.

#### CirQ

- [Install CirQ](https://quantumai.google/cirq/install) I recommend you make a separate environment like the instructions in Qiskit.

#### Q#

- [Install .NET SDK](https://dotnet.microsoft.com/download)
- [Install Visual Studio Code](https://code.visualstudio.com/Download) It's the IDE that I used, it has good support for Q#.
- Install the C# extension in VS code: Type C# in the extension tab in VS code, the one from Microsoft.
- [Install QDK for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=quantum.quantum-devkit-vscode)

#### R

- [Install R](https://cran.r-project.org/bin/windows/base/)
- [Install RStudio](https://www.rstudio.com/products/rstudio/) Get the open source version for desktop.
- [Install RTools4](https://cran.r-project.org/bin/windows/Rtools/)

---

### Chapter 3: Programming language tutorials and handy links

#### Qiskit 

- [Step-by-step introduction to Qiskit](https://qiskit.org/textbook/ch-algorithms/defining-quantum-circuits.html) This link provides many tutorials in Qiskit, they are very well structured and paced - highly recommended - Go as far as you feel comfortable with, but you will probably **not need to go further than chapter 3.6**, the aim is to get comfortable with the Qiskit Syntax, and general structure.
- [Faster paced tutorials](https://qiskit.org/documentation/tutorials.html) These tutorials provided in the Qiskit documentation website, provide less theory, and are less step-by-step, but they are more time efficient.
- [Official Documentation](https://qiskit.org/documentation/apidoc/aer.html) In this github we currently only use Qiskit Aer API.
- [Qiskit backends guide](https://medium.com/qiskit/qiskit-backends-what-they-are-and-how-to-work-with-them-fb66b3bd0463) A guide on providers and backends in Qiskit, we use a local Aer backend.
- [Qiskit Circuit Library](https://qiskit.org/documentation/locale/fr_FR/apidoc/circuit_library.html) Documentation on the gates that can be added to a Qiskit Circuit.
- [Quantum Fourier Transform](https://quantumcomputinguk.org/tutorials/quantum-fourier-transform-in-qiskit) Another Quantum Fourier Transform implementation in Qiskit, a good explanation.

#### CirQ

If you've begun by looking into qiskit, the structure of CirQ code will be very familiar as they follow a very similar concept of defining a quantum circuit and running it. The main difference that can be found with CirQ, is that Qubits are separate Objects and they need to be declared and stored in an array and passed into functions that create said circuits.

- [Basic tutorial for CirQ](https://quantumai.google/cirq/tutorials/basics) Simple introduction to syntax and various concepts.
- [Textbook algorithms in CirQ](https://quantumai.google/cirq/tutorials/educators/textbook_algorithms) Contains various quantum algorithm implementation.
- [Other tutorials from Google](https://quantumai.google/cirq/tutorials)
- [Official Documentation](https://quantumai.google/reference/python/cirq/all_symbols)

#### Q#

When searching for information on google on Q#, search ‘microsoft qsharp’ in google instead of ‘Q#’, otherwise you will get a lot of irrelevant results. 

- [A basic tutorial on calling Q# code with a C# host](https://docs.microsoft.com/en-us/azure/quantum/install-csharp-qdk?tabs=tabid-cmdline%2Ctabid-csharp) It also includes some basic Q# syntax.
- [The 4 tutorials on this site are quite good](https://docs.microsoft.com/en-us/azure/quantum/tutorial-qdk-quantum-random-number-generator?tabs=tabid-qsharp)
- [The Q# user guide](https://docs.microsoft.com/en-us/azure/quantum/user-guide/)
- [The Q# language guide](https://docs.microsoft.com/en-us/azure/quantum/user-guide/language/programstructure/) Check through the Q# language guide, the Q# syntax is quite challenging to learn, the best way to do so is to look at the documentation. [One example of this](https://docs.microsoft.com/en-us/azure/quantum/user-guide/language/statements/variabledeclarationsandreassignments): To create a variable that can be reassigned you have to use `mutable` and to reassign the variable you have to use `set`. Be sure to check this language guide if you are stuck.
- [Official Documentation](https://docs.microsoft.com/en-us/qsharp/api/)

#### R

R seems very similar to Python data science with Pandas, Mathplotlib, Numpy. I recommend using StackOverflow for this one as the official documentation is not very good. 

- [A good place to start - dataframes](https://www.datacamp.com/community/tutorials/15-easy-solutions-data-frame-problems-r)
- [Official Introduction](https://cran.r-project.org/doc/manuals/r-release/R-intro.html#Preface)
- [R FAQ](https://cran.r-project.org/doc/FAQ/R-FAQ.html)

---

### Chapter 4: This GitHub

Once you understand some of the theory, installed everything and had a look at some of the programming languages, you can begin by looking at the [Quantum Fourier Transform folder](https://github.com/Lilgabz/Quantum-Algorithm-Implementations/tree/main/Quantum%20Fourier%20Transform)

There are 4 folders in the QFT folder:
1. **[CirQ Code](https://github.com/Lilgabz/Quantum-Algorithm-Implementations/tree/main/Quantum%20Fourier%20Transform/CirQ%20Code)**: Contains the notebook file with the CirQ code in it to run QFT, make sure to run this in your CirQ Environment 
2. **[QSharp Code](https://github.com/Lilgabz/Quantum-Algorithm-Implementations/tree/main/Quantum%20Fourier%20Transform/QSharp%20Code)**: Contains C# host file and Q# quantum algorithm file, open these with visual studio code
3. **[Qiskit Code](https://github.com/Lilgabz/Quantum-Algorithm-Implementations/tree/main/Quantum%20Fourier%20Transform/Qiskit%20Code)**: Contains the notebook file with the Qiskit code in it to run QFT, make sure to run this in your Qiskit Environment  
4. **[R Code](https://github.com/Lilgabz/Quantum-Algorithm-Implementations/tree/main/Quantum%20Fourier%20Transform/R%20Code)**: Contains the R code that analyses a spreadsheet of results to calculate the phase of each qubit from their X and Y measurements. It also contains 2 input and 2 output spreadsheets to give an example of the input files that the R code accepts and output files that it generates (QFTres0111.xlsx, input file and QFTres0111Calc.xlsx, output file). Bear in mind that in the R code, **you should change the path of the input file to calculate and add a location to create the output file**.

There are also 2 word document files in the QFT folder:
1. **[QFT Benchmarks](https://github.com/Lilgabz/Quantum-Algorithm-Implementations/blob/main/Quantum%20Fourier%20Transform/QFT%20Benchmarks.docx)**:
    - Includes a short description of Quantum Fourier Transform 
    - Includes 5 properties that can be tested
    - Step-by-step and side-by-side descriptions of all 3 implementations of the QFT algorithm, this is quite in depth and will help with understanding the differences between the languages.
2. **[QFT Property Test Example](https://github.com/Lilgabz/Quantum-Algorithm-Implementations/blob/main/Quantum%20Fourier%20Transform/QFT%20Property%20Test%20Example.docx)**:
    - This document contains 5 examples of manually testing the properties using the results gathered from the output spreadsheet genereated from the R code.
  
---
  
### Chapter 5: Guide to start

1. It's best to look at the "QFT Code Comparisons & Description" and "QFT Properties" document first, to get an idea of what the code looks like and what the QFT algorithm should do.
2. Then, I recommend trying to run the quantum algorithm code on your local machines, again be careful with the environments that you run the Qiskit and Cirq code. 
3. Try and create another spreadsheet like [QFTres0111.xlsx](https://github.com/Lilgabz/Quantum-Algorithm-Implementations/blob/main/Quantum%20Fourier%20Transform/R%20Code/QFTres0111.xlsx) (but with a different set of input qubits), gather your own results across the different languages (you will have to modify some of the code to do this, like changing the **measurement qubits**, and **changing set_measure_x to set_measure_y**)  
4. Analyse this spreadsheet with the R script, you will need to **change the file locations in the code** and **install the packages** that are used in the code by running: 
    - `install.packages("xlsx")`
    - `install.packages("dplyr")`
    - `install.packages("readxl")`
5. Take a look at the "QFT Property Test Example" document, see what properties you can test with the output spreadsheet you generated with R.
---
