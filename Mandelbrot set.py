from PIL import Image
width = 800
height = 600
x_min, x_max = -2.0, 1.0
y_min, y_max = -1.5, 1.5
img = Image.new('RGB', (width, height))
pixels = img.load()
max_iter = 100
escape_radius = 2
def pixel_to_complex(x, y):
    return complex(x_min + (x / width) * (x_max - x_min), y_min + (y / height) * (y_max - y_min))
def mandelbrot(c, max_iter):
    z = 0
    for i in range(max_iter):
        z = z * z + c
        if abs(z) > escape_radius:
            return i
    return max_iter
for y in range(height):
    for x in range(width):
        iterations = mandelbrot(pixel_to_complex(x, y), max_iter)
        pixels[x, y] = (iterations % 16 * 16, iterations % 8 * 32, iterations % 4 * 64)
img.show()
