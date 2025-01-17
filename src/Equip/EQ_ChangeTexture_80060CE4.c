#include "Game/game.h"
#include "libdg/libdg.h"
#include "unknown.h"

void EQ_ChangeTexture_80060CE4(const char *itemName1, const char *itemName2)
{
    DG_TEX *pTexture1;
    DG_TEX *pTexture2;
    u_short    buff[5];

    pTexture1 = DG_GetTexture_8001D830(GV_StrCode_80016CCC(itemName1));
    pTexture2 = DG_GetTexture_8001D830(GV_StrCode_80016CCC(itemName2));

    face_item_helper_80060CB8(&pTexture1->field_2_bUsed.s, buff);
    face_item_helper_80060CB8(&pTexture2->field_2_bUsed.s, &pTexture1->field_2_bUsed.s);
    face_item_helper_80060CB8(buff, &pTexture2->field_2_bUsed.s);
}

// Remove head model
void EQ_InvisibleHead_80060D5C(OBJECT *pObj, short *pnPacks, short *pRaise)
{
    if (pObj->objs->n_models >= 7)
    {
        *pnPacks = pObj->objs->objs[6].n_packs;
        *pRaise = pObj->objs->objs[6].raise;
        DG_FreeObjPacket_8001AAD0(&pObj->objs->objs[6], 0);
        DG_FreeObjPacket_8001AAD0(&pObj->objs->objs[6], 1);
        pObj->objs->objs[6].n_packs = 1;
        pObj->objs->objs[6].raise = -30000;
    }
}

// Put head model back
void EQ_VisibleHead_80060DF0(OBJECT *pObj, short *pnPacks, short *pRaise)
{
    if (pObj->objs->n_models >= 7)
    {
        pObj->objs->objs[6].n_packs = *pnPacks;
        pObj->objs->objs[6].raise = *pRaise;
        DG_FreeObjPacket_8001AAD0(&pObj->objs->objs[6], 0);
        DG_FreeObjPacket_8001AAD0(&pObj->objs->objs[6], 1);
    }
}

void EQ_InvisibleUnit_80060E68(DG_OBJS *pObjs, unsigned int color, int arg2)
{
    int       i;
    int       n_models;
    DG_OBJ   *pObj;
    POLY_GT4 *pPoly;
    DG_OBJ   *pIter;
    int       n_packs;

    for (i = 0; i < 2; i++)
    {
        pObj = pObjs->objs;

        for (n_models = pObjs->n_models; n_models > 0; n_models--)
        {
            pPoly = pObj->packs[i];

            if (!pPoly)
            {
                pObj++;
                continue;
            }

            if ((arg2 != 0) && (LLOAD(&pPoly->r0) == color))
            {
                continue;
            }

            for (pIter = pObj; pIter; pIter = pIter->extend)
            {
                for (n_packs = pIter->n_packs; n_packs > 0; n_packs--)
                {
                    LSTORE(color, &pPoly->r0);
                    LSTORE(color, &pPoly->r1);
                    LSTORE(color, &pPoly->r2);
                    LSTORE(color, &pPoly->r3);
                    pPoly++;
                }
            }

            pObj++;
        }
    }
}

int EQ_VisibleUnit_80060F20(short *arg0, char *arg1)
{
    int adjust;
    int x, y;

    adjust = ((arg0[0] / 4) - 160);
    x = arg0[0] - adjust;

    if (x < 0)
    {
        x = 0;
    }

    if (x > 319)
    {
        x = 319;
    }

    arg1[0] = x;

    y = arg0[1] + 112;

    if (y < 0)
    {
        y = 0;
    }

    if (y > 223)
    {
        y = 223;
    }

    arg1[1] = y;

    return x > 255;
}
