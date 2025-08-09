// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, 
// the screen should be cleared.

//// Replace this comment with your code.


// R0 is the number of addresses we want to fill = 8192
// R1 is a pointer to an address in the screen.
// R2 is the value we want to push to the screen.


// Loop forever
(LOOP)

// If *KBD = 0 go to SETWHITE
@KBD
D=M
@SETWHITE
D;JEQ

(SETBLACK)
D=-1
@R2
M=D

// Go to SETSCREEN
@SETSCREEN
0;JMP

(SETWHITE)
D=0
@R2
M=D

// Go to SETSCREEN
@SETSCREEN
0;JMP




// ================================================================================
// Set the entire screen to the value of R2
(SETSCREEN)

// R0 = 8192
@8192
D=A
@R0
M=D

// @R1 = @SCREEN
@SCREEN
D=A
@R1
M=D

(SETSCREENLOOP)

// *R1 = R2
@R2
D=M
@R1
A=M
M=D

// R1=R1+1
@R1
D=M
D=D+1
M=D

// R0 = R0 - 1
@R0
M=M-1

// If R0 > 0 go to SETSCREENLOOP
@R0
D=M
@SETSCREENLOOP
D;JGT

// Go to LOOP
@LOOP
0;JMP




