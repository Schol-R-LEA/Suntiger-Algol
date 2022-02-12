# Baby Algol output file examples/assign-test.s

.text
.globl main
main:
	la $a0, ps
	li $v0, 4
	syscall
# Program Start

	move $t1, $zero
	la $t0, lit0
	lw $t1, 0($t0)
	sw $t1, -24($sp)
	move $t1, $zero
	la $t0, lit1
	lb $t1, 0($t0)
	sb $t1, -28($sp)
	move $t1, $zero
	la $t0, lit2
	lb $t1, 0($t0)
	sb $t1, -32($sp)
	la $t0, lit3
	sw $t0, -36($sp)
	move $a0, $zero
	lw $a0, -24($sp)
	li $v0, 1
	syscall
	la $a0, nl
	li $v0, 4
	syscall
	move $t1, $zero
	lb $t1, -28($sp)
	sb $t1, charSwap
	la $a0, charSwap
	li $v0, 4
	syscall
	la $a0, nl
	li $v0, 4
	syscall
	lw $a0, -36($sp)
	li $v0, 4
	syscall
	la $a0, nl
	li $v0, 4
	syscall
	move $a0, $zero
	lb $a0, -32($sp)
	la $t0, boolLookup
	sll $a0, $a0, 2
	add $t0, $a0, $t0
	lw $a0, 0($t0)
	li $v0, 4
	syscall
	la $a0, nl
	li $v0, 4
	syscall
	move $t1, $zero
	la $t0, lit0
	lw $t1, 0($t0)
	move $t2, $zero
	la $t0, lit0
	lw $t2, 0($t0)
	sub $t1, $t1, $t2
	beq $zero, $t1, true.0
	move $t3, $zero
	j false.1
true.0:
	li $t1, 1
	move $t3, $t1
false.1:
	move $a0, $zero
	move $a0, $t3
	la $t0, boolLookup
	sll $a0, $a0, 2
	add $t0, $a0, $t0
	lw $a0, 0($t0)
	li $v0, 4
	syscall
	la $a0, nl
	li $v0, 4
	syscall
	move $t1, $zero
	la $t0, lit0
	lw $t1, 0($t0)
	move $t2, $zero
	la $t0, lit4
	lw $t2, 0($t0)
	sub $t1, $t1, $t2
	beq $zero, $t1, true.2
	move $t3, $zero
	j false.3
true.2:
	li $t1, 1
	move $t3, $t1
false.3:
	move $a0, $zero
	move $a0, $t3
	la $t0, boolLookup
	sll $a0, $a0, 2
	add $t0, $a0, $t0
	lw $a0, 0($t0)
	li $v0, 4
	syscall
	la $a0, nl
	li $v0, 4
	syscall
	move $t1, $zero
	la $t0, lit0
	lw $t1, 0($t0)
	move $t2, $zero
	la $t0, lit0
	lw $t2, 0($t0)
	sub $t1, $t1, $t2
	bne $zero, $t1, true.4
	move $t3, $zero
	j false.5
true.4:
	li $t1, 1
	move $t3, $t1
false.5:
	move $a0, $zero
	move $a0, $t3
	la $t0, boolLookup
	sll $a0, $a0, 2
	add $t0, $a0, $t0
	lw $a0, 0($t0)
	li $v0, 4
	syscall
	la $a0, nl
	li $v0, 4
	syscall
	move $t1, $zero
	la $t0, lit0
	lw $t1, 0($t0)
	move $t2, $zero
	la $t0, lit4
	lw $t2, 0($t0)
	sub $t1, $t1, $t2
	bne $zero, $t1, true.6
	move $t3, $zero
	j false.7
true.6:
	li $t1, 1
	move $t3, $t1
false.7:
	move $a0, $zero
	move $a0, $t3
	la $t0, boolLookup
	sll $a0, $a0, 2
	add $t0, $a0, $t0
	lw $a0, 0($t0)
	li $v0, 4
	syscall
	la $a0, nl
	li $v0, 4
	syscall
	move $t1, $zero
	la $t0, lit0
	lw $t1, 0($t0)
	move $t2, $zero
	la $t0, lit4
	lw $t2, 0($t0)
	sub $t1, $t1, $t2
	blez $t1, true.8
	move $t3, $zero
	j false.9
true.8:
	li $t1, 1
	move $t3, $t1
false.9:
	move $a0, $zero
	move $a0, $t3
	la $t0, boolLookup
	sll $a0, $a0, 2
	add $t0, $a0, $t0
	lw $a0, 0($t0)
	li $v0, 4
	syscall
	la $a0, nl
	li $v0, 4
	syscall
	move $t1, $zero
	la $t0, lit0
	lw $t1, 0($t0)
	move $t2, $zero
	la $t0, lit4
	lw $t2, 0($t0)
	sub $t1, $t1, $t2
	bgtz $t1, true.10
	move $t3, $zero
	j false.11
true.10:
	li $t1, 1
	move $t3, $t1
false.11:
	move $a0, $zero
	move $a0, $t3
	la $t0, boolLookup
	sll $a0, $a0, 2
	add $t0, $a0, $t0
	lw $a0, 0($t0)
	li $v0, 4
	syscall
	la $a0, nl
	li $v0, 4
	syscall
	move $t1, $zero
	la $t0, lit0
	lw $t1, 0($t0)
	move $t2, $zero
	la $t0, lit0
	lw $t2, 0($t0)
	sub $t1, $t1, $t2
	beq $zero, $t1, true.12
	move $t3, $zero
	j false.13
