public class Path {
    private final Location startPoint;
    private final Location endPoint;
    private final double metric;

    public Path(Location startPoint, Location endPoint, double metric){
        this.startPoint = startPoint;
        this.endPoint = endPoint;
        this.metric = metric;

    }
    public Location getStartPoint(){
        return startPoint;
    }
    public Location getEndPoint(){
        return endPoint;
    }
    public double getMetric(){
        return metric;
    }
    public String toString(){
        return startPoint + " -> " + endPoint + "(" + metric + ")";
    }
   
    
}
