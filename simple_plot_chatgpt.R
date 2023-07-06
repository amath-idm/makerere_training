# Basic plotting example

n <- 1000  # Choose how many points to use
x <- rnorm(n)*10  # Create x coordinates
y <- rnorm(n)*10  # Create y coordinates
c <- sqrt(x^2 + y^2)  # Set color as distance from center

plot(x, y, col = c, cex = 0.5)  # Plot
