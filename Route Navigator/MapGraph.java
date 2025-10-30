import java.util.*;
public class MapGraph{
    private final Map<Location, List<Path>> connectionMap;

    public MapGraph () {
        connectionMap = new HashMap<> ();
    }
    public void registerLocation(Location point){
        connectionMap.putIfAbsent(point, new ArrayList<>());
    }
    public void connectLocations(Location source, Location target, double metric){
        registerLocation(source);
        registerLocation(target);
        connectionMap.get(source).add(new Path(source, target, metric));
    }
    public List<Path> getOutgoingPaths(Location point){
        return connectionMap.getOrDefault(point,Collections.emptyList());
    }
    public Set<Location> getALLLocations(){
        return connectionMap.keySet();
    }

}
    

