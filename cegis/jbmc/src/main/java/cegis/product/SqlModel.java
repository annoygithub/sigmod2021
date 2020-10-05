package cegis.product;

public class SqlModel {
    public static int add(int a, int b) {
        return a + b;
    }

    public static boolean and(boolean a, boolean b) {
        return a && b;
    }

    public static boolean constBool(boolean a) {
        return a;
    }

    public static int constInt(int a) {
        return a;
    }

    public static String constString(String s) {
        return s;
    }

    public static boolean eq(int a, int b) {
        return a == b;
    }

    public static boolean eq_str(String a, String b) {
        return a.equals(b);
    }

    public static String int2char(int a) {
        a = a % 256;
        char c = (char) a;
        return String.valueOf(c);
    }

    public static int locate(String substr, String str) {
        return str.indexOf(substr) + 1;
    }

    public static int locate2(String substr, String str, int start) {
        return str.indexOf(substr, start-1) + 1;
    }

    public static boolean le(int a, int b) {
        return a <= b;
    }

    public static int length(String s) {
        return s.length();
    }

    public static boolean lt(int a, int b) {
        return a < b;
    }

    public static String ltrim(String s) {
        int i = 0;
        while (i < s.length() && Character.isWhitespace(s.charAt(i))) {
            i++;
        }
        return s.substring(i);
    }

    public static int max(int a, int b) {
        return a > b ? a : b;
    }

    public static int neg(int a) {
        return -a;
    }

    public static int min(int a, int b) {
        return a < b ? a : b;
    }

    public static boolean or(boolean a, boolean b) {
        return a || b;
    }

    public static String right(String s, int l) {
        int start = s.length() - l;
        if (start > s.length()) start = s.length();
        if (start < 0) start = 0;
        return s.substring(start);
    }

    public static String rpad2(String str, int l, String pad) {
        if (pad.equals("")) return str;

        if (l < str.length()) 
            return str.substring(0, l);

        String ret = str;
        while (l >= pad.length()) {
            ret = ret + pad;
            l -= pad.length();
        }

        ret = ret + pad.substring(0, l);
        return ret;
    }
        
    public static String rtrim(String s) {
        int i = s.length() - 1;
        while (i > 0 && Character.isWhitespace(s.charAt(i))) {
            i --;
        }
        return s.substring(0, i + 1);
    }

    public static int sub(int a, int b) {
        return a - b;
    }

    public static String substring(String str, int start) {
        int s = 0;
        if (start > 0) {
            s = start - 1;
            if (s > str.length()) s = str.length();
        } else if (start < 0) {
            s = str.length()+start;
            if (s < 0) s = 0;
        }
        
        return str.substring(s);
    }

    public static String substring2(String str, int start, int len) {
        int s = 0;
        if (start > 0) {
            s = start - 1;
            if (s > str.length()) s = str.length();
        } else if (start < 0) {
            s = str.length()+start;
            if (s < 0) s = 0;
        }

        int e = s + len;
        if (e > str.length()) e = str.length();
        return str.substring(s, e);
    }

    public static String substring_index(String str, String delim, int count) {
        if (count == 0) return "";
        if (delim.isEmpty()) return "";

        if (count >= 0) {
            int end = 0;
            int from = 0;
            while (count-- > 0) {
                end = str.indexOf(delim, from);
                if (end == -1) {
                    end = str.length();
                    break;
                }
                from = end + delim.length();
            }
            return str.substring(0, end);
        } else {
            int start = str.length();
            int from = str.length() - 1;
            while (count ++ < 0) {
                int i = str.lastIndexOf(delim, from);
                if (i == -1) {
                    start = 0;
                    break;
                }
                start = i + delim.length();
                from = i -1;
            }
            return str.substring(start);
        }
    }

    public static String translate(String str, String sub, String rep) {
        return str.replace(sub, rep);
    }

    public static String trim(String str) {
        return str.trim();
    }
}
