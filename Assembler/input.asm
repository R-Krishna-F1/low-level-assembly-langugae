// input.asm
@10      // A-instruction (number)
D=A      // C-instruction
@count   // Variable (will be assigned to RAM 16)
M=D
@sum     // Variable (will be assigned to RAM 17)
M=0
(LOOP)   // Label
    @count
    D=M
    @END
    D;JEQ    // Jump if count == 0
    @count
    D=M
    @sum
    M=D+M
    @count
    M=M-1
    @LOOP
    0;JMP    // Infinite loop back to (LOOP)
(END)
    @END
    0;JMP