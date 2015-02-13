.TITLE 3NAND_2_NP_error_node

.OPTION POST=2 POST_VERSION=2001  $ Generate .tr0 file
.OPTION MTTHRESH=10               $ Multi-core operation if >10 transitor
.OPTION CAPTAB INGOLD=0
.OPTION PROBE                     $ Nanosim requires this line
.PROBE I(I*) V(*)           $ Nanosim requires to specify output node
.PROBE I1(M*) I2(M*) I3(M*) I4(M*) 


.TEMP = 27                    
.param mvdd = 1.8
.TRAN 1p simtime *sweep currentheight1 -67000e-6 -68000e-6 -100e-6
.param currentheight1 = -1100e-6
.param currentheight2 = -0e-6
.param currentheight = -0e-6   ***100e-6 = 0.1mA

*currentdelay1   P_nand_3
*currentdelay2   P_and_3
*currentdelay11  N_nand_3
*currentdelay12  N_and_3
*currentdelay21  CD_3             

VVDD  VDD  0 DC mvdd               
VGND  GND  0 DC 0                  

.param simtime = 80n
.param pw1 = 4n  *it was 2n
.param pw2 = simtime
.param period1 = 4*pw1   *it was 6n
.param period2 = simtime
.param latency1 = 5n
.param latency2 = latency1+2*pw1
.param latency3 = simtime
.param latency4 = simtime


VRESET RESET 0 PULSE(0 mvdd 0n 0n 0n latency1 simtime)

VA A_n 0 PULSE(0 mvdd latency1 0n 0n pw1 period1)
VB B_n 0 PULSE(0 mvdd latency1 0n 0n pw1 period1)
VC C_n 0 PULSE(0 mvdd latency1 0n 0n pw1 period1)


VA_p A_p 0 PULSE(0 mvdd latency2 0n 0n pw1 period1)
VB_p B_p 0 PULSE(0 mvdd latency2 0n 0n pw1 period1)
VC_p C_p 0 PULSE(0 mvdd latency2 0n 0n pw1 period1)

VNA NA_n 0 PULSE(0 mvdd latency3 0n 0n pw2 period2)
VNB NB_n 0 PULSE(0 mvdd latency3 0n 0n pw2 period2)
VNC NC_n 0 PULSE(0 mvdd latency3 0n 0n pw2 period2)

VNA_p NA_p 0 PULSE(0 mvdd latency4 0n 0n pw2 period2)
VNB_p NB_p 0 PULSE(0 mvdd latency4 0n 0n pw2 period2)
VNC_p NC_p 0 PULSE(0 mvdd latency4 0n 0n pw2 period2)


*********************netlist_sim**********************

*********current pulse injection********
***pulse i1 i2 delay rise fall pw period
***P Pipeline i1 - i10   N Pipeline i11 - i20
***AND侧和NAND侧注入pulse时间均为58n

.param pulse_time = 58n
.param currentduration = 0.1e-9  ***0.1ns
.param currentdelay1 = simtime   ***P_nand_3
.param currentdelay2 = simtime   ***P_and_3
.param currentdelay3 = simtime   ***Part1 M1 M2
.param currentdelay4 = simtime   
.param currentdelay5 = pulse_time   ***Part2 M1 M3   
.param currentdelay6 = simtime   ***Part2 M4 M5
.param currentdelay7 = simtime   ***Part2 M5 M6
.param currentdelay8 = simtime   ***Part3 M1 M2
.param currentdelay9 = simtime   ***Part3 M2 M3
.param currentdelay10 = simtime 
.param currentdelay11 = simtime  ***N_nand_3
.param currentdelay12 = simtime  ***N_and_3
.param currentdelay13 = simtime 
.param currentdelay14 = simtime 
.param currentdelay15 = simtime 
.param currentdelay16 = simtime 
.param currentdelay17 = simtime  
.param currentdelay18 = simtime 
.param currentdelay19 = simtime 
.param currentdelay20 = simtime 
.param currentdelay21 = simtime  ***CD_3

i1 gnd net239 PULSE 0 currentheight currentdelay1 0 0 currentduration simtime
i2 gnd net261 PULSE 0 currentheight currentdelay2 0 0 currentduration simtime
i3 gnd net245 PULSE 0 currentheight currentdelay3 0 0 currentduration simtime
i4 gnd net247 PULSE 0 currentheight currentdelay4 0 0 currentduration simtime
i5 gnd net297 PULSE 0 currentheight1 currentdelay5 0 0 currentduration simtime
i6 gnd net0298 PULSE 0 currentheight currentdelay6 0 0 currentduration simtime
i7 gnd net0161 PULSE 0 currentheight currentdelay7 0 0 currentduration simtime
i8 gnd net116 PULSE 0 currentheight currentdelay8 0 0 currentduration simtime
i9 gnd net0336 PULSE 0 currentheight currentdelay9 0 0 currentduration simtime
i10 gnd net0339 PULSE 0 currentheight currentdelay10 0 0 currentduration simtime
i11 gnd net105 PULSE 0 currentheight currentdelay11 0 0 currentduration simtime
i12 gnd net132 PULSE 0 currentheight currentdelay12 0 0 currentduration simtime
i13 gnd net246 PULSE 0 currentheight currentdelay13 0 0 currentduration simtime
i14 gnd net109 PULSE 0 currentheight currentdelay14 0 0 currentduration simtime
i15 gnd net113 PULSE 0 currentheight currentdelay15 0 0 currentduration simtime
i16 gnd net284 PULSE 0 currentheight currentdelay16 0 0 currentduration simtime
i17 gnd net114 PULSE 0 currentheight currentdelay17 0 0 currentduration simtime
i18 gnd net282 PULSE 0 currentheight currentdelay18 0 0 currentduration simtime
i19 gnd net283 PULSE 0 currentheight currentdelay19 0 0 currentduration simtime
i20 gnd net115 PULSE 0 currentheight currentdelay20 0 0 currentduration simtime
i21 gnd net278 PULSE 0 currentheight currentdelay21 0 0 currentduration simtime

