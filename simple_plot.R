# Basic plotting example

n <- 1000  # Choose how many points to use
x <- rnorm(n)  # Create x coordinates
y <- rnorm(n)  # Create y coordinates
c <- 1+sqrt(x^2 + y^2)  # Set color as distance from center

plot(x, y, col=c, pch=16, cex=0.5)  # Plot