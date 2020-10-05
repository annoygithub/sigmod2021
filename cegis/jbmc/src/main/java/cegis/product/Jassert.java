package cegis.product;

public class Jassert {
    public static void jassert(boolean condition)
    {
      assert condition;
    }

    public static void assert_equal(int a, int b) {
      assert a == b;
    }

    public static void assert_equal(String a, String b) {
      assert a.equals(b);
    }

    public static void assert_equal(boolean a, boolean b) {
      assert a == b;
    }
    
}