*********current pulse injection********

* PWL(time1 volt1, time2 volt2, ...)  $ Lined change (time1 volt1), (time2 volt2) 
* PULSE(v1 v2 tdelay tr tf pw period) $ Square wave
* SIN(voffset vamp freq tdelay)       $ SIN wave

*$ Specify parameter set file
.include "../../../../../rules/rohm180/spice/hspice/bu40n1.mdl"
.lib "../../../../../rules/rohm180/spice/hspice/bu40n1.skw" NT
.lib "../../../../../rules/rohm180/spice/hspice/bu40n1.skw" PT



******计算每个半导体四个端子的平均电流******
.param start_time = 58.000ns
.param end_time = 58.2ns
.param end_time2 = 58.1ns

*****AND Part*****
.MEAS TRAN "i(m97)_avg"  AVG i(m97)  FROM=start_time TO=end_time
.MEAS TRAN "i2(m97)_avg" AVG i2(m97) FROM=start_time TO=end_time
.MEAS TRAN "i3(m97)_avg" AVG i3(m97) FROM=start_time TO=end_time
.MEAS TRAN "i4(m97)_avg" AVG i4(m97) FROM=start_time TO=end_time

.MEAS TRAN "i(m92)_avg"  AVG i(m92)  FROM=start_time TO=end_time
.MEAS TRAN "i2(m92)_avg" AVG i2(m92) FROM=start_time TO=end_time
.MEAS TRAN "i3(m92)_avg" AVG i3(m92) FROM=start_time TO=end_time
.MEAS TRAN "i4(m92)_avg" AVG i4(m92) FROM=start_time TO=end_time

.MEAS TRAN "i(m89)_avg"  AVG i(m89)  FROM=start_time TO=end_time
.MEAS TRAN "i2(m89)_avg" AVG i2(m89) FROM=start_time TO=end_time
.MEAS TRAN "i3(m89)_avg" AVG i3(m89) FROM=start_time TO=end_time
.MEAS TRAN "i4(m89)_avg" AVG i4(m89) FROM=start_time TO=end_time

*****NAND Part*****
.MEAS TRAN "i(m222)_avg"  AVG i(m222)  FROM=start_time TO=end_time
.MEAS TRAN "i2(m222)_avg" AVG i2(m222) FROM=start_time TO=end_time
.MEAS TRAN "i3(m222)_avg" AVG i3(m222) FROM=start_time TO=end_time
.MEAS TRAN "i4(m222)_avg" AVG i4(m222) FROM=start_time TO=end_time

.MEAS TRAN "i(m225)_avg"  AVG i(m225)  FROM=start_time TO=end_time
.MEAS TRAN "i2(m225)_avg" AVG i2(m225) FROM=start_time TO=end_time
.MEAS TRAN "i3(m225)_avg" AVG i3(m225) FROM=start_time TO=end_time
.MEAS TRAN "i4(m225)_avg" AVG i4(m225) FROM=start_time TO=end_time

.MEAS TRAN "i(m94)_avg"  AVG i(m94)  FROM=start_time TO=end_time
.MEAS TRAN "i2(m94)_avg" AVG i2(m94) FROM=start_time TO=end_time
.MEAS TRAN "i3(m94)_avg" AVG i3(m94) FROM=start_time TO=end_time
.MEAS TRAN "i4(m94)_avg" AVG i4(m94) FROM=start_time TO=end_time

.MEAS TRAN "i(m98)_avg"  AVG i(m98)  FROM=start_time TO=end_time
.MEAS TRAN "i2(m98)_avg" AVG i2(m98) FROM=start_time TO=end_time
.MEAS TRAN "i3(m98)_avg" AVG i3(m98) FROM=start_time TO=end_time
.MEAS TRAN "i4(m98)_avg" AVG i4(m98) FROM=start_time TO=end_time

.MEAS TRAN "i(m93)_avg"  AVG i(m93)  FROM=start_time TO=end_time
.MEAS TRAN "i2(m93)_avg" AVG i2(m93) FROM=start_time TO=end_time
.MEAS TRAN "i3(m93)_avg" AVG i3(m93) FROM=start_time TO=end_time
.MEAS TRAN "i4(m93)_avg" AVG i4(m93) FROM=start_time TO=end_time

