# Baby Algol output file examples/if-test.s

.text
.globl main
main:
	la $a0, ps
	li $v0, 4
	syscall
# Program Start

	move $t1, $zero
	la $t0, lit0
	lb $t1, 0($t0)
	sb $t1, charSwap
	la $a0, charSwap
	li $v0, 4
	syscall
	la $a0, nl
	li $v0, 4
	syscall
	move $t1, $zero
	la $t0, lit1
	lw $t1, 0($t0)
	move $t2, $zero
	la $t0, lit1
	lw $t2, 0($t0)
	sub $t1, $t1, $t2
	beq $zero, $t1, true.0
	move $t3, $zero
	j false.1
true.0:
	li $t1, 1
	move $t3, $t1
false.1:
	move $t1, $zero
	move $t1, $t3
	beq $zero, $t1, else.2
	la $a0, lit2
	li $v0, 4
	syscall
else.2:
	la $a0, nl
	li $v0, 4
	syscall
	move $t1, $zero
	la $t0, lit3
	lb $t1, 0($t0)
	sb $t1, charSwap
	la $a0, charSwap
	li $v0, 4
	syscall
	la $a0, nl
	li $v0, 4
	syscall
	move $t1, $zero
	la $t0, lit1
	lw $t1, 0($t0)
	move $t2, $zero
	la $t0, lit1
	lw $t2, 0($t0)
	sub $t1, $t1, $t2
	bne $zero, $t1, true.3
	move $t3, $zero
	j false.4
true.3:
	li $t1, 1
	move $t3, $t1
false.4:
	move $t1, $zero
	move $t1, $t3
	beq $zero, $t1, else.5
	la $a0, lit4
	li $v0, 4
	syscall
else.5:
	la $a0, nl
	li $v0, 4
	syscall
	move $t1, $zero
	la $t0, lit5
	lb $t1, 0($t0)
	sb $t1, charSwap
	la $a0, charSwap
	li $v0, 4
	syscall
	la $a0, nl
	li $v0, 4
	syscall
	move $t1, $zero
	la $t0, lit1
	lw $t1, 0($t0)
	move $t2, $zero
	la $t0, lit1
	lw $t2, 0($t0)
	sub $t1, $t1, $t2
	bne $zero, $t1, true.6
	move $t3, $zero
	j false.7
true.6:
	li $t1, 1
	move $t3, $t1
false.7:
	move $t1, $zero
	move $t1, $t3
	beq $zero, $t1, else.8
	la $a0, lit4
	li $v0, 4
	syscall
	j fi.9
else.8:
	la $a0, lit2
	li $v0, 4
	syscall
fi.9:
	la $a0, nl
	li $v0, 4
	syscall
	move $t1, $zero
	la $t0, lit6
	lb $t1, 0($t0)
	sb $t1, charSwap
	la $a0, charSwap
	li $v0, 4
	syscall
	la $a0, nl
	li $v0, 4
	syscall
	move $t1, $zero
	la $t0, lit1
	lw $t1, 0($t0)
	sw $t1, -24($sp)
	move $t1, $zero
	lw $t1, -24($sp)
	move $t2, $zero
	la $t0, lit1
	lw $t2, 0($t0)
	sub $t1, $t1, $t2
	bne $zero, $t1, true.10
	move $t3, $zero
	j false.11
true.10:
	li $t1, 1
	move $t3, $t1
false.11:
	move $t1, $zero
	move $t1, $t3
	beq $zero, $t1, else.12
	la $a0, lit4
	li $v0, 4
	syscall
	j fi.13
else.12:
	la $a0, lit2
	li $v0, 4
	syscall
fi.13:
	la $a0, nl
	li $v0, 4
	syscall
	move $t1, $zero
	la $t0, lit7
	lb $t1, 0($t0)
	sb $t1, charSwap
	la $a0, charSwap
	li $v0, 4
	syscall
	la $a0, nl
	li $v0, 4
	syscall
	move $t1, $zero
	la $t0, lit8
	lb $t1, 0($t0)
	beq $zero, $t1, else.14
	move $a0, $zero
	la $t0, lit8
	lb $a0, 0($t0)
	la $t0, boolLookup
	sll $a0, $a0, 2
	add $t0, $a0, $t0
	lw $a0, 0($t0)
	li $v0, 4
	syscall
	j fi.15
else.14:
	move $a0, $zero
	la $t0, lit9
	lb $a0, 0($t0)
	la $t0, boolLookup
	sll $a0, $a0, 2
	add $t0, $a0, $t0
	lw $a0, 0($t0)
	li $v0, 4
	syscall
fi.15:
	la $a0, nl
	li $v0, 4
	syscall
	move $t1, $zero
	la $t0, lit10
	lb $t1, 0($t0)
	sb $t1, charSwap
	la $a0, charSwap
	li $v0, 4
	syscall
	la $a0, nl
	li $v0, 4
	syscall
	move $t1, $zero
	la $t0, lit1
	lw $t1, 0($t0)
	move $t2, $zero
	la $t0, lit11
	lw $t2, 0($t0)
	sub $t1, $t1, $t2
	blez $t1, true.16
	move $t3, $zero
	j false.17
