// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// set i register (first available register) to 1
@i   
M=1 

// Set register 2 to 0. This will be our counter
@R2 
M=0 

(LOOP)
// Load contents of i register into D. Remember, computations are only allowed for A and D registers. 
// Technically we could load it into either A or D but D is more appropriate for plain data even though A can also 
// Store non-address data
@i 
D=M 

// If we reached the end of R1, we're done
// Does the jump to end need to happen here? Not 
// necessarily, but it does need to happen before the new 
// result is saved

@R1
D=M-D 
@END 
D;JLT

// At this point, we can compute the new result

@R0
D=M
@R2
M=D+M
@i 
M=M+1
@LOOP
// Hard code 0 so it will always jump
0;JMP 

// Keep spinning
(END)
@END 
0;JMP
