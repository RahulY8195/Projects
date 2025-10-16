public class Location{
    private final String label;

    public Location(String label){
        this.label = label;
    }
    public String getLabel(){
        return label;
    }
    public boolean equals(Object other){
        if (this == other) return true;
        if (other == null || getClass() != other.getClass()) return false;
        Location location = (Location) other;
        return label. equals(location.label);
    }
    public int hashCode(){
        return label.hashCode();
    }
    public String toString(){
        return label;
    }
}