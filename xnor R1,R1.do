    mem load -i C:/Users/ramym/Desktop/smart-attendance-credit/Assembler_Arch_project/microroutines/rom.mem /system/Rom_c/rom
    mem load -filltype value -filldata 0111000001000001 -fillradix binary -skip 0 /system/ram/ram
    add wave -position insertpoint  \
    sim:/system/clk
    add wave -position insertpoint  \
    sim:/system/rst
    add wave -position insertpoint  \
    sim:/system/clkram
    add wave -position insertpoint  \
sim:/system/instruction
    add wave -position end  sim:/system/busA
    add wave -position end  sim:/system/busB
    add wave -position end  sim:/system/busC
    add wave -position end  sim:/system/outRegPcTriIn
    add wave -position end  sim:/system/RegCwOut 
    add wave -position end  sim:/system/PlaMicroARin
    add wave -position end  sim:/system/MicroARout
    add wave -position end  sim:/system/RomCwOut
    add wave -position end sim:/system/ramout
    add wave -position end  sim:/system/muxout
    add wave -position end  sim:/system/ReadWriteDecoder
    add wave -position 14  sim:/system/outRegTemp1TriIn
    add wave -position 15  sim:/system/outRegTemp2TriIn
    add wave -position end sim:/system/OutA
    add wave -position 41  sim:/system/R0outAEn
    add wave -position 25  sim:/system/DecodingCircuitSrcOutput
    force -freeze sim:/system/DecoderEnSrcA 1 0
    force -freeze sim:/system/DecoderEnSrcB 1 0
    force -freeze sim:/system/DecoderEnRnTemp 1 0
    force -freeze sim:/system/DecoderEnMARMDRFlag 1 0
    force -freeze sim:/system/DecoderEnReadWrite 1 0
    force -freeze sim:/system/DecodingCircuitEn 1 0

    force -freeze sim:/system/initMicroAr 0 0

    force -freeze sim:/system/clkram 0 0, 1 {50 ns} -r 100
    force -freeze sim:/system/clk 1 0, 0 {50 ns} -r 100

    add wave -position end  sim:/system/outRegPcTriIn
    force -freeze sim:/system/busC 16'h0001 0
    add wave -position end  sim:/system/RnTempInDecoder
    force -freeze sim:/system/rst 1 0
    force -freeze sim:/system/rst 0 0
    add wave -position end  sim:/system/DecoderEnRnTemp
    force -freeze sim:/system/DecoderEnRnTemp 1 0
    force -freeze sim:/system/rst 1 0
    run
    force -freeze sim:/system/rst 0 0
    add wave -position end  sim:/system/DecoderEnRnTemp
    force -freeze sim:/system/DecoderEnRnTemp 1 0
    run
    add wave -position end  sim:/system/outReg0TriIn
    add wave -position end  sim:/system/outReg1TriIn
    run
    add wave -position 14  sim:/system/R0InCEn
    force -freeze sim:/system/R0InCEn 1 0
    run
    force -freeze sim:/system/R0InCEn 0 0
    add wave -position 15  sim:/system/R1InCEn
    force -freeze sim:/system/R1InCEn 1 0
    force -freeze sim:/system/busC 16'h0077 0

    run
    force -freeze sim:/system/R1InCEn 0 0
    noforce sim:/system/busC
    noforce sim:/system/busA
    noforce sim:/system/busB
    noforce sim:/system/R1InCEn
    noforce sim:/system/R0InCEn
    add wave -position end  sim:/system/PLA_c/initMicroAr
    add wave -position 19  sim:/system/PLA_c/plaEn
    run
    force -freeze sim:/system/initMicroAr 1 0
    run
    run
    run
    add wave -position 22  sim:/system/outRegMDRTriIn
    add wave -position 6  sim:/system/nextAddress
    add wave -position 11  sim:/system/Orvector
    add wave -position 12  sim:/system/outRegIRTriIn
    run
    run
    run
    run