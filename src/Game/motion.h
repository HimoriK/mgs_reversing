#ifndef _MOTION_H_
#define _MOTION_H_

#include "psyq.h"

typedef struct Motion_0x18
{
    // Controls the sound of Snake's footsteps; values, ranging from 0x0-0x11 (with intermediary jumps to 0x80 and
    // 0xff), appear to be the current frame of the sound sample (with frame 0x8 corresponding to the hard footstep
    // sound). Disabling any of the reads or writes causes Snake's footsteps no longer to make any noise, such that he
    // can for instance walk in puddles without being heard by enemies.
  short field_0;
  short field_2;
  short field_4;
  short field_6;
  unsigned int field_8;
  void* field_C;
  short field_10;
  short field_12;
  short field_14;
  unsigned short field_16;
} Motion_0x18;

typedef struct _MOTION_CONTROL
{
    void          *field_00_oar_ptr; // 0x00
    Motion_0x18 field_04;         // 0x04
    Motion_0x18 field_1C; // 0x1C

    // In Actor_SnaInit, this is a pointer to his GM_Control's rotator (0x20->0x8).
    SVECTOR *field_34; // 0x34

    // In Actor_SnaInit, this is a pointer to his GM_Control's movement vector (0x20->0x44).
    SVECTOR        *step;     // 0x38
    unsigned short *field_3C; // 0x3C
    unsigned long   interp;   // 0x40
    SVECTOR         field_44;
    SVECTOR        *field_4C;
    // todo: padding field here?
} MOTION_CONTROL;

void sub_8003501C(MOTION_CONTROL *m_ctrl, int a1, int motion);
void sub_800350D4(MOTION_CONTROL *m_ctrl, int a1, int motion);
void sub_8003556C(MOTION_CONTROL *m_ctrl);

int sub_8003603C(MOTION_CONTROL *pCtrl, Motion_0x18 *pSub);
int Process_Oar_8003518C(MOTION_CONTROL *pCtrl, Motion_0x18 *a2, int a3);
int sub_800360EC(MOTION_CONTROL *pCtrl, Motion_0x18 *a2, int a3, int a4);

#endif // _MOTION_H_
