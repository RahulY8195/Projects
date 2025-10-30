import java.util.*;

public class RouteApp {
    private static final Scanner scanner = new Scanner(System.in);
    private static final MapGraph mapGraph = new MapGraph();

    public static void main(String[] args) {
        System.out.println("=== Route Navigation Utility ===");
        while (true) {
            displayMenu();
            String input = scanner.nextLine().trim();
            switch (input) {
                case "1":
                    addNewLocation();
                    break;
                case "2":
                    definePath();
                    break;
                case "3":
                    getOptimalRoute();
                    break;
                case "4":
                    showLocations();
                    break;
                case "5":
                    showPaths();
                    break;
                case "0":
                    System.out.println("Exiting. Thank you!");
                    return;
                default:
                    System.out.println("Invalid option.");
            }
        }
    }

    static void displayMenu() {
        System.out.println("\nOptions:");
        System.out.println("1. Register New Location");
        System.out.println("2. Define Path Between Locations");
        System.out.println("3. Find Optimal Route");
        System.out.println("4. Show All Locations");
        System.out.println("5. Show All Paths");
        System.out.println("0. Exit");
        System.out.print("Select: ");
    }

    static void addNewLocation() {
        System.out.print("Location name: ");
        String label = scanner.nextLine().trim();
        Location loc = new Location(label);
        mapGraph.registerLocation(loc);
        System.out.println("Location '" + label + "' added.");
    }

    static void definePath() {
        System.out.print("Start Location: ");
        String startLabel = scanner.nextLine().trim();
        System.out.print("End Location: ");
        String endLabel = scanner.nextLine().trim();
        System.out.print("Distance/Cost: ");
        double value = Double.parseDouble(scanner.nextLine().trim());
        Location start = new Location(startLabel);
        Location end = new Location(endLabel);
        mapGraph.connectLocations(start, end, value);
        System.out.println("Path defined: " + startLabel + " -> " + endLabel + " (" + value + ")");
    }

    static void getOptimalRoute() {
        System.out.print("From: ");
        String fromLabel = scanner.nextLine().trim();
        System.out.print("To: ");
        String toLabel = scanner.nextLine().trim();
        Location from = new Location(fromLabel);
        Location to = new Location(toLabel);

        List<Location> route = ShortestRouteFinder.computeOptimalRoute(mapGraph, from, to);
        if (route.isEmpty()) {
            System.out.println("No route found from " + fromLabel + " to " + toLabel + ".");
        } else {
            double metric = ShortestRouteFinder.totalRouteMetric(mapGraph, route);
            System.out.print("Best path: ");
            for (int i = 0; i < route.size(); i++) {
                System.out.print(route.get(i));
                if (i != route.size() - 1) System.out.print(" -> ");
            }
            System.out.println("\nTotal metric: " + metric);
        }
    }

    static void showLocations() {
        System.out.println("All Registered Locations:");
        for (Location loc : mapGraph.getALLLocations()) {
            System.out.println("- " + loc.getLabel());
        }
    }

    static void showPaths() {
        System.out.println("All Defined Paths:");
        for (Location loc : mapGraph.getALLLocations()) {
            for (Path path : mapGraph.getOutgoingPaths(loc)) {
                System.out.println("- " + path);
            }
        }
    }
}
