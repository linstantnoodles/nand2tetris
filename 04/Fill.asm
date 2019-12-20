// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Always running
(MAINLOOP)
// (512 * 256) / 16. Number of words in our screen since each word is 16 bits
@8192
D=A
@i
M=D
// Set counter
@c
M=0
// Location of keyboard
// Jump if key is not zero (any key is pressed)
@24576
D=M
@BLACKLOOP
D;JNE

// Jump if key is zero 
@24576
D=M
@WHITELOOP
D;JEQ

@MAINLOOP
0;JMP

(BLACKLOOP)
@i 
D=M 
@c 
D=D-M
// Return to the main loop
@MAINLOOP
D;JLE

// Update the address
@SCREEN 
D=A
@c 
D=D+M
A=D
// -1 in twos complement is 111111... which makes screen black
M=-1
@c
M=M+1

@BLACKLOOP
0;JMP

(WHITELOOP)
@i 
D=M 
@c 
D=D-M
@MAINLOOP
D;JLE

// Update the address
@SCREEN 
D=A
@c 
D=D+M
A=D
M=0
@c
M=M+1

@WHITELOOP
0;JMP
