public class Trivial {
  @Annotation
  public class Inner {
    @Annotation
    private int x;

    public Inner() { x = 1; }

    @Annotation
    public void f(int y) {
        try {
            x++;
        } catch(Exception ex) {
        }
    }
  }
}
