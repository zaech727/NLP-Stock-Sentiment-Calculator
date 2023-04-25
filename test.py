import openai


openai.api_key = "INSERT API KEY"

response = openai.Completion.create(
    model="text-davinci-003",
    prompt="Produce 5 prompts for DALLE to generate promotional images of my product. Make the prompts concise, incomplete sentences, specify what is within the frame of each image, and the style of the image. I supplied DALLE with starting images of my product, and my goal is for DALLE to create images containing my product. Base these prompts off of the following product description: My product is a running watch. It uses GPS to track your miles and other information related to running, syncs easily with your smartphone, is water-proof.",
    temperature=0.6,
)

result = response.choices[0].text
print(result)
