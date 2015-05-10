c***************************************************
c* Modified 8903 [RJM] See CHANGES.DOC
c***************************************************
C-------------------------------------------------------------------------------
C  @(#)cform.inc	5.1 06/22/94
C-------------------------------------------------------------------------------
C
C       Class 1 :  Basic Information
C       Class 2 :  Pointing Parameters
C       Class 3 :  Observing Parameters
C       Class 4 :  Positions
C       Class 5 :  Environment
C       Class 6 :  Map Parameters
C       Class 7 :  Data Parameters
C       Class 8 :  Engineering Parameters
C       Class 9 :  Telescope Dependent Parameters
C       Class 10:  Open Parameters
C       Class 11:  Phase Block
C       Class 12:  Receiver Descriptor Block
C       Class 13:  Reduced Data Values
C
C       C pointers for the currently referenced array
C
      INTEGER*2  C1HLN,  C1DLN,  C1SNO,  C1OBS,  C1ONA,  C1TEL,
     .   C1PID,  C1SNA,  C1STC,  C1RCV,  C1BKE,  C1DP,   c1save, 
     .   c1norec,c1recid,C2XPC,  C2YPC,  C2UXP,  C2UYP,  C2PC,   
     .   C2ORI,  C2FR,   C2FV,   C2FL,   C2PTM,
     .   C3DAT,  C3UT,   C3LST,  C3NRC,  C3NSV,  C3PPC,  C3CYL,  
     .   C3SRT,  C3TYP11,c3phsid,
     .   C4EPH,  C4SX,   C4SY,   C4RX,   C4RY,   C4ERA,  C4EDC,  
     .   C4GL,   C4GB,   C4AZ,   C4EL,   C4IX,   C4IY,   C4DO,   
     .   C4CSC,  
     .   C5AT,   C5PRS,  C5RH,   C5IR,   C5DP,   C5MM,   
     .   C6MSA,  C6XZ,   C6YZ,   C6DX,   C6DY,   C6NP,   C6XNP,  
     .   C6YNP,  C6XGC,  C6YGC,  C6FC,      
     .   C7FW,   C7OSN,  C7BCV,  C7VC,   C7VR,   C7VRD,  C7CAL,    
     .   C8AAE,  C8ABE,  C8GN,   C8EL,   C8EF,   
     .   C9L1,   C9L1F1, C9L1F2, C9L2,   C9L2F1, C9L2F2, C9LA,   
     .   C9LB,   C9LC,   C9LD,   C9LVC,  C9PF,   C9RHO,  C9THE,  
     .   C9CFF,  
     .   C9SYN,  C9LOF,  C9HM,   C9LOI,  C9FIF,  C9RAO,  C9REO,  
     .   C9BT,   C9BOR,  C9BO,   C9OT,   C9SB,   C9WL,   C9GS,   
     .   C9PBM,  C9MBM,  C9SRO,  C9FOFS, C9FOFR1,C9FOFR2
      integer*2  C10PV,  
     .   C11OVV(22),  C11OVD(22),  C11OPT(22),  
     .   C11NSVF,C11NCY, C11NCYF,C11PPCF,C11CYLF,C11SRTF,
     .   C11PVV(10), C11PVD(10), C11PPT(10),
     .   C12CF,  C12RF,  C12FR,  C12BW,  C12RT,  C12CT,  C12SST, 
     .   C12RST, C12ST,  C12RMS, C12RP,  C12X0,  C12DX,  C12IT,  
     .   C12NI,  C12SPN, C12WO,  C12WT,  C12OO,  C12OT,  C12SP,  
     .   C12EIT, C12RXI,
     .   C13NS,  C13FS,  C13LS,  C13LAM, C13LW,  C13ILI, C13RMS
C
      integer*2 idatoff, astrings(92), numastrings
c
      data C1HLN/5/,    C1DLN/6/,    C1SNO/7/,   C1OBS/8/,   C1ONA/9/, 
     1     C1TEL/11/,   C1PID/12/,   C1SNA/13/,  C1STC/15/,  C1RCV/16/,
     2     C1BKE/17/,   C1DP/18/,    c1save/19/, C1norec/20/,c1recid/21/
      data C2XPC/30/,   C2YPC/31/,   C2UXP/32/,  C2UYP/33/,  C2PC/34/,   
     1     C2ORI/38/,   C2FR/39/,    C2FV/40/,   C2FL/41/, C2PTM/42/
      data C3DAT/55/,   C3UT/56/,    C3LST/57/,  C3NRC/58/,  C3NSV/59/,
     1     C3PPC/60/,   C3CYL/61/,   C3SRT/62/, C3TYP11/63/, c3phsid/64/
      data C4EPH/80/,   C4SX/81/,    C4SY/82/,   C4RX/83/,   C4RY/84/,   
     1     C4ERA/85/,   C4EDC/86/,   C4GL/87/,   C4GB/88/,   C4AZ/89/,   
     2     C4EL/90/,    C4IX/91/,    C4IY/92/,   C4DO/93/,   C4CSC/96/
      data C5AT/105/,   C5PRS/106/,  C5RH/107/,  C5IR/108/,  C5DP/109/,   
     1     C5MM/110/
      data C6MSA/130/,  C6XZ/131/,   C6YZ/132/,  C6DX/133/,  C6DY/134/, 
     1     C6NP/135/,   C6XNP/136/,  C6YNP/137/, C6XGC/138/, C6YGC/139/,  
     2     C6FC/140/
      data C7FW/155/,   C7OSN/156/,  C7BCV/157/, C7VC/158/,  C7VR/159/, 
     1     C7VRD/160/,  C7CAL/161/
      data C8AAE/180/,  C8ABE/181/,  C8GN/182/,  C8EL/183/,  C8EF/184/
      data C9L1/205/,   C9L1F1/206/, C9L1F2/207/,C9L2/208/,  C9L2F1/209/, 
     1     C9L2F2/210/, C9LA/211/,   C9LB/212/,  C9LC/213/,  C9LD/214/,  
     2     C9LVC/215/,  C9PF/216/,   C9RHO/218/, C9THE/219/, C9CFF/220/
      data C9SYN/205/,  C9LOF/206/,  C9HM/207/,  C9LOI/208/, C9FIF/209/,
     1     C9RAO/210/,  C9REO/211/,  C9BT/212/,  C9BOR/213/, C9BO/214/,   
     2     C9OT/215/,   C9SB/216/,   C9WL/217/,  C9GS/218/,  C9PBM/219/,  
     3     C9MBM/221/,  C9SRO/223/,  C9FOFS/227/,C9FOFR1/228/,
     4     C9FOFR2/229/
      data C10PV/230/
      data C11OVV /255, 258, 261, 264, 267, 270, 273, 276, 279, 282,
     1             285, 288, 291, 294, 297, 300, 303, 306, 309, 312,
     2             315, 318/
      data C11OVD /256, 259, 262, 265, 268, 271, 274, 277, 280, 283,
     1             286, 289, 292, 295, 298, 301, 304, 307, 310, 313,
     2             316, 319/
      data C11OPT /257, 260, 263, 266, 269, 272, 275, 278, 281, 284,
     1             287, 290, 293, 296, 299, 302, 305, 308, 311, 314,
     2             317, 320/
      data C11NSVF/255/, C11NCY/256/, C11NCYF/257/, C11PPCF/258/,
     1     C11CYLF/259/, C11SRTF/260/
      data C11PVV /261, 267, 273, 279, 285, 291, 297, 303, 309, 315/
      data C11PVD /262, 268, 274, 280, 286, 292, 298, 304, 310, 316/
      data C11PPT /263, 269, 275, 281, 287, 293, 299, 305, 311, 317/
      data C12CF/321/,  C12RF/322/, C12FR/323/,  C12BW/324/, C12RT/325/,  
     1     C12CT/326/,  C12SST/327/,C12RST/328/, C12ST/329/, C12RMS/330/, 
     2     C12RP/331/,  C12X0/332/, C12DX/333/,  C12IT/334/, C12NI/335/, 
     3     C12SPN/336/, C12WO/337/, C12WT/338/,  C12OO/339/, C12OT/340/,  
     4     C12SP/341/,  C12EIT/342/,C12RXI/343/
      data C13NS/346/,  C13FS/347/, C13LS/348/,  C13LAM/349/, C13LW/350/,  
     1     C13ILI/351/, C13RMS/352/
c
      data idatoff/790/
c
c     IDATOFF+1 = position of first data point in arrays in R*4 words
c
c     idatoff = (25*13 + 66 + 4) * 2
c                  25 = size of padded classes in R*8 words
c                  13 = number of padded classes (class 14 is not used)
c                  66 = size of class 11 in R*8 words
c	           2 converts R*8's to R*4's
c
      data astrings  /8,  9, 11, 12, 13, 15, 16, 17, 18, 42, 63, 
     .               96,140,160,161,220,230,231,232,233,234,235,
     .              236,237,238,239,256,259,262,265,268,271,274,
     .              277,280,283,286,289,292,295,298,301,304,307,
     .              310,313,316,319,257,260,263,266,269,272,275,
     .              278,281,284,287,290,293,296,299,302,305,308,
     .              311,314,317,320,262,268,274,280,286,292,298,
     .              304,310,316,263,269,275,281,287,293,299,305,
     .              311,317,341,343/
      data numastrings/92/
c     Locations in array headers of strings; number of string
c	header words
c
