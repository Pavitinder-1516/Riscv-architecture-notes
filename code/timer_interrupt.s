# Week 8: bare-metal machine-timer interrupt + GPIO toggle (RV32I + Zicsr)
# Addresses follow the SiFive / QEMU convention; change them for your SoC.
        .equ MTIMECMP,  0x02004000
        .equ MTIME,     0x0200BFF8
        .equ GPIO_OUT,  0x1001200C
        .equ TICK,      1000000

        .section .text.init
        .globl _start
_start:
        la    sp, _stack_top          # provided by the linker script
        la    t0, trap_handler
        csrw  mtvec, t0               # direct mode
        jal   ra, set_next_tick
        li    t0, (1 << 7)
        csrs  mie, t0                 # MTIE
        csrsi mstatus, (1 << 3)       # MIE
idle:   wfi
        j     idle

set_next_tick:
        li    t0, MTIME
        lw    t1, 0(t0)               # low word of mtime (simplified)
        li    t2, TICK
        add   t1, t1, t2
        li    t0, MTIMECMP
        li    t2, -1
        sw    t2, 4(t0)               # avoid a spurious match while updating
        sw    t1, 0(t0)
        sw    x0, 4(t0)
        ret

        .align 2                      # mtvec needs 4-byte alignment
trap_handler:
        addi  sp, sp, -16             # step 9 - save
        sw    ra, 12(sp)
        sw    t0,  8(sp)
        sw    t1,  4(sp)
        sw    t2,  0(sp)

        csrr  t0, mcause              # step 10 - service
        bgez  t0, trap_done           # exception: ignore in this demo
        jal   ra, set_next_tick       # clears MTIP
        li    t0, GPIO_OUT
        lw    t1, 0(t0)
        xori  t1, t1, 1               # toggle LED on pin 0
        sw    t1, 0(t0)

trap_done:
        lw    t2,  0(sp)              # step 11 - restore
        lw    t1,  4(sp)
        lw    t0,  8(sp)
        lw    ra, 12(sp)
        addi  sp, sp, 16
        mret                          # step 12 - return
