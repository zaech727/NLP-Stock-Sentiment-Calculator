import openai

openai.api_key = "YOUR API KEY HERE"


def getChatResponse(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response


def getImageForPrompt(prompt):
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="256x256",
    )
    return response


def editImageFromPrompt(prompt, imageName):
    response = openai.Image.create_edit(
        prompt=prompt,
        n=1,
        size="256x256",
        image=open(imageName, "rb"),
    )
    return response


def createImageVariation(imageName):
    response = openai.Image.create_variation(
        image=open(imageName, "rb"),
        size="256x256",
        n=3
    )
    return response


def getImageUrl(response):
    return response['data'][0]['url']


# prompt = "Produce 5 prompts for DALLE to generate promotional images of my product. Make the prompts concise, incomplete sentences, specify what is within the frame of each image, and the style of the image. I supplied DALLE with starting images of my product, and my goal is for DALLE to create images containing my product. Base these prompts off of the following product description: My product is a running watch. It uses GPS to track your miles and other information related to running, syncs easily with your smartphone, is water-proof."
# response_content = getChatResponse(prompt).choices[0].message.content
# print(response_content)

# dalle_prompt = "Action shot, a person wearing the watch jumping into a pool, with water droplets flying everywhere. Style is high-energy and exciting, emphasizing the watch's durability."
# dalle_image_url = getImageForPrompt(dalle_prompt)['data'][0]['url']

# dalle_prompt = "Fish-eye shot of water bottle sitting on table. Hand reaches from out of frame to grab bottle."
# response = editImageFromPrompt(dalle_prompt, "tea.png")
# print(response)
# imageUrl = getImageUrl(response)
# print(imageUrl)

response = createImageVariation(
    "sample_images/img-EnETbf3wrgSsEVnwquGwQygW.png")
print(response)

'''
GPT response:
1. Show a runner mid-stride, with the running watch prominently featured on their wrist. Keep the image bright and energetic to match the feeling of a good run!
2. Zoom in on the running watch as it syncs with a smartphone, capturing the ease and simplicity of the process. Consider showing a hand holding the phone to imply that the owner is out and about, on the go.
3. Create a sleek image of the running watch resting on a rock by a scenic vista, with the GPS tracking data clearly displayed on the watch face. The style should be cool and composed, just like the user of the watch.
4. Capture the watch's water-proof feature in an action shot: a person wearing the watch jumping into a pool, with water droplets flying everywhere. The style should be high-energy and exciting, emphasizing the watch's durability.
5. Display the running watch alongside other running gear (e.g. shoes, a water bottle, headphones) to show the watch as an integral part of the runner's toolkit. The style should be composed and balanced, with all the gear arranged aesthetically.

DALLE prompt:
Action shot, a person wearing the watch jumping into a pool, with water droplets flying everywhere. Style is high-energy and exciting, emphasizing the watch's durability.

DALLE response:
https://oaidalleapiprodscus.blob.core.windows.net/private/org-xKgAZa73o2Iblr0I78OO3RCk/user-wOA06Dqq4vIkYdvKW5FprvIo/img-odRd2QYb3wGdvhha9CqnzVJL.png?st=2023-05-01T21%3A33%3A42Z&se=2023-05-01T23%3A33%3A42Z&sp=r&sv=2021-08-06&sr=b&rscd=inline&rsct=image/png&skoid=6aaadede-4fb3-4698-a8f6-684d7786b067&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2023-05-01T17%3A36%3A33Z&ske=2023-05-02T17%3A36%3A33Z&sks=b&skv=2021-08-06&sig=nu1PfMZJDMykP%2BUPdfBNGgqFuOPROgIAHSPUVBZrj4Q%3D
'''
