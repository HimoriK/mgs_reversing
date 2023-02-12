#!/usr/bin/env python3

import sys
import re

FUNC_SIZES = { # should be updated if any .s outside psy/ changes
    0x800166AC: 68, 0x800166F0: 96, 0x80016750: 120, 0x800167C8: 100, 0x8001682C: 1100,
    0x80016C84: 12, 0x80016C90: 60, 0x800172D0: 524, 0x800175E0: 420, 0x800178D8: 160,
    0x80017978: 12, 0x80017E9C: 396, 0x800181E4: 144, 0x80018274: 108, 0x800182E0: 164,
    0x800185BC: 1000, 0x800189A4: 892, 0x80018D90: 204, 0x80018E5C: 328, 0x80018FA4: 160,
    0x80019044: 84, 0x800190A0: 124, 0x8001911C: 120, 0x8001923C: 220, 0x80019318: 304,
    0x80019448: 620, 0x800196B4: 616, 0x8001991C: 916, 0x80019CB0: 148, 0x80019D44: 500,
    0x80019F40: 64, 0x80019F80: 120, 0x8001A094: 80, 0x8001A0E4: 48, 0x8001A114: 148,
    0x8001A1A8: 540, 0x8001A3C4: 524, 0x8001A5D8: 152, 0x8001A774: 580, 0x8001AD28: 120,
    0x8001ADA0: 188, 0x8001AE5C: 308, 0x8001AF90: 292, 0x8001B0B4: 308, 0x8001B1E8: 108,
    0x8001B31C: 536, 0x8001B534: 200, 0x8001B66C: 1096, 0x8001C708: 1712, 0x8001CF88: 172,
    0x8001D034: 360, 0x8001D19C: 392, 0x8001D324: 668, 0x8001D5C8: 432, 0x8001D778: 144,
    0x8001D880: 364, 0x8001D9EC: 188, 0x8001DAA8: 104, 0x8001DC90: 256, 0x8001DD90: 440,
    0x8001DF48: 1144, 0x8001E3C0: 448, 0x8001E588: 428, 0x8001E734: 504, 0x8001E92C: 428,
    0x8001EB38: 380, 0x8001ECB4: 280, 0x8001EDCC: 584, 0x8001F3CC: 288, 0x8001FC28: 48,
    0x8001FC58: 48, 0x80021928: 160, 0x80021C64: 264, 0x80021E2C: 152, 0x80021F0C: 60,
    0x80021F70: 112, 0x80021FE0: 68, 0x80022024: 100, 0x80022090: 468, 0x80022264: 1348,
    0x800227A8: 100, 0x8002280C: 72, 0x80022854: 16, 0x80022864: 36, 0x80022888: 16,
    0x80022898: 60, 0x800228D4: 68, 0x80022918: 100, 0x8002297C: 480, 0x80022B5C: 352,
    0x80022CBC: 68, 0x80022D00: 204, 0x80022DCC: 132, 0x80022E50: 856, 0x800231A8: 204,
    0x80023274: 248, 0x8002336C: 244, 0x80023460: 452, 0x80023624: 188, 0x80023860: 316,
    0x8002399C: 676, 0x80023C40: 340, 0x80023D94: 120, 0x80023E24: 360, 0x80023F94: 64,
    0x80023FD4: 84, 0x80024028: 56, 0x80024060: 56, 0x80024098: 56, 0x800240D0: 16,
    0x800240E0: 168, 0x80024188: 12, 0x80024194: 32, 0x800241C8: 220, 0x800242A4: 276,
    0x800243D8: 44, 0x80024404: 28, 0x80024420: 188, 0x800247E8: 376, 0x800249CC: 112,
    0x80024A54: 1012, 0x80025178: 472, 0x8002554C: 336, 0x8002569C: 276, 0x800257C0: 240,
    0x80025A7C: 1616, 0x8002631C: 104, 0x8002646C: 68, 0x800264B0: 84, 0x80026504: 80,
    0x80026554: 88, 0x800265AC: 88, 0x80026604: 120, 0x8002667C: 88, 0x800266D4: 96,
    0x80026734: 96, 0x80026794: 88, 0x800267EC: 84, 0x80026840: 108, 0x800268AC: 120,
    0x80026924: 124, 0x800269A0: 132, 0x80026A24: 132, 0x80026AA8: 92, 0x80026B04: 96,
    0x80026B64: 96, 0x80026BC4: 164, 0x80026C68: 1656, 0x800272E0: 164, 0x80027384: 408,
    0x8002751C: 140, 0x800275A8: 268, 0x800276B4: 412, 0x80027850: 332, 0x8002799C: 248,
    0x80027A94: 356, 0x80027BF8: 108, 0x80027C64: 284, 0x80027D80: 400, 0x80027F10: 1348,
    0x80028454: 972, 0x80028820: 16, 0x80028830: 16, 0x80028840: 80, 0x80028890: 44,
    0x800288E0: 80, 0x80028930: 968, 0x80028CF8: 180, 0x80028DAC: 748, 0x80029098: 588,
    0x800292E4: 32, 0x80029304: 32, 0x80029324: 60, 0x80029384: 400, 0x80029514: 240,
    0x80029604: 192, 0x800296C4: 508, 0x800298C0: 28, 0x800298DC: 28, 0x800298F8: 52,
    0x8002992C: 256, 0x80029A2C: 48, 0x80029AB4: 56, 0x80029AEC: 176, 0x80029B9C: 436,
    0x80029D50: 832, 0x8002A090: 356, 0x8002A27C: 572, 0x8002A4B8: 128, 0x8002A538: 168,
    0x8002A5E0: 292, 0x8002A960: 24, 0x8002A978: 152, 0x8002AA10: 56, 0x8002AB40: 100,
    0x8002AC44: 88, 0x8002AC9C: 288, 0x8002ADBC: 1948, 0x8002B558: 24, 0x8002B570: 144,
    0x8002B6C8: 72, 0x8002B77C: 216, 0x8002CA48: 100, 0x8002D208: 248, 0x8002D300: 240,
    0x8002D400: 176, 0x8002D4B0: 80, 0x8002D500: 48, 0x8002D530: 240, 0x8002D620: 184,
    0x8002D6D8: 260, 0x8002D7DC: 568, 0x8002DA14: 608, 0x8002DC74: 64, 0x8002DCCC: 72,
    0x8002DD1C: 196, 0x8002DDE0: 984, 0x8002E1B8: 240, 0x8002E2A8: 204, 0x8002E374: 28,
    0x8002E508: 60, 0x8002E544: 68, 0x8002E588: 140, 0x8002E614: 44, 0x8002E640: 72,
    0x8002E8D4: 72, 0x8002E91C: 332, 0x8002EA68: 64, 0x8002EADC: 164, 0x8002EBE8: 164,
    0x8002EC8C: 88, 0x8002ECE4: 88, 0x8002ED68: 156, 0x8002EE04: 124, 0x8002EE80: 136,
    0x8002EF08: 128, 0x8002EF88: 128, 0x8002F008: 140, 0x8002F094: 308, 0x8002F1C8: 172,
    0x8002F274: 272, 0x8002F384: 576, 0x8002F5C4: 136, 0x8002F64C: 320, 0x8002F78C: 800,
    0x8002FAAC: 168, 0x8002FB54: 108, 0x8002FBC0: 152, 0x8002FC58: 76, 0x8002FCA4: 76,
    0x8002FCF0: 148, 0x8002FD84: 24, 0x8002FD9C: 892, 0x80030118: 312, 0x80030250: 400,
    0x800303E0: 188, 0x8003049C: 256, 0x8003059C: 260, 0x800306A0: 192, 0x80030760: 188,
    0x8003081C: 52, 0x80030850: 56, 0x80030888: 88, 0x800308E0: 88, 0x80030938: 72,
    0x80030980: 40, 0x800309B4: 68, 0x800309F8: 56, 0x80030A30: 116, 0x80030AA4: 32,
    0x80030AC4: 40, 0x80030AEC: 80, 0x80030B3C: 304, 0x80030C6C: 452, 0x80031580: 164,
    0x80031624: 60, 0x80031954: 428, 0x80031BD4: 768, 0x80031F04: 524, 0x8003214C: 96,
    0x800321AC: 76, 0x800321F8: 272, 0x80032308: 280, 0x80032420: 276, 0x80032534: 296,
    0x8003265C: 120, 0x800326D4: 116, 0x80032748: 116, 0x800327BC: 100, 0x80032820: 56,
    0x80032858: 272, 0x80032968: 92, 0x800329C4: 296, 0x80032AEC: 84, 0x80032B40: 132,
    0x80032BC4: 132, 0x80032C68: 36, 0x80032C8C: 112, 0x80032CFC: 20, 0x80032D10: 412,
    0x80032EAC: 424, 0x80033054: 336, 0x8003330C: 120, 0x80033384: 116, 0x800333F8: 264,
    0x80033500: 96, 0x80033560: 112, 0x800335D0: 212, 0x80033704: 128, 0x80033784: 2052,
    0x80034020: 176, 0x800340D0: 1064, 0x800344F8: 200, 0x800345C0: 408, 0x80034758: 220,
    0x80034834: 192, 0x800348F4: 188, 0x80034E10: 248, 0x80034EAC: 92, 0x8003501C: 184,
    0x800350D4: 184, 0x8003518C: 600, 0x800353E4: 392, 0x8003556C: 400, 0x800356FC: 2104,
    0x80035F34: 200, 0x80035FFC: 32, 0x8003601C: 32, 0x8003603C: 176, 0x800360EC: 668,
    0x80036388: 816, 0x800366B8: 856, 0x80036A10: 304, 0x80036B40: 100, 0x80036BA4: 1412,
    0x80037128: 244, 0x8003721C: 760, 0x80037514: 236, 0x80037600: 248, 0x800376F8: 244,
    0x800377EC: 52, 0x80037820: 708, 0x80037AE4: 128, 0x80037B64: 372, 0x80037CD8: 68,
    0x80037D1C: 72, 0x80037D64: 84, 0x80037DB8: 16, 0x80037DC8: 16, 0x80037DD8: 104,
    0x80037E40: 160, 0x80037EE0: 76, 0x80038070: 1228, 0x80038678: 16, 0x80038688: 16,
    0x80038698: 12, 0x800386A4: 324, 0x800387E8: 100, 0x800389A8: 88, 0x80038A6C: 16,
    0x80038A7C: 12, 0x80038A88: 172, 0x80038BB4: 132, 0x80038C38: 216, 0x80038D10: 88,
    0x80038D68: 12, 0x80038D74: 108, 0x80038DE0: 72, 0x80038E28: 264, 0x80038F3C: 448,
    0x800390FC: 212, 0x800391D0: 2956, 0x80039D5C: 88, 0x80039DB4: 272, 0x80039EC4: 504,
    0x8003A0BC: 532, 0x8003A2D0: 916, 0x8003A664: 788, 0x8003A978: 180, 0x8003AA2C: 824,
    0x8003ADD8: 232, 0x8003AEC0: 1168, 0x8003B350: 292, 0x8003B474: 224, 0x8003B5E0: 52,
    0x8003B614: 188, 0x8003B6D0: 196, 0x8003B794: 348, 0x8003B8F0: 764, 0x8003BBEC: 232,
    0x8003BCD4: 584, 0x8003BF1C: 816, 0x8003C24C: 672, 0x8003C4EC: 1136, 0x8003C95C: 572,
    0x8003CBF0: 132, 0x8003CC74: 20, 0x8003CC88: 12, 0x8003CC94: 428, 0x8003CE40: 56, 0x8003CE84: 116,
    0x8003CEF8: 232, 0x8003CFE0: 144, 0x8003D070: 96, 0x8003D0D0: 84, 0x8003D1DC: 224,
    0x8003D2BC: 144, 0x8003D34C: 88, 0x8003D3A4: 88, 0x8003D3FC: 80, 0x8003D44C: 128,
    0x8003D4CC: 84, 0x8003D568: 44, 0x8003D594: 92, 0x8003D5F0: 92, 0x8003D64C: 92,
    0x8003D6CC: 272, 0x8003D7DC: 560, 0x8003DB2C: 128, 0x8003DBAC: 368, 0x8003DF30: 256,
    0x8003E030: 184, 0x8003E0E8: 712, 0x8003E3B0: 264, 0x8003E4B8: 444, 0x8003E674: 796,
    0x8003E990: 588, 0x8003EBDC: 80, 0x8003EC2C: 128, 0x8003ECC0: 12, 0x8003ECCC: 128,
    0x8003ED4C: 1472, 0x8003F30C: 252, 0x8003F408: 92, 0x8003F464: 84, 0x8003F4B8: 84,
    0x8003F530: 688, 0x8003F7E0: 88, 0x8003F84C: 304, 0x8003F97C: 56, 0x8003F9B4: 600,
    0x8003FC0C: 72, 0x8003FC54: 252, 0x8003FD50: 608, 0x8003FFB0: 132, 0x80040034: 376,
    0x800401AC: 244, 0x800402A0: 324, 0x800403E4: 180, 0x80040498: 248, 0x80040590: 188,
    0x8004064C: 344, 0x800407A4: 280, 0x800408BC: 720, 0x80040B8C: 568, 0x80040DC4: 432,
    0x80040F74: 368, 0x8004114C: 256, 0x80041280: 444, 0x8004143C: 208, 0x8004150C: 128,
    0x8004158C: 3028, 0x80042198: 1384, 0x80042730: 184, 0x800427E8: 44, 0x80042814: 40,
    0x80042848: 312, 0x80042988: 476, 0x80042B64: 144, 0x80042BF4: 580, 0x80042E38: 320,
    0x80042F78: 72, 0x80042FC0: 304, 0x800430F0: 72, 0x80043138: 232, 0x80043220: 592,
    0x80043470: 56, 0x800434A8: 76, 0x800434F4: 176, 0x800435A4: 36, 0x800435C8: 36,
    0x800435EC: 140, 0x80043678: 940, 0x80043A24: 1452, 0x80043FD0: 788, 0x800442E4: 788,
    0x800445F8: 712, 0x800448C0: 432, 0x80044A70: 32, 0x80044A9C: 292, 0x80044BC0: 24,
    0x80044DC4: 372, 0x80044FF4: 256, 0x80045124: 808, 0x8004544C: 716, 0x80045718: 112,
    0x80045788: 12, 0x80045794: 20, 0x800457B4: 260, 0x800458B8: 248, 0x800459B0: 308,
    0x80045AE4: 552, 0x80045D0C: 3056, 0x800469F0: 168, 0x80046A98: 120, 0x80046B10: 100,
    0x80046B74: 100, 0x80046BD8: 184, 0x80046C90: 356, 0x80046DF4: 328, 0x80046F3C: 348,
    0x800470B4: 64, 0x800470F4: 184, 0x80047AA0: 412, 0x80047D70: 396, 0x80047EFC: 72,
    0x80047F44: 176, 0x80047FF4: 48, 0x80048044: 60, 0x80048080: 128, 0x80048124: 168,
    0x800481CC: 1236, 0x800486F4: 232, 0x800487DC: 140, 0x80048868: 260, 0x8004896C: 1092,
    0x80048DB0: 488, 0x80048F98: 60, 0x80048FD4: 1060, 0x800494C4: 36, 0x800494E8: 48,
    0x80049518: 28, 0x80049534: 40, 0x8004955C: 76, 0x800495A8: 156, 0x80049644: 56,
    0x8004969C: 116, 0x80049710: 84, 0x80049764: 48, 0x80049794: 48, 0x800497C4: 120,
    0x8004983C: 1196, 0x80049CE8: 428, 0x80049E94: 72, 0x80049EDC: 1352, 0x8004A424: 112,
    0x8004A4C4: 136, 0x8004A54C: 252, 0x8004A648: 328, 0x8004A790: 112, 0x8004A800: 88,
    0x8004A87C: 280, 0x8004A994: 212, 0x8004AA68: 372, 0x8004ABF0: 336, 0x8004AD40: 212,
    0x8004AE3C: 108, 0x8004AEA8: 316, 0x8004AFE4: 188, 0x8004B0A0: 2140, 0x8004B958: 108,
    0x8004B9C4: 188, 0x8004BA80: 632, 0x8004BCF8: 416, 0x8004BE98: 436, 0x8004C04C: 280,
    0x8004C164: 384, 0x8004C2E4: 308, 0x8004C418: 2824, 0x8004CF20: 232, 0x8004D008: 324,
    0x8004D14C: 132, 0x8004D1D0: 124, 0x8004D280: 80, 0x8004D2D0: 44, 0x8004D3D8: 200,
    0x8004D4A0: 224, 0x8004D580: 168, 0x8004D628: 2040, 0x8004DE20: 292, 0x8004DF68: 388,
    0x8004E110: 136, 0x8004E198: 92, 0x8004E1F4: 56, 0x8004E260: 60, 0x8004E358: 44,
    0x8004E384: 152, 0x8004E458: 104, 0x8004E4C0: 92, 0x8004E51C: 108, 0x8004E5E8: 308,
    0x8004E71C: 236, 0x8004E808: 296, 0x8004E930: 160, 0x8004E9D0: 128, 0x8004EAA8: 108,
    0x8004EB14: 96, 0x8004EB74: 140, 0x8004EC00: 140, 0x8004EC8C: 124, 0x8004ED08: 100,
    0x8004ED6C: 188, 0x8004EE28: 136, 0x8004EEB0: 100, 0x8004EF14: 208, 0x8004EFE4: 80,
    0x8004F090: 188, 0x8004F14C: 184, 0x8004F204: 156, 0x8004F2A0: 76, 0x8004F338: 284,
    0x8004F454: 240, 0x8004F544: 228, 0x8004F628: 192, 0x8004F6E8: 508, 0x8004F8E4: 344,
    0x8004FA3C: 56, 0x8004FAE8: 80, 0x8004FB38: 20, 0x8004FB4C: 68, 0x8004FB90: 16,
    0x8004FBA0: 68, 0x8004FBE4: 20, 0x8004FBF8: 120, 0x8004FC70: 72, 0x8004FCB8: 304,
    0x8004FDE8: 416, 0x8004FF88: 276, 0x8005009C: 348, 0x800501F8: 132, 0x8005027C: 284,
    0x80050398: 168, 0x80050440: 296, 0x80050568: 256, 0x80050668: 368, 0x800507D8: 160,
    0x80050878: 492, 0x80050A64: 1804, 0x80051170: 76, 0x800511BC: 1024, 0x800515BC: 1108,
    0x80051A10: 404, 0x80051BA4: 508, 0x80051DA0: 560, 0x80051FD0: 336, 0x80052120: 492,
    0x8005230C: 348, 0x80052468: 216, 0x80052540: 184, 0x800525F8: 196, 0x800526BC: 160,
    0x8005275C: 128, 0x800527DC: 224, 0x800528BC: 112, 0x8005292C: 148, 0x800529C0: 156,
    0x80052A5C: 332, 0x80052BA8: 292, 0x80052CCC: 396, 0x80052E58: 444, 0x80053014: 480,
    0x800531F4: 364, 0x80053360: 600, 0x800535B8: 540, 0x800537D4: 248, 0x800538CC: 392,
    0x80053A54: 300, 0x80053B88: 96, 0x80053BE8: 396, 0x80053D74: 296, 0x80053E9C: 272,
    0x80053FAC: 292, 0x800540D0: 216, 0x800541A8: 104, 0x80054210: 76, 0x8005425C: 188,
    0x80054318: 144, 0x800543A8: 124, 0x80054424: 100, 0x800544E0: 360, 0x80054648: 200,
    0x80054710: 544, 0x80054930: 224, 0x80054A10: 320, 0x80054B50: 184, 0x80054C08: 352,
    0x80054D68: 404, 0x80054EFC: 1080, 0x80055334: 152, 0x800553EC: 96, 0x8005544C: 104,
    0x800554B4: 112, 0x80055524: 1204, 0x800559D8: 1024, 0x80055DD8: 2168, 0x80056650: 508,
    0x8005684C: 64, 0x8005688C: 156, 0x80056928: 244, 0x80056A54: 132, 0x80056AD8: 176,
    0x80056B88: 84, 0x80056BDC: 96, 0x80056C3C: 96, 0x80056C9C: 320, 0x80056DDC: 740,
    0x800570C0: 88, 0x80057118: 160, 0x800571B8: 448, 0x80057474: 284, 0x80057590: 548,
    0x800577B4: 144, 0x80057844: 348, 0x800579A0: 240, 0x80057A90: 352, 0x80057BF0: 996,
    0x80057FD4: 932, 0x80058378: 248, 0x80058470: 468, 0x80058644: 316, 0x80058780: 584,
    0x800589C8: 584, 0x80058C10: 112, 0x80058C80: 520, 0x80058E88: 108, 0x80058EF4: 148,
    0x80058F88: 204, 0x80059054: 256, 0x80059154: 104, 0x800591BC: 56, 0x800591F4: 808,
    0x8005951C: 256, 0x8005961C: 224, 0x800596FC: 5652, 0x8005AD10: 2076, 0x8005B52C: 292,
    0x8005B650: 2356, 0x8005BF84: 88, 0x8005BFDC: 128, 0x8005C05C: 228, 0x8005C140: 164,
    0x8005C1E4: 180, 0x8005C298: 188, 0x8005C354: 176, 0x8005C404: 84, 0x8005C458: 64,
    0x8005C498: 76, 0x8005C4E4: 240, 0x8005C5D4: 240, 0x8005C6C4: 472, 0x8005C89C: 216,
    0x8005C974: 468, 0x8005CB48: 468, 0x8005CD1C: 320, 0x8005CE5C: 336, 0x8005CFAC: 392,
    0x8005D134: 52, 0x8005D168: 32, 0x8005D188: 256, 0x8005D288: 208, 0x8005D358: 76,
    0x8005D3A4: 128, 0x8005D424: 228, 0x8005D424: 228, 0x8005D508: 132, 0x8005D58C: 120,
    0x8005D604: 184, 0x8005D6BC: 716, 0x8005D988: 1112, 0x8005DDE0: 144, 0x8005DE70: 224,
    0x8005DF50: 320, 0x8005E090: 272, 0x8005E1A0: 184, 0x8005E258: 220, 0x8005E334: 468,
    0x8005E508: 108, 0x8005E574: 304, 0x8005E6A4: 208, 0x8005E774: 120, 0x8005E7EC: 500,
    0x8005E9E0: 140, 0x8005EA6C: 196, 0x8005EB30: 104, 0x8005EB98: 132, 0x8005EC1C: 240,
    0x8005ED0C: 104, 0x8005ED74: 104, 0x8005EDDC: 104, 0x8005EE44: 96, 0x8005EEA4: 96,
    0x8005EF04: 244, 0x8005EFF8: 156, 0x8005F094: 92, 0x8005F0F0: 144, 0x8005F180: 264,
    0x8005F288: 108, 0x8005F2F4: 136, 0x8005F37C: 140, 0x8005F408: 48, 0x8005F438: 52,
    0x8005F4AC: 348, 0x8005F644: 168, 0x8005F6EC: 680, 0x8005F994: 564, 0x8005FBC8: 220,
    0x8005FCA4: 132, 0x8005FD28: 768, 0x80060028: 188, 0x800600E4: 172, 0x800601B0: 284,
    0x800602CC: 184, 0x80060384: 104, 0x800603EC: 212, 0x800604C0: 136, 0x80060548: 148,
    0x800605DC: 104, 0x80060644: 64, 0x80060684: 96, 0x800606E4: 40, 0x8006070C: 360,
    0x80060874: 152, 0x8006090C: 52, 0x80060940: 128, 0x800609C0: 332, 0x80060B0C: 80,
    0x80060B5C: 184, 0x80060C14: 164, 0x80060D5C: 148, 0x80060DF0: 120, 0x80060E68: 184,
    0x80060F20: 120, 0x80060F98: 268, 0x800610A4: 352, 0x80061204: 184, 0x800612BC: 200,
    0x800613FC: 268, 0x80061528: 204, 0x800615FC: 268, 0x80061708: 596, 0x8006195C: 184,
    0x80061A14: 284, 0x80061B30: 112, 0x80061BA0: 220, 0x80061C7C: 152, 0x80061D14: 140,
    0x80061DA0: 124, 0x80061E40: 108, 0x800620B4: 448, 0x80062320: 92, 0x8006237C: 320,
    0x800624BC: 56, 0x800624F4: 152, 0x8006258C: 324, 0x800626D0: 712, 0x80062998: 580,
    0x80062BDC: 160, 0x80062C7C: 300, 0x80062DA8: 228, 0x80062E8C: 752, 0x8006317C: 188,
    0x80063238: 60, 0x80063274: 96, 0x800632D4: 148, 0x80063368: 108, 0x800633D4: 308,
    0x80063508: 180, 0x800635BC: 136, 0x80063644: 12, 0x80063650: 24, 0x80063668: 156,
    0x80063704: 388, 0x80063888: 44, 0x800638B4: 120, 0x8006392C: 92, 0x80063988: 96,
    0x800639E8: 428, 0x80063B94: 124, 0x80063C10: 192, 0x80063CD0: 268, 0x80063DDC: 212,
    0x80063EB0: 420, 0x80064054: 364, 0x800641C0: 440, 0x80064378: 220, 0x80064454: 308,
    0x80064588: 1132, 0x800649F4: 160, 0x80064A94: 444, 0x80064C50: 952, 0x80065008: 144,
    0x80065098: 128, 0x80065118: 152, 0x800651B0: 80, 0x80065200: 84, 0x80065254: 56,
    0x8006528C: 172, 0x80065338: 76, 0x80065384: 52, 0x800653B8: 80, 0x80065408: 272,
    0x80065518: 1404, 0x80065B04: 624, 0x80065E90: 760, 0x800663A0: 124, 0x8006641C: 1144,
    0x80066B58: 104, 0x80066BC0: 680, 0x80066FF0: 220, 0x800670CC: 740, 0x80067558: 440,
    0x8006788C: 488, 0x80067BFC: 356, 0x80067D60: 952, 0x80068118: 108, 0x80068214: 268,
    0x80068320: 92, 0x8006837C: 164, 0x80068420: 888, 0x80068798: 652, 0x80068A24: 464,
    0x80068BF4: 280, 0x80068D0C: 460, 0x80068ED8: 156, 0x80068F74: 396, 0x80069100: 132,
    0x80069184: 176, 0x80069234: 156, 0x800692D0: 272, 0x800693E0: 152, 0x80069478: 596,
    0x800696CC: 388, 0x80069850: 12, 0x8006985C: 64, 0x8006989C: 132, 0x80069920: 132,
    0x800699A4: 1048, 0x80069DBC: 108, 0x80069E28: 60, 0x80069E64: 428, 0x8006A010: 240,
    0x8006A100: 40, 0x8006A128: 240, 0x8006A218: 652, 0x8006A4A4: 108, 0x8006A510: 60,
    0x8006A54C: 384, 0x8006A6CC: 204, 0x8006A798: 348, 0x8006A8F4: 92, 0x8006A950: 524,
    0x8006AB5C: 1280, 0x8006B05C: 200, 0x8006B124: 324, 0x8006B268: 60, 0x8006B2A4: 488,
    0x8006B48C: 216, 0x8006B564: 520, 0x8006B800: 136, 0x8006B888: 156, 0x8006B924: 140,
    0x8006B9B0: 192, 0x8006BA70: 160, 0x8006BB10: 532, 0x8006BD24: 300, 0x8006BE50: 64,
    0x8006BE90: 92, 0x8006BEEC: 232, 0x8006BFD4: 208, 0x8006C0A4: 112, 0x8006C114: 616,
    0x8006C37C: 584, 0x8006C5C4: 1404, 0x8006CB40: 152, 0x8006CBD8: 120, 0x8006CC50: 204,
    0x8006CD1C: 312, 0x8006CE54: 240, 0x8006CF44: 480, 0x8006D124: 208, 0x8006D1F4: 172,
    0x8006D2A0: 220, 0x8006D37C: 644, 0x8006D608: 916, 0x8006D99C: 112, 0x8006DA0C: 580,
    0x8006DC50: 200, 0x8006DD18: 120, 0x8006DDEC: 416, 0x8006DF8C: 80, 0x8006DFDC: 276,
    0x8006E0F0: 308, 0x8006E224: 132, 0x8006E2A8: 132, 0x8006E32C: 132, 0x8006E3B0: 244,
    0x8006E4A4: 552, 0x8006E6CC: 1348, 0x8006ECB8: 144, 0x8006ED48: 112, 0x8006EDB8: 972,
    0x8006F184: 268, 0x8006F290: 136, 0x8006F318: 1024, 0x8006F7AC: 460, 0x8006FA60: 672,
    0x8006FDDC: 104, 0x8006FE44: 160, 0x8006FEE4: 184, 0x8006FF9C: 76, 0x8006FFE8: 88,
    0x80070040: 92, 0x8007009C: 68, 0x800700E0: 200, 0x800701A8: 100, 0x8007020C: 860,
    0x80070568: 696, 0x80070820: 656, 0x80070AB0: 508, 0x80070CAC: 360, 0x80070E14: 172,
    0x80070ECC: 128, 0x80070F4C: 196, 0x80071010: 268, 0x8007111C: 164, 0x800711C0: 352,
    0x80071320: 220, 0x800713FC: 156, 0x80071498: 84, 0x800714EC: 1244, 0x800719C8: 140,
    0x80071A54: 648, 0x80071CDC: 236, 0x80071DC8: 224, 0x80071EA8: 240, 0x80071F98: 220,
    0x80072074: 12, 0x80072080: 788, 0x80072394: 228, 0x80072478: 148, 0x8007250C: 44,
    0x80072538: 148, 0x80072608: 288, 0x80072728: 524, 0x80072934: 120, 0x800729B4: 88,
    0x80072A0C: 280, 0x80072B60: 116, 0x80072C10: 472, 0x80072DE8: 276, 0x80072EFC: 496,
    0x800730EC: 92, 0x800731CC: 44, 0x800731F8: 184, 0x800732B0: 180, 0x80073364: 300,
    0x80073490: 272, 0x800735A0: 272, 0x800736B0: 580, 0x80073930: 188, 0x800739EC: 416,
    0x80073B8C: 548, 0x80073DB0: 152, 0x80073E48: 720, 0x80074118: 284, 0x80074234: 188,
    0x800742F0: 68, 0x80074334: 168, 0x80074564: 224, 0x80074644: 112, 0x800746B4: 124,
    0x80074730: 276, 0x80074844: 116, 0x800748D8: 644, 0x80074B5C: 328, 0x80074CA4: 132,
    0x80074D28: 132, 0x80074DAC: 408, 0x80074F5C: 520, 0x80075164: 48, 0x80075194: 268,
    0x80075314: 68, 0x80075358: 188, 0x80075414: 208, 0x800754E4: 300, 0x80075610: 332,
    0x8007575C: 1656, 0x80075DD4: 912, 0x80076164: 388, 0x800761A0: 212, 0x80076274: 428,
    0x80076420: 356, 0x80076708: 548, 0x8007692C: 192, 0x800769EC: 128, 0x80076A6C: 44,
    0x80076A98: 144, 0x80076B28: 1260, 0x80077014: 520, 0x8007721C: 72, 0x80077264: 472,
    0x8007743C: 132, 0x800774C0: 244, 0x800775B4: 248, 0x800776AC: 144, 0x8007773C: 224,
    0x800778B4: 212, 0x80077988: 48, 0x800779B8: 108, 0x80077A24: 584, 0x80077C6C: 184,
    0x80077D24: 588, 0x80077F70: 228, 0x80078054: 468, 0x80078228: 464, 0x80078404: 64,
    0x80078444: 220, 0x80078520: 256, 0x800789E0: 216, 0x80078AB8: 296, 0x80078BE0: 260,
    0x80078CE4: 168, 0x80078D8C: 224, 0x80078F30: 200, 0x80078FF8: 12, 0x80079004: 228,
    0x800790E8: 84, 0x8007913C: 88, 0x80079194: 80, 0x800791E4: 60, 0x80079220: 100,
    0x80079284: 356, 0x80079460: 132, 0x800794E4: 384, 0x80079664: 360, 0x800797CC: 48,
    0x800797FC: 356, 0x80079960: 72, 0x800799A8: 116, 0x80079A1C: 16, 0x80079A2C: 184,
    0x80079AE4: 108, 0x80079B50: 2844, 0x8007A66C: 732, 0x8007A948: 1224, 0x8007AE10: 8016,
    0x8007CD60: 152, 0x8007CDF8: 284, 0x8007CF14: 212, 0x8007CFE8: 1052, 0x8007D404: 1476,
    0x8007D9C8: 96, 0x8007DA28: 108, 0x8007DA94: 400, 0x8007DC24: 348, 0x8007DD80: 400,
    0x8007DF10: 412, 0x8007E0AC: 276, 0x8007E1C0: 3444, 0x8007EF34: 312, 0x8007F06C: 100,
    0x8007F0D0: 268, 0x8007F1DC: 348, 0x8007F350: 68, 0x8007F394: 100, 0x8007F3F8: 1944,
    0x8007FB90: 584, 0x8007FDD8: 452, 0x8007FF9C: 316, 0x800800D8: 2888, 0x80080C20: 296,
    0x80080D48: 204, 0x80080E14: 2024, 0x800815FC: 788, 0x80081910: 256, 0x80081A18: 452,
    0x80081BDC: 160, 0x80081C7C: 784, 0x80081F8C: 56, 0x80081FC4: 36,
    0x80081FE8: 260, 0x800820EC: 132, 0x80082170: 36, 0x80082194: 308, 0x800822C8: 72,
    0x80082310: 112, 0x80082380: 200, 0x80082448: 504, 0x80082640: 348, 0x800827A4: 8,
    0x800827AC: 3048, 0x80083394: 104, 0x8008341C: 224, 0x800834FC: 776, 0x80083804: 320,
    0x80083964: 100, 0x800839C8: 492, 0x80083BB4: 692, 0x80083E68: 36, 0x80083E8C: 72,
    0x80083ED4: 20, 0x80083EE8: 16, 0x80083EF8: 16, 0x80083F08: 76, 0x80083F54: 640,
    0x800841D4: 488, 0x800843BC: 216, 0x80084494: 2104, 0x80084CCC: 148, 0x80084D60: 232,
    0x80084E48: 320, 0x80084F88: 152, 0x80085020: 324, 0x80085164: 796, 0x80085480: 112,
    0x800854F0: 172, 0x8008559C: 188, 0x80085658: 276, 0x8008576C: 588, 0x800859B8: 152,
    0x80085A50: 308, 0x80085B84: 340, 0x80085CD8: 192, 0x80085D98: 72, 0x80085DE0: 440,
    0x80085F98: 180, 0x8008604C: 332, 0x80086198: 136, 0x80086220: 96, 0x80086280: 644,
    0x80086504: 200, 0x800865CC: 200, 0x80086694: 160, 0x80086734: 312, 0x8008686C: 792,
    0x80086B84: 132, 0x80086C08: 144, 0x80086C98: 128, 0x80086D18: 132, 0x80086D9C: 156,
    0x80086E38: 64, 0x80086E78: 64, 0x80086EB8: 64, 0x80086F00: 80, 
    0x80086F50: 200, 0x80087018: 264, 0x80087120: 76, 0x8008716C: 72, 0x800871B4: 44,
    0x800871E0: 224, 0x800872C0: 44, 0x800872EC: 128, 0x8008736C: 24, 0x80087384: 72,
    0x800873CC: 24, 0x800873E4: 296, 0x8008750C: 24, 0x80087524: 72, 0x8008756C: 32,
    0x8008758C: 228, 0x80087670: 100, 0x800876D4: 92, 0x80087730: 28, 0x80087764: 104,
    0x800877CC: 104, 0x80087834: 32, 0x80087854: 168, 0x80087904: 136, 0x8008798C: 88,
    0x800879E4: 100, 0x80087A48: 8, 0x80087A58: 40, 0x80087A80: 8, 0x80087A88: 804,
    0x80087DAC: 128, 0x80087E2C: 104, 0x80087E94: 96, 0x80087EF4: 48, 0x80087F24: 52,
    0x80087F58: 40, 0x80087F80: 40, 0x80087FA8: 828, 0x800882E4: 60, 0x80088320: 692,
    0x800885D4: 192, 0x80088694: 48, 0x800886C4: 24, 0x800886DC: 24, 0x800886F4: 24,
    0x8008870C: 112, 0x8008877C: 112, 0x8008880C: 44, 0x80088838: 40, 0x80088868: 76,
    0x800888B4: 68, 0x800888F8: 936, 0x80088CB0: 1528, 0x800892A8: 16, 0x8008982C: 728,
    0x80089D24: 1756, 0x8008AAEC: 1368, 0x8008AAEC: 1368, 0x8008B0A4: 984, 0x8008B450: 44,
    0x8008B51C: 116, 0x8008B590: 40, 0x8008B5B8: 80, 0x8008B630: 24, 0x8008B68C: 240,
    0x8008B77C: 744, 0x8008BA88: 216, 0x8008BB4C: 20, 0x8008BBC0: 8, 0x8008BC8C: 352,
    0x8008BDEC: 684, 0x8008C170: 236, 0x8008C25C: 200, 0x8008C324: 92, 0x8008C380: 60,
    0x8008C408: 76, 0x8008C454: 104, 0x8008C4BC: 120, 0x8008C534: 88, 0x8008C58C: 12,
    0x8008C5B8: 8, 0x8008C5C0: 8, 0x8008C5E0: 8, 0x8008C5E8: 8, 0x8008C5F0: 8, 0x8008C5F8: 8,
    0x8002A848: 56, 0x80076584 : 388, 0x80057378: 252,
}

