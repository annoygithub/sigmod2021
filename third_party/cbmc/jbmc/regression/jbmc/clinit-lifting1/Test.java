public class Test {

  public static void main(boolean unknown) {

    int total = 0;

    for(int i = 0; i < 10; ++i) {
      if(unknown)
        total += Other.x;
    }

  }

}

class Other {

  static int x = 1;

}
