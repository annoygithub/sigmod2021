// https://github.com/MarkCLewis/WorldCongress2019/blob/master//scala/src/main/scala/utility/GHCNStation.scala
case class GHCNStation(
    id: String,
    lat: Double,
    lon: Double,
    elevation: Double,
    state: String,
    name: String
)
def apply(line: String): GHCNStation = {
        val id = line.substring(0, 11).trim
        val lat = line.substring(12, 20).trim.toDouble
        val lon = line.substring(21, 30).trim.toDouble
        val elevation = line.substring(31, 37).trim.toDouble
        val state = line.substring(38, 40).trim
        val name = line.substring(41, 71).trim
        GHCNStation(id, lat, lon, elevation, state, name)
    }