import sys
import re
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

RETURN_SIZE = 12 # just the return
NOP_SIZE = 4

# #pragma INCLUDE_ASM("asm/chara/snake/sna_init_800515BC.s");
PRAGMA_RE = r'^#pragma\s+INCLUDE_ASM\s*\(\s*"([^"]+)"\s*\).*$'

# all on one line to keep error line numbers correct
FUNC_FMT = r'int {}(void) {{ asm("{}"); return {}; }}'

# _800515BC.
ADDR_SUFFIX_RE = r'_([0-9A-F]{8})\.'

TMP_DIR = 'include_asm_tmp'

def main(path, output):
    with open(path) as f:
        lines = f.readlines()

    processed = []
    depends = []

    for raw_line in lines:
        line = raw_line.strip()
        if not line.startswith('#pragma'):
            processed.append(raw_line)
            continue

        m = re.match(PRAGMA_RE, line)
        if not m:
            processed.append(raw_line)
            continue

        include_path = m.group(1)

        if '\\' in include_path:
            print("error: INCLUDE_ASM paths should not use backslashes in: ", include_path, file=sys.stderr)
            sys.exit(1)

        m = re.search(ADDR_SUFFIX_RE, include_path)
        if not m:
            print('error: INCLUDE_ASM paths should have the _<ADDR>.s suffix', file=sys.stderr)
            sys.exit(2)

        addr_str = m.group(1)
        addr = int(addr_str, 16)
        func_size = FUNC_SIZES.get(addr)

        if not func_size:
            print('error: INCLUDE_ASM addr suffix of referenced path is unknown:', addr_str, file=sys.stderr)
            sys.exit(3)

        if func_size < RETURN_SIZE + NOP_SIZE:
            print('error: INCLUDE_ASM func too small - consider matching it: ', addr_str, file=sys.stderr)
            sys.exit(5)

        num_nops = func_size - RETURN_SIZE
        assert num_nops % NOP_SIZE == 0
        nops = 'nop;' * int(num_nops / NOP_SIZE)

        name = os.path.basename(include_path).replace('.s', '')

        first_char = ord(name[0])

        upper_byte = addr >> 24
        assert upper_byte == 0x80

        # we need to temporarily rename the func without changing its size so
        # encode first char of name into 0x80 part of addr since that's constant for us
        addr = (addr & 0x00FFFFFF) | (first_char << 24)

        name_chars = list(name)
        name_chars[0] = '_'
        name = ''.join(name_chars)

        func = FUNC_FMT.format(name, nops, hex(addr)) + '\n'
        processed.append(func)
        depends.append(include_path.replace('.s', '.obj').replace('asm/', 'obj/'))

    with open(output, 'w') as f:
        f.write(''.join(processed))

    with open(output + '.deps', 'w') as f:
        f.write('\n'.join(depends) + '\n')

    # nina picks this up due to deps=msvc which ensures the post process
    # will only run after these required objs are built
    #for d in depends:
    #    print("Note: including file: " + os.path.abspath(d))
    #print("output = " + output)
    
    dynDepName = output.replace(".c.asm.preproc", ".c.dyndep")
    #print("Dyndep file = " + dynDepName)

    targetAddTo = output.replace(".c.asm.preproc", ".obj")
    targetAddTo = targetAddTo.replace(":", "$:") # escape colon in drive path
    #print("targetAddTo = " + targetAddTo)
 
    with open(dynDepName, 'w') as f:
        f.write("ninja_dyndep_version = 1\n")
        depsStr = ""
        if len(depends) > 0:
            for d in depends:
                d = '../' + d
                d = d.replace("\\", "/")
                d = d.replace(":", "$:") # escape colon in drive path
                depsStr = depsStr + " " + d
            f.write("build " + targetAddTo + ": dyndep | " + depsStr + "\n")
        else:
            f.write("build " + targetAddTo + ": dyndep" + depsStr + "\n")

if __name__ == '__main__':
    src = sys.argv[1].replace('\\', '/')
    dst = sys.argv[2].replace('\\', '/')
    main(src, dst)
