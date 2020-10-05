#ifndef __RAND_INPUT_H__
#define __RAND_INPUT_H__

#include "String.h"
#include "Array.h"
#include "Map.h"
#include "Any.h"

int rand_int();
long rand_long();
_Bool rand_bool();
String rand_string();
AString rand_astring();
Any rand_any();
AAny rand_aany();
AStringAny rand_astringany();
double rand_double();

char* hex(const char* buf, int size);
char* unhex(const char* h, int size);

char* string2cstr(String s);
char* astr2cstr(AString str);
char* any2str(Any a);
char* aany2str(AAny aa);
char* astringany2str(AStringAny asa);
char* mstringany2str(MStringAny msa);

String cstr2string(char *str);
AString cstr2astr(char* astr);
Any str2any(char* str);
AAny str2aany(char* str);
AStringAny str2astringany(char* str);

String dup_string(String s);
AString dup_astring(AString a);
Any dup_any(Any a);
AAny dup_aany(AAny aa);
AStringAny dup_astringany(AStringAny asa);

void rand_inputs(int num, ...);

#endif
