# VM Translator 

## Project 6: Stack Arithmetic

Our VM is based on a stack machine. By using a stack abstraction, we can write a language that allows us to describe the behavior and data of a program without having direct knowledge of the hardware.  

That said, we do need to bootstrap this stack with some memory locations. The most important of which is the address where the stack begins!

memory segments 

stack - stores the address of the top of our stack
local - stores the base address of local values
argument - stores base address of function arguments
this - stores ?
that - stores ?

how these are mapped to our hack computer RAM

address

So first we reserve the first (0) for our stack pointer on the hack machine

0 -> stack
1 - LCL
2 - argument
3- this
4 - that 
5 - 12 (temp. keep in mind your assembly uses this space on translation to machine language)
13 - 15 (general purpose)
16 - 255 (static variables)
255 ... (stack data)

notice we dont set a value for static because that's already taken care of by our assembler as it encounters static label types in the code. We set the base register to 16 for dealing with noninteger type labels in our assembler.

Also note that in our assembler it already recognizes certain predefined symbols like SP, ARG, LCL, THIS, THAT so you don't really need to set thoe in your translator (woops).

Also note that TEMP is not specified in the assembler (has no knowledge) but the VM language is deciding to map it to 5 (starting). 

Memory commands

push - pushes data onto the stack from a memory segment (or constant)
pop - pops data off the stack and into a memory segment

Operations

arithmetic: add, sub, neg
logical: and, or, not, gt, eq, lt

All together, what the different commands are supposed to do: 

push constant 1
push argument 0
push argument 1
pop argument 0 
pop constant 0 (invalid)
pop this 0 (put value at top of stack into this segment)
push pointer 0 (pushes THIS)
push pointer 1 (pushes THAT)
add 
not

questions

* how many slots does segments like local, argument need? Is there a range? 

## Project 7: Function Calls

### goto commands and conditionals

### function calls
