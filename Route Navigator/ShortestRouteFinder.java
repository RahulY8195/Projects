import java.util.*;

public class ShortestRouteFinder {
    public static List<Location> computeOptimalRoute(MapGraph map,Location origin, Location destination){
        Map<Location, Double> minDistance = new HashMap<>();
        Map<Location, Location> previousNode = new HashMap<>();
        PriorityQueue<Location> queue = new PriorityQueue<>(Comparator.comparingDouble(minDistance::get));
        Set<Location> settled = new HashSet<>();

        for(Location loc : map.getALLLocations()){
            minDistance.put(loc, Double.POSITIVE_INFINITY);
        }
        minDistance.put(origin,0.0);
        queue.add(origin);

        while(!queue.isEmpty()){
            Location active = queue.poll();
            if(settled.contains(active)) continue;
            settled.add(active);
            if(active.equals(destination)) break;

            for(Path path : map.getOutgoingPaths(active)){
                Location neighbor = path.getEndPoint();
                if(settled.contains(neighbor)) continue;
                double altDist = minDistance.get(active) + path.getMetric();
                if(altDist < minDistance.get(neighbor)){
                    minDistance.put(neighbor,altDist);
                    previousNode.put(neighbor,active);
                    queue.add(neighbor);
                }

                
            }
        }
        List<Location> route = new ArrayList<>();
        Location cursor = destination;
        if(!previousNode.containsKey(destination) && !destination.equals(origin)){

        }
        while(cursor != null){
            route.add(cursor);
            cursor = previousNode.get(cursor);
        }
        Collections.reverse(route);
        return route;

    }
    public static double totalRouteMetric(MapGraph map, List<Location> route){
        double total = 0.0;
        for(int i = 0; i < route.size()-1; i++){
            Location from = route.get(i);
            Location to = route.get(i + 1);
            for ( Path path : map.getOutgoingPaths(from)){
                if(path.getEndPoint().equals(to)){
                    total += path.getMetric();
                    break;
                }
            }
        }
        return total;
    }
}
