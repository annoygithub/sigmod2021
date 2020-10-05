// https://github.com/charleso/fuse/blob/master//src/main/scala/fuse/Data.scala
def udf(r: Row) = {
    f(E.fromRowUnsafe(r))
}
