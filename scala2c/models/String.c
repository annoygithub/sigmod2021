#include <stdlib.h>
#include <stddef.h>
#include <string.h>
#include <assert.h>
#include "String.h"


String constString(char *cstr) {
    assume(cstr != NULL);
    String ret = malloc(sizeof(_String));
    ret->size = strlen(cstr);
    ret->buf = cstr;
    return ret;
}


String _empty_string(int buflen) {
    char *buf = malloc(buflen);
    String r = malloc(sizeof(_String));
    r->size = 0;
    r->buf = buf;
    return r;
}


void _append_char(String s, char c) {
    s->buf[s->size] = c;
    s->size ++;
}


void* memmem(void* haystack, int haystack_len, void *needle, int needle_len) {
    for (int i=0; i<=haystack_len-needle_len; i++) {
        int j=0;
        while (j < needle_len) {
            char h = ((char*)haystack)[i+j];
            char n = ((char*)needle)[j];
            if (h != n) break;
            j ++;
        }
        if (j == needle_len) return (char*) haystack + i;
    }
    return NULL;
}


String String_concat(String a, String b) {
    String r = _empty_string(a->size + b->size);
    for (int i=0; i<a->size; i++) {
        _append_char(r, a->buf[i]);
    }
    for (int i=0; i<b->size; i++) {
        _append_char(r, b->buf[i]);
    }
    return r;
}


_Bool String_equals(String s1, String s2) {
    if (s1->size != s2->size) return 0;
    return 0 == memcmp(s1->buf, s2->buf, s1->size);
}


int String_indexOf(String str, String substr) {
    char *r = memmem(str->buf, str->size, substr->buf, substr->size);
    if (r == NULL) return -1;
    char *b = str->buf;
    return r - b;
}


int String_indexOf2(String str, String substr, int start) {
    if (start < 0) start = 0;
    if (start > str->size) return -1;
    
    char *r = memmem(str->buf + start, str->size - start, substr->buf, substr->size);
    if (r == NULL) return -1;
    char *b = str->buf;
    return r - b;
}


String String_replace(String str, String search, String replace) {
    if (search->size == 0) return str;
    int maxlen = str->size / search->size * replace->size + str->size % search->size;
    if (replace->size <= search->size) maxlen = str->size;

    char* buf = malloc(maxlen);
    int size = 0;
    int pos = 0;
    while (pos < str->size) {
        char* sub = memmem(str->buf+pos, str->size-pos, search->buf, search->size);
        if (sub == NULL) {
            memcpy(buf+size, str->buf+pos, str->size-pos);
            size += str->size - pos;
            break;
        }
        
        memcpy(buf+size, str->buf+pos, (sub-str->buf)-pos);
        size += (sub-str->buf)-pos;
        memcpy(buf+size, replace->buf, replace->size);
        size += replace->size;
        pos = (sub-str->buf) + search->size;
    }

    String r = malloc(sizeof(_String));
    r->size = size;
    r->buf = buf;
    return r;
}


String String_substring(String str, int s) {
    if (s >= str->size) return constString("");
    if (s < 0) s = 0;

    String ret = malloc(sizeof(_String));
    ret->size = str->size - s;
    ret->buf = str->buf + s;
    return ret;
}


String String_substring2(String str, int s, int e) {
    assume(0 <= s && s <= str->size);
    assume(0 <= e && e <= str->size);
    assume(e >= s);

    String ret = malloc(sizeof(_String));
    ret->size = e-s;
    ret->buf = str->buf + s;
    return ret;
}


String String_trim(String str) {
    int s = 0;
    int e = str->size;
    while (s < str->size && (str->buf[s] == ' ' || str->buf[s] == '\t')) s ++;
    while (e > s && (str->buf[e-1] == ' ' || str->buf[e-1] == '\t')) e --;

    String ret = malloc(sizeof(_String));
    ret->size = e-s;
    ret->buf = str->buf + s;
    return ret;
}


int String_toint(String str) {
    assume(str->size > 0);

    int ret = 0;
    char c = str->buf[0];
    int sign = c == '-' ? -1 : 1;
    int i = (c == '-' || c == '+') ? 1 : 0;
    assume(str->size > 1);
    for (;i<str->size; i++) {
        char c = str->buf[i];
        assume('0' <= c && c <= '9');
        ret = ret * 10 + c - '0';
    }
    return ret * sign;
}


double String_todouble(String str) {
    assume(str->size > 0);

    double ret = 0.0;
    char c = str->buf[0];
    int sign = c == '-' ? -1 : 1;
    int i = (c == '-' || c == '+') ? 1 : 0;
    assume(str->size > i);
    assume(str->buf[i] != '.');
    for (;i<str->size; i++) {
        char c = str->buf[i];
        assume(('0' <= c && c <= '9') || c == '.');
        if (c == '.') break;
        ret = ret * 10 + c - '0';
    }

    if (i < str->size) {
        assume(str->buf[i] == '.');
        i ++;
    }
    assume(str->size > i);
    double factor = 0.1;
    for (; i<str->size; i++) {
        char c = str->buf[i];
        assume('0' <= c && c <= '9');
        ret += factor * (c - '0');
        factor *= 0.1;
    }

    return ret * sign;
}


