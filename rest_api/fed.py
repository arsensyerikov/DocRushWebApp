import asyncio, randint

async def say_hello():
    # print("Привіт!")
    await asyncio.sleep(1)  # Затримка на 1 секунду
    print("Як справи?")
    await asyncio.sleep(2)  
    print("lj,hfysx")
    await asyncio.sleep(3)  
    print("lj,dfghshg")
async def main():
    await say_hello()

# Запуск асинхронного завдання
asyncio.run(main())