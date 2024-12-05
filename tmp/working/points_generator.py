import math
import random

xa, ya = random.randint(0, 20), random.randint(0, 20)
p1_a = (xa, ya)

xb, yb = random.randint(0, 20), random.randint(0, 20)
p2_a = (xb, yb)

theta = random.uniform(0, math.pi)
tx = random.randint(0, 20)
ty = random.randint(0, 20)

print(f"theta: {theta} \n tx: {tx} \n ty: {ty}")

mean = 0.001
std_dev = 0.1

p1_b = (
    xa * math.cos(theta) - ya * math.sin(theta) + tx + random.gauss(mean, std_dev),
    xa * math.sin(theta) + ya * math.cos(theta) + ty + random.gauss(mean, std_dev)
)
p2_b = (
    xb * math.cos(theta) - yb * math.sin(theta) + tx + random.gauss(mean, std_dev),
    xb * math.sin(theta) + yb * math.cos(theta) + ty + random.gauss(mean, std_dev)
)

print(f"p1_a: {p1_a}, p2_a: {p2_a}")
print(f"p1_b: {p1_b}, p2_b: {p2_b}")