.MEAS TRAN "i(m90)_avg"  AVG i(m90)  FROM=start_time TO=end_time
.MEAS TRAN "i2(m90)_avg" AVG i2(m90) FROM=start_time TO=end_time
.MEAS TRAN "i3(m90)_avg" AVG i3(m90) FROM=start_time TO=end_time
.MEAS TRAN "i4(m90)_avg" AVG i4(m90) FROM=start_time TO=end_time

.MEAS TRAN "i(m215)_avg"  AVG i(m215)  FROM=start_time TO=end_time
.MEAS TRAN "i2(m215)_avg" AVG i2(m215) FROM=start_time TO=end_time
.MEAS TRAN "i3(m215)_avg" AVG i3(m215) FROM=start_time TO=end_time
.MEAS TRAN "i4(m215)_avg" AVG i4(m215) FROM=start_time TO=end_time

.MEAS TRAN "i(m96)_avg"  AVG i(m96)  FROM=start_time TO=end_time
.MEAS TRAN "i2(m96)_avg" AVG i2(m96) FROM=start_time TO=end_time
.MEAS TRAN "i3(m96)_avg" AVG i3(m96) FROM=start_time TO=end_time
.MEAS TRAN "i4(m96)_avg" AVG i4(m96) FROM=start_time TO=end_time

.MEAS TRAN "i(m219)_avg"  AVG i(m219)  FROM=start_time TO=end_time
.MEAS TRAN "i2(m219)_avg" AVG i2(m219) FROM=start_time TO=end_time
.MEAS TRAN "i3(m219)_avg" AVG i3(m219) FROM=start_time TO=end_time
.MEAS TRAN "i4(m219)_avg" AVG i4(m219) FROM=start_time TO=end_time

.MEAS TRAN "i(m95)_avg"  AVG i(m95)  FROM=start_time TO=end_time
.MEAS TRAN "i2(m95)_avg" AVG i2(m95) FROM=start_time TO=end_time
.MEAS TRAN "i3(m95)_avg" AVG i3(m95) FROM=start_time TO=end_time
.MEAS TRAN "i4(m95)_avg" AVG i4(m95) FROM=start_time TO=end_time

.MEAS TRAN "i(m91)_avg"  AVG i(m91)  FROM=start_time TO=end_time
.MEAS TRAN "i2(m91)_avg" AVG i2(m91) FROM=start_time TO=end_time
.MEAS TRAN "i3(m91)_avg" AVG i3(m91) FROM=start_time TO=end_time
.MEAS TRAN "i4(m91)_avg" AVG i4(m91) FROM=start_time TO=end_time

******计算每个半导体四个端子的平均电流******
  


******计算每个半导体四个端子的平均电荷******


*****AND Part*****
.MEAS TRAN "i(m97)_charge"  INTEGRAL i(m97)  FROM=start_time TO=end_time
.MEAS TRAN "i2(m97)_charge" INTEGRAL i2(m97) FROM=start_time TO=end_time
.MEAS TRAN "i3(m97)_charge" INTEGRAL i3(m97) FROM=start_time TO=end_time
.MEAS TRAN "i4(m97)_charge" INTEGRAL i4(m97) FROM=start_time TO=end_time

.MEAS TRAN "i(m92)_charge"  INTEGRAL i(m92)  FROM=start_time TO=end_time
.MEAS TRAN "i2(m92)_charge" INTEGRAL i2(m92) FROM=start_time TO=end_time
.MEAS TRAN "i3(m92)_charge" INTEGRAL i3(m92) FROM=start_time TO=end_time
.MEAS TRAN "i4(m92)_charge" INTEGRAL i4(m92) FROM=start_time TO=end_time

.MEAS TRAN "i(m89)_charge"  INTEGRAL i(m89)  FROM=start_time TO=end_time
.MEAS TRAN "i2(m89)_charge" INTEGRAL i2(m89) FROM=start_time TO=end_time
.MEAS TRAN "i3(m89)_charge" INTEGRAL i3(m89) FROM=start_time TO=end_time
.MEAS TRAN "i4(m89)_charge" INTEGRAL i4(m89) FROM=start_time TO=end_time

*****NAND Part*****
.MEAS TRAN "i(m222)_charge"  INTEGRAL i(m222)  FROM=start_time TO=end_time
.MEAS TRAN "i2(m222)_charge" INTEGRAL i2(m222) FROM=start_time TO=end_time
.MEAS TRAN "i3(m222)_charge" INTEGRAL i3(m222) FROM=start_time TO=end_time
.MEAS TRAN "i4(m222)_charge" INTEGRAL i4(m222) FROM=start_time TO=end_time

.MEAS TRAN "i(m225)_charge"  INTEGRAL i(m225)  FROM=start_time TO=end_time
.MEAS TRAN "i2(m225)_charge" INTEGRAL i2(m225) FROM=start_time TO=end_time
.MEAS TRAN "i3(m225)_charge" INTEGRAL i3(m225) FROM=start_time TO=end_time
.MEAS TRAN "i4(m225)_charge" INTEGRAL i4(m225) FROM=start_time TO=end_time

