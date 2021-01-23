#include "linker.h"
#include "gcl.h"

extern const char   aDemoNoCode[];
extern const char   aDemoNoDataOnCd[];

extern int          dword_800AB9B0;
extern int          gBinds_800ABA60;
extern int          game_state_flags_800AB3CC;
extern int          counter_800AB380;

int SECTION(".sbss") gBinds_800ABA60;

extern void     mts_printf_8008BBA0(const char*, ...);
char*           GCL_Read_String_80020A70(char *pScript);
int             sub_8004955C(char*, int);
int             sub_80037DD8(int, unsigned int);

int Script_tbl_demo_8002C890(void) {
    int     param;
    int     load_data;
    char    *msg;

    if (GCL_GetParam_80020968('s') == 0)
    {
        mts_printf_8008BBA0(aDemoNoCode);
    }

    param = GCL_Get_Param_80020AD4();

    if (GCL_GetParam_80020968('p') == 0)
    {
        load_data = 0;
    }
    else
    {
        load_data = GCL_Get_Param_80020AD4() | 0x80000000;
    }

    dword_800AB9B0 = gBinds_800ABA60;

    if (param >= 0)
    {
        counter_800AB380 = 0x7FFF0000;
        game_state_flags_800AB3CC |= 0x80000000;
        sub_80037DD8(param, load_data);
    }
    else
    {
        if (load_data < 0)
        {
            load_data &= 0xFFFF;
        }
        else
        {
            load_data = -1;
        }

        if (GCL_GetParam_80020968('f'))
        {
            msg = GCL_Read_String_80020A70(GCL_Get_Param_Result_80020AA4());
        }
        else
        {
            msg = (char*)aDemoNoDataOnCd;
        }
        sub_8004955C(msg, load_data);
    }
    return 0;
}