String String_fromint(int i) {
    char *buf = malloc(256);
    int size = 0;

    if (i == 0) {
        buf[0] = '0';
        size = 1;
    } else {
        _Bool sign = i < 0;
        if (sign) i *= -1;

        while (i > 0) {
            buf[255-(size++)] = '0' + i % 10;
            i /= 10;
        }

        if (sign) buf[255-(size++)] = '-';
        buf += 256 - size;
    }

    String ret = malloc(sizeof(_String));
    ret->size = size;
    ret->buf = buf;
    return ret;
}


String String_fromdouble(double d) {
    char *buf = malloc(256);
    int size = 0;
    _Bool sign = d < 0.0;
    if (sign) {
        d *= -1;
        buf[size++] = '-';
    }

    assume(d < (1 << 30));
    int id = (int) d;
    double frac = d - id;
    if (id == 0) {
        buf[size++] = '0';
    } else {
        int m = 1;
        while (m*10 <= id) m *= 10;
        while (m > 0) {
            buf[size++] = '0' + id / m;
            id = id % m;
            m /= 10;
        }
    }

    buf[size++] = '.';

    for (int i=0; i<3; i++) {
        frac *= 10;
        int t = (int) frac;
        buf[size++] = '0' + t;
        frac -= t;
    }

    String ret = malloc(sizeof(_String));
    ret->size = size;
    ret->buf = buf;
    return ret;
}


String String_format_ss(String fmt, String s1, String s2) {
    char * buf = malloc(fmt->size + s1->size + s2->size);
    int size = 0;

    int ns = 0;
    for (int i=0; i<fmt->size; i++) {
        char c = fmt->buf[i];
        if (c == '%') {
            i ++;
            assume(i<fmt->size);

            c = fmt->buf[i];
            if (c == '%') {
                buf[size++] = '%';
            } else if (c == 's') {
                String s = NULL;
                if (ns == 0) {
                    s = s1;
                } else if (ns == 1) {
                    s = s2;
                } else {
                    assume(0);
                }
                ns ++;

                for (int j=0; j<s->size; j++) {
                    buf[size++] = s->buf[j];
                }
            } else {
                assume(0);
            }
        } else {
            buf[size++] = c;
        }
    }

    String ret = malloc(sizeof(_String));
    ret->size = size;
    ret->buf = buf;
    return ret;
}


_Bool String_contains(String haystack, String needle) {
     return String_indexOf(haystack, needle) >= 0;
}


AString String_split(String str, String delim) {
    assume(delim->size > 0);

    AString ret = malloc(sizeof(_AString));
    ret->arr = malloc(sizeof(String) * (str->size+1));
    ret->size = 0;

    int pos=0;
    int npos=-1;
    while ((npos = String_indexOf2(str, delim, pos)) != -1) {
        String s = malloc(sizeof(_String));
        s->buf = str->buf+pos;
        s->size = npos - pos;
        ret->arr[ret->size] = s;
        ret->size ++;
        pos = npos + delim->size;
    }
    String s = malloc(sizeof(_String));
    s->buf = str->buf + pos;
    s->size = str->size - pos;
    ret->arr[ret->size] = s;
    ret->size ++;
    return ret;
}


_Bool String_startsWith(String s1, String s2) {
    return String_indexOf(s1, s2) == 0;
}


_Bool String_endsWith(String s1, String s2) {
    if (s1->size < s2->size) return 0;

    int off = s1->size - s2->size;
    for (int i=0; i<s2->size; i++) {
        if (s1->buf[off+i] != s2->buf[i]) return 0;
    }
    return 1;
}


String String_lower(String s) {
    String ret = malloc(sizeof(_String));
    ret->size = s->size;
    ret->buf = malloc(s->size);
    for (int i=0; i<s->size; i++) {
        char c = s->buf[i];
        if ('A' <= c && c <= 'Z') {
            ret->buf[i] = c - ('A' - 'a');
        } else {
            ret->buf[i] = c;
        }
    }
    return ret;
}


int String_length(String s) {
    return s->size;
}


String String_stripPrefix(String s, String prefix) {
    if (String_startsWith(s, prefix)) {
        return String_substring(s, prefix->size);
    }
    return s;
}


String String_stripSuffix(String s, String suffix) {
    if (String_equals(String_substring(s, s->size - suffix->size), suffix)) {
        return String_substring2(s, 0, s->size - suffix->size);
    }
    return s;
}


_Bool String_forall(String s, _Bool (*func)(char c)) {
    for (int i=0; i<s->size; i++) {
        if (! func(s->buf[i])) return 0;
    }
    return 1;
}
