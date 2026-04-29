// Test Program: Add 1 to 5
@5          // A-instruction: number
D = A       

@count      // Variable: will be RAM 16
M = D       

(LOOP)      // Label: Address 4
    @count
    D = M
    
    @END
    D ; JEQ  // Jump if count is 0
    
    @count
    M = M - 1
    
    @LOOP
    0 ; JMP  // Loop back
    
(END)
    @END
    0 ; JMP