.MEAS TRAN "i(m94)_charge"  INTEGRAL i(m94)  FROM=start_time TO=end_time
.MEAS TRAN "i2(m94)_charge" INTEGRAL i2(m94) FROM=start_time TO=end_time
.MEAS TRAN "i3(m94)_charge" INTEGRAL i3(m94) FROM=start_time TO=end_time
.MEAS TRAN "i4(m94)_charge" INTEGRAL i4(m94) FROM=start_time TO=end_time

.MEAS TRAN "i(m98)_charge"  INTEGRAL i(m98)  FROM=start_time TO=end_time
.MEAS TRAN "i2(m98)_charge" INTEGRAL i2(m98) FROM=start_time TO=end_time
.MEAS TRAN "i3(m98)_charge" INTEGRAL i3(m98) FROM=start_time TO=end_time
.MEAS TRAN "i4(m98)_charge" INTEGRAL i4(m98) FROM=start_time TO=end_time

.MEAS TRAN "i(m93)_charge"  INTEGRAL i(m93)  FROM=start_time TO=end_time
.MEAS TRAN "i2(m93)_charge" INTEGRAL i2(m93) FROM=start_time TO=end_time
.MEAS TRAN "i3(m93)_charge" INTEGRAL i3(m93) FROM=start_time TO=end_time
.MEAS TRAN "i4(m93)_charge" INTEGRAL i4(m93) FROM=start_time TO=end_time

.MEAS TRAN "i(m90)_charge"  INTEGRAL i(m90)  FROM=start_time TO=end_time
.MEAS TRAN "i2(m90)_charge" INTEGRAL i2(m90) FROM=start_time TO=end_time
.MEAS TRAN "i3(m90)_charge" INTEGRAL i3(m90) FROM=start_time TO=end_time
.MEAS TRAN "i4(m90)_charge" INTEGRAL i4(m90) FROM=start_time TO=end_time

.MEAS TRAN "i(m215)_charge"  INTEGRAL i(m215)  FROM=start_time TO=end_time
.MEAS TRAN "i2(m215)_charge" INTEGRAL i2(m215) FROM=start_time TO=end_time
.MEAS TRAN "i3(m215)_charge" INTEGRAL i3(m215) FROM=start_time TO=end_time
.MEAS TRAN "i4(m215)_charge" INTEGRAL i4(m215) FROM=start_time TO=end_time

.MEAS TRAN "i(m96)_charge"  INTEGRAL i(m96)  FROM=start_time TO=end_time
.MEAS TRAN "i2(m96)_charge" INTEGRAL i2(m96) FROM=start_time TO=end_time
.MEAS TRAN "i3(m96)_charge" INTEGRAL i3(m96) FROM=start_time TO=end_time
.MEAS TRAN "i4(m96)_charge" INTEGRAL i4(m96) FROM=start_time TO=end_time

.MEAS TRAN "i(m219)_charge"  INTEGRAL i(m219)  FROM=start_time TO=end_time
.MEAS TRAN "i2(m219)_charge" INTEGRAL i2(m219) FROM=start_time TO=end_time
.MEAS TRAN "i3(m219)_charge" INTEGRAL i3(m219) FROM=start_time TO=end_time
.MEAS TRAN "i4(m219)_charge" INTEGRAL i4(m219) FROM=start_time TO=end_time

.MEAS TRAN "i(m95)_charge"  INTEGRAL i(m95)  FROM=start_time TO=end_time
.MEAS TRAN "i2(m95)_charge" INTEGRAL i2(m95) FROM=start_time TO=end_time
.MEAS TRAN "i3(m95)_charge" INTEGRAL i3(m95) FROM=start_time TO=end_time
.MEAS TRAN "i4(m95)_charge" INTEGRAL i4(m95) FROM=start_time TO=end_time

.MEAS TRAN "i(m91)_charge"  INTEGRAL i(m91)  FROM=start_time TO=end_time
.MEAS TRAN "i2(m91)_charge" INTEGRAL i2(m91) FROM=start_time TO=end_time
.MEAS TRAN "i3(m91)_charge" INTEGRAL i3(m91) FROM=start_time TO=end_time
.MEAS TRAN "i4(m91)_charge" INTEGRAL i4(m91) FROM=start_time TO=end_time

******计算每个半导体四个端子的平均电荷******




********* netlist_lvs ******************

** Library name: error_tolerance
** Cell name: inv
** View name: schematic
.subckt inv gnd in out vdd
m1 out in gnd gnd N L=180e-9 W=1e-6
m0 out in vdd vdd P L=180e-9 W=2e-6
.ends inv
** End of subcircuit definition.

** Library name: error_tolerance
** Cell name: inv_with_reset
** View name: schematic
.subckt inv_with_reset gnd in out reset vdd
m3 out reset gnd gnd N L=180e-9 W=1.5e-6
m1 out in gnd gnd N L=180e-9 W=1.5e-6
m2 out in net23 vdd P L=180e-9 W=3e-6
m0 net23 reset vdd vdd P L=180e-9 W=3e-6
.ends inv_with_reset
** End of subcircuit definition.

** Library name: error_tolerance
** Cell name: inv2
** View name: schematic
.subckt inv2 gnd in out vdd
m1 out in gnd gnd N L=180e-9 W=1e-6
m0 out in vdd vdd P L=180e-9 W=2e-6
.ends inv2
** End of subcircuit definition.

