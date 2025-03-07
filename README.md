# Report Weather With Python Asyncio

## ผู้ทำ

นายปุรัสกร เกียรติ์นนทพัทธ์ 6710110270

## หลักการของ asyncio

Asyncio ใน Python ใช้สำหรับเขียนโปรแกรม asynchronous I/O แบบ event loop และ coroutines เพื่อให้โปรแกรมสามารถทำงานหลายอย่างพร้อมกันได้โดยไม่ต้องรอให้งานหนึ่งเสร็จก่อนจึงเริ่มงานถัดไป

1. Event Loop
   Event Loop เป็นตัวจัดการและรันงานต่าง ๆ ที่เป็น asynchronous โดยคอยตรวจสอบ coroutine ไหนพร้อมทำงาน (เช่น เมื่อ I/O operation เสร็จสิ้น) และสลับการทำงานระหว่าง coroutines ต่าง ๆ

2. Coroutines
   Coroutine คือฟังก์ชันที่สามารถหยุดการทำงานชั่วคราว (pause) และกลับมาทำงานต่อ (resume) ได้ ใน Python ซึ่งผมใช้ async def เพื่อประกาศ coroutine ภายใน coroutine เราจะใช้ await เพื่อหยุดการทำงานชั่วคราวจนกว่า task ที่รออยู่จะเสร็จสิ้น

3. Tasks
   Task คือการนำ coroutine มาสร้างเป็น task เพื่อให้ event loop สามารถรันมันได้ เราสามารถสร้าง task ด้วย asyncio.create_task() หรือใช้ asyncio.gather() เพื่อรันหลาย task พร้อมกัน

## หลักการโปรแกรมดึงข้อมูลสภาพอากาศ กับ asyncio

### 1. ฟังก์ชัน fetch_weather(city)

```bash
async def fetch_weather(city):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(BASE_URL, params=params) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                print(f"เกิดข้อผิดพลาดในการดึงข้อมูลสำหรับเมือง {city}")
                return None
```

async def: ประกาศฟังก์ชันนี้เป็น coroutine

async with: ใช้สำหรับจัดการ asynchronous context manager (เช่น การเปิดและปิด session)

await response.json(): หยุดการทำงานชั่วคราวจนกว่า response จะถูกแปลงเป็น JSON เสร็จ

เหตุผลที่ใช้ asyncio: การดึงข้อมูลจาก API เป็น I/O-bound operation (ต้องรอการตอบกลับจากเซิร์ฟเวอร์) ซึ่งเหมาะกับการใช้ asyncio เพื่อให้โปรแกรมไม่ต้องรอจนกว่า request จะเสร็จ

### 2. ฟังก์ชัน display_weather(city)

```bash
  async def display_weather(city):
  weather_data = await fetch_weather(city)
  if weather_data:
  print(f"\nข้อมูลสภาพอากาศสำหรับเมือง {city}:")
  print(f"อุณหภูมิ: {weather_data['main']['temp']}°C")
  print(f"สภาพอากาศ: {weather_data['weather'][0]['description']}")
  print(f"ความชื้น: {weather_data['main']['humidity']}%")
  else:
  print(f"ไม่สามารถดึงข้อมูลสำหรับเมือง {city} ได้")
  await fetch_weather(city): หยุดการทำงานชั่วคราวจนกว่าฟังก์ชัน fetch_weather จะเสร็จสิ้นและคืนค่ากลับมา
```

เหตุผลที่ใช้ asyncio: ฟังก์ชันนี้ต้องรอผลลัพธ์จาก fetch_weather ซึ่งเป็น asynchronous operation

### 3. ฟังก์ชัน main()

```bash
    async def main():
    cities = ["Bangkok", "London", "New York", "Tokyo", "Paris"]

        tasks = [display_weather(city) for city in cities]
        await asyncio.gather(*tasks)

    tasks = [display_weather(city) for city in cities]: สร้าง task สำหรับดึงข้อมูลสภาพอากาศของทุกเมือง

    await asyncio.gather(\*tasks): รันทุก task พร้อมกันและรอจนกว่าทุก task จะเสร็จสิ้น
```

เหตุผลที่ใช้ asyncio: เราต้องการดึงข้อมูลสภาพอากาศจากหลายเมืองพร้อมกัน โดยไม่ต้องรอให้เมืองหนึ่งเสร็จก่อนจึงเริ่มเมืองถัดไป

### 4. การรันโปรแกรม

```bash
   if **name** == "**main**":
   asyncio.run(main())
```

เริ่มรัน event loop และเรียกฟังก์ชัน main() ซึ่งเป็น coroutine

## เหตุผลที่ใช้ asyncio: เพื่อให้โปรแกรมทำงานแบบ asynchronous โดยรวม

### ภาพรวมการทำงานของโปรแกรม

1. เริ่มต้น: โปรแกรมเริ่มด้วยการเรียก asyncio.run(main()) ซึ่งเริ่ม event loop

2. สร้าง tasks: ใน main() เราสร้าง task สำหรับดึงข้อมูลสภาพอากาศของแต่ละเมือง

3. รัน tasks พร้อมกัน: asyncio.gather(\*tasks) จะรันทุก task พร้อมกัน

4. หยุดรอ I/O: เมื่อ fetch_weather ส่ง HTTP request และรอ response โปรแกรมจะหยุดรอชั่วคราวและสลับไปทำงาน task อื่น

5. แสดงผล: เมื่อได้ข้อมูลจาก API แล้ว โปรแกรมจะแสดงผลข้อมูลสภาพอากาศ

6. จบการทำงาน: เมื่อทุก task เสร็จสิ้น event loop จะหยุดทำงาน

เหตุผลที่เลือกโปรแกรมนี้ ใช้กับ asyncio :
I/O-bound Operation: การดึงข้อมูลจาก API เป็นงานที่ต้องรอ I/O (เช่น การรอ response จากเซิร์ฟเวอร์) ซึ่ง asyncio ช่วยให้โปรแกรมไม่ต้องรอจนกว่า I/O operation จะเสร็จ

ประสิทธิภาพโปรแกรมนี้ ใช้กับ asyncio :
การใช้ asyncio ช่วยให้โปรแกรมสามารถดึงข้อมูลจากหลายเมืองพร้อมกันได้ โดยไม่ต้องรอให้เมืองหนึ่งเสร็จก่อนจึงเริ่มเมืองถัดไป รวมถึง asyncio ใช้ทรัพยากรน้อยกว่าเมื่อเทียบกับการใช้ threads หรือ processes

### สรุป

asyncio ช่วยให้โปรแกรมสามารถทำงานหลายอย่างพร้อมกันได้โดยไม่ต้องรอ I/O operation ให้เสร็จก่อน Coroutines และ Tasks เป็นเครื่องมือสำคัญในการเขียนโปรแกรมแบบ asynchronous Event Loop เป็นตัวจัดการที่คอยสลับการทำงานระหว่าง coroutines ต่าง ๆ