true.12:
	li $t1, 1
	move $t3, $t1
false.13:
	move $t1, $zero
	la $t0, lit4
	lw $t1, 0($t0)
	move $t2, $zero
	la $t0, lit5
	lw $t2, 0($t0)
	sub $t1, $t1, $t2
	blez $t1, true.14
	move $t4, $zero
	j false.15
true.14:
	li $t1, 1
	move $t4, $t1
false.15:
	move $t1, $zero
	move $t1, $t3
	move $t2, $zero
	move $t2, $t4
	and $t1, $t1, $t2
	move $t5, $t1
	move $a0, $zero
	move $a0, $t5
	la $t0, boolLookup
	sll $a0, $a0, 2
	add $t0, $a0, $t0
	lw $a0, 0($t0)
	li $v0, 4
	syscall
	la $a0, nl
	li $v0, 4
	syscall
	move $t1, $zero
	la $t0, lit6
	lw $t1, 0($t0)
	move $t2, $zero
	la $t0, lit4
	lw $t2, 0($t0)
	mult $t1, $t2
	mfhi $t1
	mflo $t2
	move $t3, $t2
	move $a0, $zero
	move $a0, $t3
	li $v0, 1
	syscall
	la $a0, nl
	li $v0, 4
	syscall
	move $t1, $zero
	la $t0, lit7
	lw $t1, 0($t0)
	move $t2, $zero
	la $t0, lit5
	lw $t2, 0($t0)
	div $t1, $t2
	mflo $t1
	move $t3, $t1
	move $t1, $zero
	move $t1, $t3
	sw $t1, -24($sp)
	move $a0, $zero
	lw $a0, -24($sp)
	li $v0, 1
	syscall
	la $a0, nl
	li $v0, 4
	syscall
	move $t1, $zero
	lw $t1, -24($sp)
	move $t2, $zero
	la $t0, lit8
	lw $t2, 0($t0)
	add $t1, $t1, $t2
	move $t3, $t1
	move $t1, $zero
	move $t1, $t3
	sw $t1, -24($sp)
	move $a0, $zero
	lw $a0, -24($sp)
	li $v0, 1
	syscall
	la $a0, nl
	li $v0, 4
	syscall
	move $t1, $zero
	lw $t1, -24($sp)
	move $t2, $zero
	la $t0, lit9
	lw $t2, 0($t0)
	sub $t1, $t1, $t2
	move $t3, $t1
	move $t1, $zero
	move $t1, $t3
	sw $t1, -24($sp)
	move $t1, $zero
	lw $t1, -24($sp)
	move $t2, $zero
	la $t0, lit10
	lw $t2, 0($t0)
	sub $t1, $t1, $t2
	beq $zero, $t1, true.16
	move $t3, $zero
	j false.17
true.16:
	li $t1, 1
	move $t3, $t1
false.17:
	move $a0, $zero
	move $a0, $t3
	la $t0, boolLookup
	sll $a0, $a0, 2
	add $t0, $a0, $t0
	lw $a0, 0($t0)
	li $v0, 4
	syscall
	la $a0, nl
	li $v0, 4
	syscall
	move $t1, $zero
	la $t0, lit4
	lw $t1, 0($t0)
	move $t2, $zero
	la $t0, lit5
	lw $t2, 0($t0)
	mult $t1, $t2
	mfhi $t1
	mflo $t2
	move $t3, $t2
	move $t1, $zero
	move $t1, $t3
	move $t2, $zero
	lw $t2, -24($sp)
	mult $t1, $t2
	mfhi $t1
	mflo $t2
	move $t4, $t2
	move $t1, $zero
	lw $t1, -24($sp)
	move $t2, $zero
	move $t2, $t4
	add $t1, $t1, $t2
	move $t5, $t1
	move $t1, $zero
	lw $t1, -24($sp)
	move $t2, $zero
	la $t0, lit4
	lw $t2, 0($t0)
	div $t1, $t2
	mflo $t1
	move $t6, $t1
	move $t1, $zero
	move $t1, $t5
	move $t2, $zero
	move $t2, $t6
	add $t1, $t1, $t2
	move $t7, $t1
	move $a0, $zero
	move $a0, $t7
	li $v0, 1
	syscall

# Program End
	la $a0, pe
	li $v0, 4
	syscall
	li $v0, 10
	syscall
.data
	ps:	.asciiz "RUNNING PROGRAM\n"
	pe:	.asciiz "\nPROGRAM ENDED\n"
	nl:	.asciiz "\n"
	sFalse:	.asciiz	"FALSE"
	sTrue:	.asciiz	"TRUE"
	boolLookup:	.word	sFalse, sTrue

	charSwap:	.space 1
		.byte 0
.align 4

	lit0:	.word	1
	lit1:	.asciiz	"a"
.align 4
	lit2:	.byte	0
.align 4
	lit3:	.asciiz	"Hello, World!"
.align 4
	lit4:	.word	2
	lit5:	.word	3
	lit6:	.word	10
	lit7:	.word	6
	lit8:	.word	42
	lit9:	.word	23
	lit10:	.word	21