** Library name: error_tolerance
** Cell name: 3NAND_2_NP_error_node
** View name: schematic
xi63 gnd cd_3 net278 vdd inv
xi56 gnd cd_2 net234 vdd inv
xi47 gnd cd_1 net190 vdd inv
xi64 gnd net278 cd_3 reset vdd inv_with_reset
xi62 gnd net132 n_and_3 reset vdd inv_with_reset
xi61 gnd net261 p_and_3 reset vdd inv_with_reset
xi60 gnd cd_3 cd_n_3 reset vdd inv_with_reset
xi59 gnd net239 p_nand_3 reset vdd inv_with_reset
xi58 gnd net105 n_nand_3 reset vdd inv_with_reset
xi57 gnd net234 cd_2 reset vdd inv_with_reset
xi52 gnd net84 n_and_2 reset vdd inv_with_reset
xi49 gnd net217 p_and_2 reset vdd inv_with_reset
xi51 gnd cd_3 cd_n_2 reset vdd inv_with_reset
xi53 gnd net57 n_nand_2 reset vdd inv_with_reset
xi50 gnd net195 p_nand_2 reset vdd inv_with_reset
xi48 gnd net190 cd_1 reset vdd inv_with_reset
xi44 gnd net173 p_and_1 reset vdd inv_with_reset
xi43 gnd net36 n_and_1 reset vdd inv_with_reset
xi42 gnd cd_2 cd_n_1 reset vdd inv_with_reset
xi41 gnd net151 p_nand_1 reset vdd inv_with_reset
xi40 gnd net9 n_nand_1 reset vdd inv_with_reset
m239 net261 p_and_3 vdd vdd P L=180e-9 W=1e-6
m238 net132 n_and_3 vdd vdd P L=180e-9 W=1e-6
m237 net132 cd_n_3 vdd vdd P L=180e-9 W=4e-6
m236 net261 cd_3 vdd vdd P L=180e-9 W=4e-6
m231 net105 cd_n_3 vdd vdd P L=180e-9 W=4e-6
m230 net239 cd_3 vdd vdd P L=180e-9 W=4e-6
m214 net239 p_nand_3 vdd vdd P L=180e-9 W=1e-6
m213 net105 n_nand_3 vdd vdd P L=180e-9 W=1e-6
m212 net84 n_and_2 vdd vdd P L=180e-9 W=1e-6
m211 net217 p_and_2 vdd vdd P L=180e-9 W=1e-6
m210 net217 cd_3 vdd vdd P L=180e-9 W=4e-6
m209 net84 cd_n_2 vdd vdd P L=180e-9 W=4e-6
m200 net195 cd_3 vdd vdd P L=180e-9 W=4e-6
m199 net57 cd_n_2 vdd vdd P L=180e-9 W=4e-6
m176 net57 n_nand_2 vdd vdd P L=180e-9 W=1e-6
m175 net195 p_nand_2 vdd vdd P L=180e-9 W=1e-6
m174 net36 n_and_1 vdd vdd P L=180e-9 W=1e-6
m113 net173 p_and_1 vdd vdd P L=180e-9 W=1e-6
m112 net36 cd_n_1 vdd vdd P L=180e-9 W=4e-6
m111 net173 cd_2 vdd vdd P L=180e-9 W=4e-6
m110 net9 cd_n_1 vdd vdd P L=180e-9 W=4e-6
m109 net151 cd_2 vdd vdd P L=180e-9 W=4e-6
m108 net9 n_nand_1 vdd vdd P L=180e-9 W=1e-6
m107 net151 p_nand_1 vdd vdd P L=180e-9 W=1e-6
m235 net132 n_nand_2 net282 gnd N L=180e-9 W=2e-6 AD=960e-15 AS=260e-15 PD=2.96e-6 PS=260e-9
m234 net283 n_nand_2 net115 gnd N L=180e-9 W=3e-6 AD=300e-15 AS=1.44e-12 PD=300e-9 PS=3.96e-6
m233 net282 n_nand_2 net283 gnd N L=180e-9 W=2e-6 AD=260e-15 AS=320e-15 PD=260e-9 PS=320e-9
m97 net261 p_nand_2 net116 gnd N L=180e-9 W=2e-6 AD=960e-15 AS=260e-15 PD=2.96e-6 PS=260e-9
m92 net116 p_nand_2 net0336 gnd N L=180e-9 W=2e-6 AD=260e-15 AS=320e-15 PD=260e-9 PS=320e-9
m89 net0336 p_nand_2 net0339 gnd N L=180e-9 W=3e-6 AD=300e-15 AS=1.44e-12 PD=300e-9 PS=3.96e-6
m232 net115 cd_n_3 gnd gnd N L=180e-9 W=4e-6
m88 net0339 cd_3 gnd gnd N L=180e-9 W=4e-6
m229 net284 n_nand_2 net114 gnd N L=180e-9 W=2e-6 AD=260e-15 AS=960e-15 PD=260e-9 PS=2.96e-6
m228 net105 n_and_2 net284 gnd N L=180e-9 W=2e-6 AD=960e-15 AS=260e-15 PD=2.96e-6 PS=260e-9
m98 net239 p_and_2 net0298 gnd N L=180e-9 W=2e-6 AD=960e-15 AS=260e-15 PD=2.96e-6 PS=260e-9
m93 net0298 p_nand_2 net0161 gnd N L=180e-9 W=2e-6 AD=260e-15 AS=960e-15 PD=260e-9 PS=2.96e-6
m90 net0161 p_nand_2 net0339 gnd N L=180e-9 W=3e-6 AD=810e-15 AS=1.44e-12 PD=540e-9 PS=3.96e-6
m227 net114 n_nand_2 net115 gnd N L=180e-9 W=3e-6 AD=810e-15 AS=1.44e-12 PD=540e-9 PS=3.96e-6
m226 net105 n_and_2 net113 gnd N L=180e-9 W=2e-6 AD=540e-15 AS=960e-15 PD=540e-9 PS=2.96e-6
m225 net239 p_and_2 net297 gnd N L=180e-9 W=2e-6 AD=540e-15 AS=960e-15 PD=540e-9 PS=2.96e-6
m224 net113 n_and_2 net114 gnd N L=180e-9 W=3e-6 AD=600e-15 AS=810e-15 PD=1.54e-6 PS=540e-9
m94 net297 p_and_2 net0161 gnd N L=180e-9 W=3e-6 AD=600e-15 AS=810e-15 PD=1.54e-6 PS=540e-9
m223 net105 n_nand_2 net113 gnd N L=180e-9 W=2e-6 AD=540e-15 AS=960e-15 PD=540e-9 PS=540e-9
m222 net239 p_nand_2 net297 gnd N L=180e-9 W=2e-6 AD=540e-15 AS=960e-15 PD=540e-9 PS=540e-9
m221 net105 n_and_2 net246 gnd N L=180e-9 W=2e-6 AD=540e-15 AS=960e-15 PD=540e-9 PS=540e-9
m220 net246 n_and_2 net109 gnd N L=180e-9 W=3e-6 AD=600e-15 AS=1.44e-12 PD=1.54e-6 PS=3.96e-6
m219 net239 p_and_2 net245 gnd N L=180e-9 W=2e-6 AD=540e-15 AS=960e-15 PD=540e-9 PS=540e-9
m95 net245 p_and_2 net247 gnd N L=180e-9 W=3e-6 AD=600e-15 AS=1.44e-12 PD=1.54e-6 PS=3.96e-6
m218 net109 n_and_2 net115 gnd N L=180e-9 W=5e-6 AD=2.4e-12 AS=2.4e-12 PD=5.96e-6 PS=5.96e-6
m91 net247 p_and_2 net0339 gnd N L=180e-9 W=5e-6 AD=2.4e-12 AS=2.4e-12 PD=5.96e-6 PS=5.96e-6
m217 net105 n_nand_2 net246 gnd N L=180e-9 W=2e-6 AD=540e-15 AS=540e-15 PD=540e-9 PS=540e-9
m216 net246 n_nand_2 net109 gnd N L=180e-9 W=2e-6 AD=540e-15 AS=960e-15 PD=540e-9 PS=2.96e-6
m215 net239 p_nand_2 net245 gnd N L=180e-9 W=2e-6 AD=540e-15 AS=540e-15 PD=540e-9 PS=540e-9
m96 net245 p_nand_2 net247 gnd N L=180e-9 W=2e-6 AD=540e-15 AS=960e-15 PD=540e-9 PS=2.96e-6
m208 net299 p_and_1 net68 gnd N L=180e-9 W=3e-6 AD=300e-15 AS=1.44e-12 PD=300e-9 PS=3.96e-6
m207 net288 n_and_1 net67 gnd N L=180e-9 W=3e-6 AD=300e-15 AS=1.44e-12 PD=300e-9 PS=3.96e-6
m206 net287 n_and_1 net288 gnd N L=180e-9 W=2e-6 AD=260e-15 AS=320e-15 PD=260e-9 PS=320e-9
m205 net84 n_and_1 net287 gnd N L=180e-9 W=2e-6 AD=960e-15 AS=260e-15 PD=2.96e-6 PS=260e-9
m204 net217 p_and_1 net298 gnd N L=180e-9 W=2e-6 AD=960e-15 AS=260e-15 PD=2.96e-6 PS=260e-9
m203 net298 p_and_1 net299 gnd N L=180e-9 W=2e-6 AD=260e-15 AS=320e-15 PD=260e-9 PS=320e-9
m202 net68 cd_3 gnd gnd N L=180e-9 W=4e-6
m201 net67 cd_n_2 gnd gnd N L=180e-9 W=4e-6
m198 net195 p_nand_1 net300 gnd N L=180e-9 W=2e-6 AD=960e-15 AS=260e-15 PD=2.96e-6 PS=260e-9
m197 net300 p_and_1 net69 gnd N L=180e-9 W=2e-6 AD=260e-15 AS=960e-15 PD=260e-9 PS=2.96e-6
m196 net289 n_and_1 net66 gnd N L=180e-9 W=2e-6 AD=260e-15 AS=960e-15 PD=260e-9 PS=2.96e-6
m195 net57 n_nand_1 net289 gnd N L=180e-9 W=2e-6 AD=960e-15 AS=260e-15 PD=2.96e-6 PS=260e-9
m194 net69 p_and_1 net68 gnd N L=180e-9 W=3e-6 AD=810e-15 AS=1.44e-12 PD=540e-9 PS=3.96e-6
m193 net66 n_and_1 net67 gnd N L=180e-9 W=3e-6 AD=810e-15 AS=1.44e-12 PD=540e-9 PS=3.96e-6
m192 net57 n_nand_1 net65 gnd N L=180e-9 W=2e-6 AD=540e-15 AS=960e-15 PD=540e-9 PS=2.96e-6
m191 net195 p_nand_1 net64 gnd N L=180e-9 W=2e-6 AD=540e-15 AS=960e-15 PD=540e-9 PS=2.96e-6
m190 net65 n_nand_1 net66 gnd N L=180e-9 W=3e-6 AD=600e-15 AS=810e-15 PD=1.54e-6 PS=540e-9
m189 net64 p_nand_1 net69 gnd N L=180e-9 W=3e-6 AD=600e-15 AS=810e-15 PD=1.54e-6 PS=540e-9
m188 net57 n_and_1 net65 gnd N L=180e-9 W=2e-6 AD=540e-15 AS=960e-15 PD=540e-9 PS=540e-9
m187 net195 p_and_1 net64 gnd N L=180e-9 W=2e-6 AD=540e-15 AS=960e-15 PD=540e-9 PS=540e-9
m186 net195 p_nand_1 net201 gnd N L=180e-9 W=2e-6 AD=540e-15 AS=960e-15 PD=540e-9 PS=540e-9
m185 net202 n_nand_1 net61 gnd N L=180e-9 W=3e-6 AD=600e-15 AS=1.44e-12 PD=1.54e-6 PS=3.96e-6
m184 net201 p_nand_1 net203 gnd N L=180e-9 W=3e-6 AD=600e-15 AS=1.44e-12 PD=1.54e-6 PS=3.96e-6
m183 net57 n_nand_1 net202 gnd N L=180e-9 W=2e-6 AD=540e-15 AS=960e-15 PD=540e-9 PS=540e-9
m182 net61 n_nand_1 net67 gnd N L=180e-9 W=5e-6 AD=2.4e-12 AS=2.4e-12 PD=5.96e-6 PS=5.96e-6
m181 net203 p_nand_1 net68 gnd N L=180e-9 W=5e-6 AD=2.4e-12 AS=2.4e-12 PD=5.96e-6 PS=5.96e-6
m180 net195 p_and_1 net201 gnd N L=180e-9 W=2e-6 AD=540e-15 AS=540e-15 PD=540e-9 PS=540e-9
m179 net201 p_and_1 net203 gnd N L=180e-9 W=2e-6 AD=540e-15 AS=960e-15 PD=540e-9 PS=2.96e-6
m178 net202 n_and_1 net61 gnd N L=180e-9 W=2e-6 AD=540e-15 AS=960e-15 PD=540e-9 PS=2.96e-6
m177 net57 n_and_1 net202 gnd N L=180e-9 W=2e-6 AD=540e-15 AS=540e-15 PD=540e-9 PS=540e-9
m173 net293 c_n net19 gnd N L=180e-9 W=3e-6 AD=300e-15 AS=1.44e-12 PD=300e-9 PS=3.96e-6
m172 net292 b_n net293 gnd N L=180e-9 W=2e-6 AD=260e-15 AS=320e-15 PD=260e-9 PS=320e-9
m171 net36 a_n net292 gnd N L=180e-9 W=2e-6 AD=960e-15 AS=260e-15 PD=2.96e-6 PS=260e-9
m170 net173 a_p net301 gnd N L=180e-9 W=2e-6 AD=960e-15 AS=260e-15 PD=2.96e-6 PS=260e-9
m169 net301 b_p net302 gnd N L=180e-9 W=2e-6 AD=260e-15 AS=320e-15 PD=260e-9 PS=320e-9
m168 net302 c_p net20 gnd N L=180e-9 W=3e-6 AD=300e-15 AS=1.44e-12 PD=300e-9 PS=3.96e-6
m167 net19 cd_n_1 gnd gnd N L=180e-9 W=4e-6
m166 net20 cd_2 gnd gnd N L=180e-9 W=4e-6
m165 net294 b_n net18 gnd N L=180e-9 W=2e-6 AD=260e-15 AS=960e-15 PD=260e-9 PS=2.96e-6
m164 net9 na_n net294 gnd N L=180e-9 W=2e-6 AD=960e-15 AS=260e-15 PD=2.96e-6 PS=260e-9
m163 net151 na_p net303 gnd N L=180e-9 W=2e-6 AD=960e-15 AS=260e-15 PD=2.96e-6 PS=260e-9
m162 net303 b_p net21 gnd N L=180e-9 W=2e-6 AD=260e-15 AS=960e-15 PD=260e-9 PS=2.96e-6
m161 net21 c_p net20 gnd N L=180e-9 W=3e-6 AD=810e-15 AS=1.44e-12 PD=540e-9 PS=3.96e-6
m160 net18 c_n net19 gnd N L=180e-9 W=3e-6 AD=810e-15 AS=1.44e-12 PD=540e-9 PS=3.96e-6
m159 net9 na_n net17 gnd N L=180e-9 W=2e-6 AD=540e-15 AS=960e-15 PD=540e-9 PS=2.96e-6
m158 net151 na_p net16 gnd N L=180e-9 W=2e-6 AD=540e-15 AS=960e-15 PD=540e-9 PS=2.96e-6
m157 net17 nb_n net18 gnd N L=180e-9 W=3e-6 AD=600e-15 AS=810e-15 PD=1.54e-6 PS=540e-9
m156 net16 nb_p net21 gnd N L=180e-9 W=3e-6 AD=600e-15 AS=810e-15 PD=1.54e-6 PS=540e-9
m155 net9 a_n net17 gnd N L=180e-9 W=2e-6 AD=540e-15 AS=960e-15 PD=540e-9 PS=540e-9
m154 net151 a_p net16 gnd N L=180e-9 W=2e-6 AD=540e-15 AS=960e-15 PD=540e-9 PS=540e-9
m153 net158 nb_n net13 gnd N L=180e-9 W=3e-6 AD=600e-15 AS=1.44e-12 PD=1.54e-6 PS=3.96e-6
m152 net151 na_p net157 gnd N L=180e-9 W=2e-6 AD=540e-15 AS=960e-15 PD=540e-9 PS=540e-9
m151 net157 nb_p net159 gnd N L=180e-9 W=3e-6 AD=600e-15 AS=1.44e-12 PD=1.54e-6 PS=3.96e-6
m150 net9 na_n net158 gnd N L=180e-9 W=2e-6 AD=540e-15 AS=960e-15 PD=540e-9 PS=540e-9
m149 net13 nc_n net19 gnd N L=180e-9 W=5e-6 AD=2.4e-12 AS=2.4e-12 PD=5.96e-6 PS=5.96e-6
m148 net159 nc_p net20 gnd N L=180e-9 W=5e-6 AD=2.4e-12 AS=2.4e-12 PD=5.96e-6 PS=5.96e-6
m147 net158 b_n net13 gnd N L=180e-9 W=2e-6 AD=540e-15 AS=960e-15 PD=540e-9 PS=2.96e-6
m146 net9 a_n net158 gnd N L=180e-9 W=2e-6 AD=540e-15 AS=540e-15 PD=540e-9 PS=540e-9
m145 net151 a_p net157 gnd N L=180e-9 W=2e-6 AD=540e-15 AS=540e-15 PD=540e-9 PS=540e-9
m144 net157 b_p net159 gnd N L=180e-9 W=2e-6 AD=540e-15 AS=960e-15 PD=540e-9 PS=2.96e-6
m242 net278 net280 vdd vdd P L=180e-9 W=5e-6 AD=2.65e-12 AS=3.7e-12 PD=1.06e-6 PS=6.48e-6
m240 net278 net281 vdd vdd P L=180e-9 W=5e-6 AD=3.7e-12 AS=2.65e-12 PD=6.48e-6 PS=1.06e-6
m87 net234 net285 vdd vdd P L=180e-9 W=5e-6 AD=2.65e-12 AS=3.7e-12 PD=1.06e-6 PS=6.48e-6
m86 net234 net286 vdd vdd P L=180e-9 W=5e-6 AD=3.7e-12 AS=2.65e-12 PD=6.48e-6 PS=1.06e-6
m82 net190 net290 vdd vdd P L=180e-9 W=5e-6 AD=2.65e-12 AS=3.7e-12 PD=1.06e-6 PS=6.48e-6
m83 net190 net291 vdd vdd P L=180e-9 W=5e-6 AD=3.7e-12 AS=2.65e-12 PD=6.48e-6 PS=1.06e-6
m243 net278 n_nand_3 gnd gnd N L=180e-9 W=2e-6 AD=540e-15 AS=960e-15 PD=540e-9 PS=2.96e-6
m241 net278 n_and_3 gnd gnd N L=180e-9 W=2e-6 AD=960e-15 AS=540e-15 PD=2.96e-6 PS=540e-9
m85 net234 n_nand_2 gnd gnd N L=180e-9 W=2e-6 AD=540e-15 AS=960e-15 PD=540e-9 PS=2.96e-6
m84 net234 n_and_2 gnd gnd N L=180e-9 W=2e-6 AD=960e-15 AS=540e-15 PD=2.96e-6 PS=540e-9
m81 net190 n_nand_1 gnd gnd N L=180e-9 W=2e-6 AD=540e-15 AS=960e-15 PD=540e-9 PS=2.96e-6
m80 net190 n_and_1 gnd gnd N L=180e-9 W=2e-6 AD=960e-15 AS=540e-15 PD=2.96e-6 PS=540e-9
xi24 gnd p_nand_3 net280 vdd inv2
xi23 gnd p_and_3 net281 vdd inv2
xi55 gnd p_nand_2 net285 vdd inv2
xi54 gnd p_and_2 net286 vdd inv2
xi46 gnd p_nand_1 net290 vdd inv2
xi45 gnd p_and_1 net291 vdd inv2


.END
