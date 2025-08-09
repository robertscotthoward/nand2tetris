// BIG GOAL
// R2 = R0 * R1
// Don't change R0 or R1



// R2 = 0
@0
D=A
@R2
M=D

// R3 = R1
@R1
D=M
@R3
M=D

// Loop until R3 = 0
//   R2 = R2 + R0
(LOOP)

// If R3 = 0 jump to QUIT
@R3
D=M
@QUIT
D;JEQ

// R2 = R2 + R0
@R0
D=M
@R2
M=D+M

// R3 = R3 - 1
@R3
M=M-1

// Repeat
@LOOP
0;JMP


(QUIT)
@QUIT
0;JEQ
