/*
 * This is the template program you should use for project 1, where you implement
 * blue hen hash. You should create a total of 4 different procedures as described
 * in the project description for full credit. Remember to document all of the
 * registers used by each of your procedures. You should also describe what each line
 * of code does.
 */
.data
	prompt: .asciz "Enter a message: "
	prompt_size = .-prompt
	input_max_size = 64
	hex_table: .asciz "0123456789ABCDEF"

.bss
	input: .space input_max_size
	output: .space 16

.text
.global _start
_start:
main:
	// Write sys call prints prompt message
	mov x0, #1
	ldur x1, =prompt
	ldur x2, =prompt_size
	mov x8, 0x40
	svc 0

	// Read sys call gets user input
	// the size of the string entered by the user is store in x0 after the service call.
	// The read sys call includes a \n (new line) character at the end. Be sure to
	// discard the new line character and only hash the text entered by the user!
	mov x0, #1
	ldur x1, =input
	ldur x2, =input_max_size
	mov x8, 0x3f
	svc 0

	mov x4, x0 
	//I WROTE THIS TO STORE RETURN INPUT INTO X4
	
	

	//mov x0, #1
	//ldur x1, =input
	//mov x2, x4
	//mov x8, 0x40
	//svc 0

	
	bl blue_hen_hash

	// Call print_hex function. 0x1234567890abcdef is a place holder value.
	// You should replace x0 with the return value of blue_hen_hash.
	// blue_hen_hash should hash the user's input
	
	//mov x0, 0x1234567890abcdef
	bl print_hex
	b exit

	exit:
	// Exit sys call terminates program
	mov x8, #93
	svc 0

//
 // ---------- print_hex ----------
 // Parameters:
 //	x0 - 8 bit value to be printed
 // Uses saved registers:
 //	x17 - address of hex table
 //	x18 - address of output table
 //	x19 - copy of 8 byte value to be printed
 //	x20	- for loop counter tracking offset
 //  x21 - stopping value constant for the for loop
 // Returns: void
 //
print_hex:
	ldur x17, =hex_table
	ldur x18, =output
	mov x19, x0
	mov x20, XZR
	mov x21, #64
	print_hex_loop:
	// loop for i=0; i<64; i+=4
	mov x0, x19
	mov x1, x20
	cmp x20, x21
	b.ge print_hex_done
	// get bits at i position
	bl extract_hex_bits
	// calculate index into hex_table of the 4 bit value at the ith position
	add x9, x17, x0
	// get the character from the hex table
	ldurb x10, [x9]
	// store the character we got into the output buffer to print later
	sturb x10, [x18]
	// increase our counters
	add x18, x18, #1
	add x20, x20, #4
	b print_hex_loop
	print_hex_done:
	mov x0, #1
	// Write sys call prints hex string
	ldur x1, =output
	mov x2, #16
	mov x8, 0x40
	svc 0
	b exit

//
// ---------- extract_hex_bits ----------
// Parameters:
//  x0 - 8 byte number we are extracting bits from
//  x1 - start offset from the left we want to extract from
// Returns: x0 - the 4 bit value
//
extract_hex_bits:
	// calculate right offset
	mov x10, #60
	sub x10, x10, x1
	// discard left bits
	lsl x0, x0, x1
	// offset back to original position
	lsr x0, x0, x1
	// offset to right align bits
	lsr x0, x0, x10
	br lr

//
 // ---- pad_message (LEAF PROCEDURE) ---
 // Notes:
 //  Does not pad the message if the length of user input is already a multiple of 8 bytes
 // Parameters:
 //	x0 - base address of user input
 //  x1 - length of user input
 // Side Effects:
 //  mutate the input inside of the .data section, applying 1-bit padding
 // Returns:
 //  x0 - new length of user input (should be a multiple of black size)(b, c) - a
 //
