# Run with tclsh; emulate OpenOCD without touching hardware.
rename source tcl_source
foreach command {source gdb_port tcl_port telnet_port init reset sleep shutdown echo} {
    proc $command args {}
}
set ::env(XIAO_ADAPTER_SERIAL) TEST1234
proc adapter {command value} {
    if {$command ne "serial" || $value ne "TEST1234"} { error "Wrong adapter selected" }
}
proc find args { return ignored }
proc target args { return cpu }
proc cpu args { return running }
proc read_memory {address width count} {
    global registers
    if {$width != 32 || $count != 1} { error "Unexpected memory read" }
    return [list [dict get $registers $address]]
}
proc mww {address value} {
    global registers ignore_writes
    if {$ignore_writes} { return }
    if {$address eq "0x5003e070" && $value == 0x10} {
        dict set registers 0x5003c070 [expr {[dict get $registers 0x5003c070] & ~$value}]
    } elseif {$address eq "0x5003d070" && $value == 0x20} {
        dict set registers 0x5003c070 [expr {[dict get $registers 0x5003c070] | $value}]
    } elseif {$address eq "0x5003c064"} {
        dict set registers $address $value
    } else {
        error "Unexpected memory write: $address / $value"
    }
}
set script [file normalize [file join [file dirname [info script]] \
    ../xiao_otbr_patch/rootfs/usr/local/share/xiao-antenna.cfg]]
foreach initial {0 0x12345678 0xffffffff} {
    set ignore_writes 0
    set registers [dict create 0x5003c064 $initial 0x5003c070 $initial]
    for {set repeat 0} {$repeat < 2} {incr repeat} {
        tcl_source $script
        if {[dict get $registers 0x5003c064] != (($initial & ~0x00ff0000) | 0x00440000)} {
            error "Other pin modes changed"
        }
        if {[dict get $registers 0x5003c070] != (($initial & ~0x10) | 0x20)} {
            error "Other output values changed"
        }
    }
}
set ignore_writes 1
set registers [dict create 0x5003c064 0 0x5003c070 0]
if {![catch {tcl_source $script} message] || $message ne "XIAO antenna switch configuration did not verify"} {
    error "Failed register initialization was not rejected"
}
unset ::env(XIAO_ADAPTER_SERIAL)
if {![catch {tcl_source $script}]} { error "Missing serial was accepted" }
set ::env(XIAO_ADAPTER_SERIAL) {[exit]}
if {![catch {tcl_source $script}]} { error "Invalid serial was accepted" }
puts "Antenna initialization preserves other pins and is repeatable: passed"
