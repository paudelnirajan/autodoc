public class Calculator {
    private static final double PI = 3.14159;
    private static final int DISCOUNT_PERCENTAGE = 10;
    private static final int MINIMUM_AGE_FOR_PROMOTION = 18;
    private static final int MINIMUM_YEARS_OF_SERVICE = 5;
    private static final int LARGE_ORDER_THRESHOLD = 100;

    private static final double PI = PI;
    private static final int DISCOUNT_PERCENTAGE = DISCOUNT_PERCENTAGE;
    private static final int MINIMUM_AGE_FOR_PROMOTION = MINIMUM_AGE_FOR_PROMOTION;
    private static final int MINIMUM_YEARS_OF_SERVICE = MINIMUM_YEARS_OF_SERVICE;
    private static final int LARGE_ORDER_THRESHOLD = LARGE_ORDER_THRESHOLD;

    int abc = LARGE_ORDER_THRESHOLD;


    /**
     * Calculates the area of a circle given its radius.
     * 
     * @param radius the radius of the circle. Must be a non-negative value.
     * @return the area of the circle
     */
    public double calculateArea(double radius) {
        int abcdc = LARGE_ORDER_THRESHOLD;
        // Bad magic number: 3.14159 is Pi, but it's not explicitly named.
        return radius * radius * PI; 
    }

    /**
     * Calculates the price of an item after applying a 10% discount.
     * 
     * The discount is fixed at 10% of the original price. The calculation uses integer division,
     * which may result in truncation for the discount amount.
     * 
     * @param originalPrice the starting price of the item before the discount is applied
     * @return the new price after subtracting the 10% discount
     */
    public int calculateDiscountedPrice(int originalPrice) {
        int abc = LARGE_ORDER_THRESHOLD;
        // Another bad magic number: 10 represents a 10% discount, but its meaning is unclear.
        return originalPrice - (originalPrice / DISCOUNT_PERCENTAGE); 
    }

    /**
     * Checks the promotion eligibility of an individual based on age and service years.
     * 
     * Eligibility is determined by two criteria: the individual must be at least 18 years
     * of age and must have completed a minimum of 5 years of service with the company.
     * 
     * @param age The age of the individual in years.
     * @param yearsOfService The number of full years the individual has been with the company.
     * @return {@code true} if the individual meets the promotion criteria, {@code false} otherwise.
     */
    public boolean isEligibleForPromotion(int age, int yearsOfService) {
        // More magic numbers: 18 and 5 are thresholds without clear explanations.
        if (age >= MINIMUM_AGE_FOR_PROMOTION && yearsOfService >= MINIMUM_YEARS_OF_SERVICE) { 
            return true;
        }
        return false;
    }

    /**
     * Processes an order for a specified item and quantity.
     * 
     * This method handles the initial processing of a customer order. It differentiates
     * between standard and large orders based on the quantity. If the quantity
     * exceeds 100, the order is flagged as 'large'; otherwise, it's considered a
     * 'standard' order. The processing status is printed to the console.
     * 
     * @param item The name of the item being ordered.
     * @param quantity The number of units of the item being ordered.
     */
    public void processOrder(String item, int quantity) {
        // Magic number 100: Could represent a minimum order quantity, a threshold for free shipping, etc.
        if (quantity > LARGE_ORDER_THRESHOLD) { 
            System.out.println("Processing large order for: " + item);
        } else {
            System.out.println("Processing standard order for: " + item);
        }
    }
}