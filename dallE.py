from min_dalle import MinDalle
import torch
from PIL import Image

# Define Data type
dtype = "float32" #@param ["float32", "float16", "bfloat16"]

# Create Model1
model1 = MinDalle(
    dtype=getattr(torch, dtype),
    device='cuda',
    is_mega=True,
    is_reusable=True
)
# New York City on a rainy day(1)
# the Eiffel tower floating on the clouds(3)
# painting of an organic forest glade surrounded by tall trees(7)
# a farmhouse surrounded by flowers
# a beautiful sunset at a beach with a shell on the shore(8)
# double rainbow over a lake(4)
# aerial view of the beach at night(5)
# white snow covered mountain under blue sky during daytime(6)
# Set Prompt, Hyperparameters
text = "Reality New York City on a rainy day"
progressive_outputs = False
seamless = False
grid_size = 1
temperature = 1
supercondition_factor = 16
top_k = 256

# Define Image stream
generated_image = model1.generate_image(
    text=text,
    seed=-1,
    grid_size=grid_size,
    #progressive_outputs=progressive_outputs,
    is_seamless=seamless,
    temperature=temperature,
    top_k=int(top_k),
    supercondition_factor=float(supercondition_factor)
)

print("a")

# Display Image
#generated_image.show()
generated_image.save("generated_image.png")
resized_image = generated_image.resize((512,512), Image.LANCZOS)

resized_image.show()
# Save Image
resized_image.save("resized_image.png")



