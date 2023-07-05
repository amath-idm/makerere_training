# Simple regression example

n <- 1000
seed <- 1
set.seed(seed) # Create example data
x1 <- rnorm(n)
y1 <- x1 + rnorm(n)
plot(x1, y1) # Apply plot function
abline(lm(y1 ~ x1), col = "red") # Draw regression line