pad_message:
	//I used the a mix of saved and temporary registers in this function because of the lack of registers offered in the armsimulator.
	
	//Will calculate mod like this: remainder = dividend - quotient x divisor
	mov x2, 8 
	//This will be the divisor in calculating the mod of the input size

	sub x4, x4, #1
	//the dividend is in x4; we will remove the \n byte from the length by substracting one from the length of the input


	udiv x3, x4, x2 
	// x3 = input_size / 8 //this is the quotient
	//msub x5, x3, x2, x4 
	mul x3, x3, x2
	sub x5, x4, x3
	//remainder = dividend - quotient x divisor

	cmp x5, #0
	b.eq ret_mod_zero
	//If length is a multiple of 8, no padding is done since in later functions the \n character in position 9 (using the length of 8 example) will be disregarded	

	sub x9, x2, x5
	//calculate how much padding is required, store value in x9

	ldur x12, =input
	//loading the address of the input into register x12
	add x13, x12, x4
	//x13 = &input + length of message
	mov x10, #0x80
	sturb x10, [x13, #0] 
	//replace \n at last position with 0x80
	

	add x0, x4, x9
	//x0 (return value) = new length of user input (length inputted + padding)

	BR LR
	//return to caller



ret_mod_zero:
	mov x0, x4	
	//x0 (return value) = new length of user input (length inputted + padding)

	
	BR LR
	//return to caller

//
// ---- blue_hen_prf (LEAF PROCEDURE) ---
// Notes:
 //  Keep in mind the addition operations used in this function are on 4 byte values.
 //  Be sure to properly handle overflow!
 // Parameters:
 //	x0 - block (8 bytes)
 //  x1 - right (4 bytes)
// Returns:
 //  x0 - computed output (we are only interested in the lowest 4 bytes of this register)
 //
blue_hen_prf:
//I used the a mix of saved and temporary registers in this function because of the lack of registers offered in the armsimulator.
lsl x2, x0, #32
lsr x2, x2, #32
//x2 = block_high

lsr x3, x0, #32
//x3 = block_low

add x4, x1, x3
//x4 (out) = right + block_low
mov x10, #0xFFFFFFFF

and x4, x4, x10
//x4 (out) = (right + block_low) & 0xFFFFFFFF

//CODE BELOW WAS PART OF OLD PYTHON
//udiv x9, x4, x10
//mul x9, x9, x10
//sub x4, x4, x9
//x4 (out) = (right + block_low) % 0xFFFFFFFF

lsl x11, x4, #8
and x11, x11, x10
//x11 = (out << 8) & 0xFFFFFFFF

lsr x12, x4, #24
//x12 = (out >> (32-8))
and x12, x12, x10
// x12 = x12 & 0xFFFFFFFF

orr x4, x12, x11
//x4 = (((out << 8) & 0xFFFFFFFF) | ((out >> (HALF_BLOCK_BIT_SIZE - 8)) & 0xFFFFFFFF))

and x4, x4, x10
//x4 = (((out << 8) & 0xFFFFFFFF) | ((out >> (HALF_BLOCK_BIT_SIZE - 8)) & 0xFFFFFFFF)) & 0xFFFFFFFF

//CODE BELOW WAS PART OF OLD PYTHON
//udiv x9, x4, x10
//mul x9, x9, x10
//sub x4, x4, x9
//x4 = (((out << 8) & 0xFFFFFFFF) | ((out >> (HALF_BLOCK_BIT_SIZE - 8)) & 0xFFFFFFFF)) % 0xFFFFFFFF

add x4, x4, x2
//x4 = out + block_high
and x4, x4, x10
//x4 = (out + block_high) & 0xFFFFFFFF

//CODE BELOW WAS PART OF OLD PYTHON
//udiv x9, x4, x10
//mul x9, x9, x10
//sub x4, x4, x9
//x4 = (out + block_high) % 0xFFFFFFFF

lsr x11, x4, #3
and x11, x11, x10
//x11 = ((out >> 3) & 0xFFFFFFFF)

lsl x12, x4, #29
and x12, x12, x10
//x12 = ((out << (32 - 3)) & 0xFFFFFFFF)

orr x4, x11, x12
//out = (((out >> 3) & 0xFFFFFFFF) | ((out << (HALF_BLOCK_BIT_SIZE - 3)) & 0xFFFFFFFF))
and x4, x4, x10
//out = (((out >> 3) & 0xFFFFFFFF) | ((out << (HALF_BLOCK_BIT_SIZE - 3)) & 0xFFFFFFFF)) &  0xFFFFFFFF

//CODE BELOW WAS PART OF OLD PYTHON
//udiv x9, x4, x10
//mul x9, x9, x10
//sub x4, x4, x9
//out = (((out >> 3) & 0xFFFFFFFF) | ((out << (HALF_BLOCK_BIT_SIZE - 3)) & 0xFFFFFFFF)) % 0xFFFFFFFF

mov x0, x4
//return out


BR LR
//return to caller


//
 // ---- blue_hen_compression (NON-LEAF PROCEDURE) ---
 // Parameters:
 //	x0 - h, the current hash value
 //  x1 - block, the current chunk of user input being processed
// Returns:
 //  x0 - compressed block
 //
blue_hen_compression:
//I used the a mix of saved and temporary registers in this function because of the lack of registers offered in the armsimulator.
mov x14, x1
//x14 = block

lsl x5, x0, #32
lsr x5, x5, #32
//x5 (left) = h[:HALF_BLOCK_SIZE]

lsr x6, x0, #32
//x6 (right) = h[HALF_BLOCK_SIZE:]


mov x15, lr
//save return address in x15
mov x13, #0
//iterator in compression_loop
compression_loop:
//for loop in compression function
mov x7, x6
//x7 (next left) = right

mov x0, x14
//x0 = block (parameter for blue_hen_prf)
mov x1, x6
// x1 = right (parameter for blue_hen_ptf)
bl blue_hen_prf
mov x8, x0
//x8 (next right) = blue_hen_prf(block, right)

eor x8, x5, x8
//next_right = bytes(x ^ y for x, y in zip(left, next_right))

mov x5, x7
mov x6, x8
//left, right = next_left, next_right

add x13, x13, #1
cmp x13, #4
b.lt compression_loop
//stay in loop for 4 iterations

lsl x6, x6, #32
orr x0, x5, x6
//output = left + right // this output is being returned
mov lr, x15
//restore LR value
BR LR
//return to caller 






//
 // ---- blue_hen_hash (NON-LEAF PROCEDURE) ---
 // Notes:
 //  Calls pad message to extend the user input to a multiple of block size
 //  Loads an IV from the .data segment
 //  Compute hash of message, as described in the project description
 // Parameters:
 //	x0 - base address of user input
 //  x1 - size of user input
 // Returns:
//  x0 - computed hash, of entire message
 //
blue_hen_hash:
//I used the a mix of saved and temporary registers in this function because of the lack of registers offered in the armsimulator.

mov x16, #5639993682373725250
//x16 = b'BLUE_HEN'
ldur x18, =input
//x18 = &input

mov x17, lr
//save return address in x17
bl pad_message
//call pad_message function
mov lr, x17
//restore return address
mov x17, x0
//x17 = return value from pad_message (length of padded input)

mov x21, lr
//save return address
mov x19, #0
//iterator for hash_loop
hash_loop:
//hash function for loop
cmp x19, x17
b.eq exit_loop
// exit_loop if x19 == padded message length
add x20, x18, x19
ldur x20, [x20]
//x20 = padded_message[i:i+BLOCK_SIZE]

mov x0, x16
// h parameter for compression function
mov x1, x20
// block parameter for compression function
bl blue_hen_compression
//call compression function

eor x16, x16, x0
//h = bytes(x ^ y for x, y in zip(h, compressed_block))

add x19, x19, #8
//iterate by 8 in loop
b hash_loop

exit_loop:
mov lr, x21
//restore return address
mov x0, x16
//return value = h
BR LR
//return to caller




