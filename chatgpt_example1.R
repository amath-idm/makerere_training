# Simple regression example

# Set parameters
n <- 1000 # Number of points
seed <- 1 # Set random seed

# Create example data
set.seed(seed) 
x1 <- rnorm(n) 
y1 <- x1 + rnorm(n)

# Plot the data
plot(x1, y1) # Apply plot function
abline(lm(y1 ~ x1), col = "red") # Draw regression line