true.16:
	li $t1, 1
	move $t3, $t1
false.17:
	move $t1, $zero
	move $t1, $t3
	beq $zero, $t1, else.18
	la $a0, lit12
	li $v0, 4
	syscall
else.18:
	la $a0, nl
	li $v0, 4
	syscall
	move $t1, $zero
	la $t0, lit13
	lb $t1, 0($t0)
	sb $t1, charSwap
	la $a0, charSwap
	li $v0, 4
	syscall
	la $a0, nl
	li $v0, 4
	syscall
	move $t1, $zero
	la $t0, lit1
	lw $t1, 0($t0)
	move $t2, $zero
	la $t0, lit11
	lw $t2, 0($t0)
	sub $t1, $t1, $t2
	blez $t1, true.19
	move $t3, $zero
	j false.20
true.19:
	li $t1, 1
	move $t3, $t1
false.20:
	move $t1, $zero
	la $t0, lit14
	lw $t1, 0($t0)
	move $t2, $zero
	la $t0, lit15
	lw $t2, 0($t0)
	sub $t1, $t1, $t2
	bgtz $t1, true.21
	move $t4, $zero
	j false.22
true.21:
	li $t1, 1
	move $t4, $t1
false.22:
	move $t1, $zero
	move $t1, $t3
	move $t2, $zero
	move $t2, $t4
	and $t1, $t1, $t2
	move $t5, $t1
	move $t1, $zero
	move $t1, $t5
	beq $zero, $t1, else.23
	la $a0, lit16
	li $v0, 4
	syscall
else.23:
	la $a0, nl
	li $v0, 4
	syscall
	move $t1, $zero
	la $t0, lit17
	lb $t1, 0($t0)
	sb $t1, charSwap
	la $a0, charSwap
	li $v0, 4
	syscall
	la $a0, nl
	li $v0, 4
	syscall
	move $t1, $zero
	la $t0, lit1
	lw $t1, 0($t0)
	move $t2, $zero
	la $t0, lit11
	lw $t2, 0($t0)
	sub $t1, $t1, $t2
	blez $t1, true.24
	move $t3, $zero
	j false.25
true.24:
	li $t1, 1
	move $t3, $t1
false.25:
	move $t1, $zero
	la $t0, lit14
	lw $t1, 0($t0)
	move $t2, $zero
	la $t0, lit15
	lw $t2, 0($t0)
	sub $t1, $t1, $t2
	bgtz $t1, true.26
	move $t4, $zero
	j false.27
true.26:
	li $t1, 1
	move $t4, $t1
false.27:
	move $t1, $zero
	move $t1, $t3
	move $t2, $zero
	move $t2, $t4
	and $t1, $t1, $t2
	move $t5, $t1
	move $t1, $zero
	move $t1, $t5
	move $t2, $zero
	la $t0, lit8
	lb $t2, 0($t0)
	or $t1, $t1, $t2
	move $t6, $t1
	move $t1, $zero
	move $t1, $t6
	beq $zero, $t1, else.28
	la $a0, lit18
	li $v0, 4
	syscall
else.28:
	la $a0, nl
	li $v0, 4
	syscall
	move $t1, $zero
	la $t0, lit19
	lb $t1, 0($t0)
	sb $t1, charSwap
	la $a0, charSwap
	li $v0, 4
	syscall
	la $a0, nl
	li $v0, 4
	syscall
	move $t1, $zero
	la $t0, lit8
	lb $t1, 0($t0)
	move $t2, $zero
	la $t0, lit8
	lb $t2, 0($t0)
	and $t1, $t1, $t2
	move $t3, $t1
	move $t1, $zero
	move $t1, $t3
	beq $zero, $t1, else.29
	la $a0, lit20
	li $v0, 4
	syscall
else.29:
	la $a0, nl
	li $v0, 4
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

	lit0:	.asciiz	"a"
.align 4
	lit1:	.word	1
	lit2:	.asciiz	"1 == 1"
.align 4
	lit3:	.asciiz	"b"
.align 4
	lit4:	.asciiz	"1 != 1"
.align 4
	lit5:	.asciiz	"c"
.align 4
	lit6:	.asciiz	"d"
.align 4
	lit7:	.asciiz	"e"
.align 4
	lit8:	.byte	1
.align 4
	lit9:	.byte	0
.align 4
	lit10:	.asciiz	"f"
.align 4
	lit11:	.word	2
	lit12:	.asciiz	"1 < 2"
.align 4
	lit13:	.asciiz	"g"
.align 4
	lit14:	.word	3
	lit15:	.word	4
	lit16:	.asciiz	"1 < 2 && 3 > 4"
.align 4
	lit17:	.asciiz	"h"
.align 4
	lit18:	.asciiz	"(1 < 2) && (3 > 4) || true"
.align 4
	lit19:	.asciiz	"i"
.align 4
	lit20:	.asciiz	"true && true"
.align 4
