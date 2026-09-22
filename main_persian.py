import asyncio
import matplotlib.pyplot as plt
from rubka.asynco import Robot
from rubka.context import Message
import os

bot = Robot("FBAED0ZOEMLXLKFVAFXRRWONKXEVGXEUWMJFFLNGSRPJNIWMNILSKIEMHUCUSAYI")
state = {}

@bot.on_message_text()
async def main(bot: Robot, msg: Message):
    text = msg.text
    chatid = msg.chat_id
    senderid = msg.sender_id
    keywords_rasm = ["/rasm", "رسم", "/draw", "/start"] 
    keywords_help = ["کمک", "راهنما", "/help", " هلپ"]
    keywords_cancel = ["/cancel", "cancel", "لغو"]
    shapes = ["خطی", "میله ای عمودی", "میله ای افقی", "دایره ای"]
    if text in keywords_rasm:
        state[senderid] = {
            "state" : "waiting_shape",
            "shape" : "...",
            "xha1" : "...",
            "yha1" : "...",
            "title" : "...",
            "namex1" : "...",
            "namey1" : "..."
        }
        await msg.reply("""
سلام! لطفا نوع نمودارتو از لیست زیر انتخاب کن:
خطی 
میله ای عمودی
میله ای افقی
دایره ای

برای لغو : لغو
""")
        return
    if text in keywords_help:
        await msg.reply("""برای ساخت نمودار یکی از دستورات زیر را بنویسید:
        /rasm
        /start
        رسم
        /draw
        """)
        return
    if text in keywords_cancel:
        if senderid not in state:
            await msg.reply("شما درحال انجام کاری نیستید.")
            return
        state.pop(senderid, None)
        await msg.reply("ساخت نمودار لغو شد.")
        return
    if senderid in state and state[senderid]["state"] == "waiting_shape":
        if text not in shapes:
            await msg.reply("شکل در لیست موجود نیست. دوباره امتحان کنید.")
            return
        if text == "خطی":
            state[senderid]["shape"] = text
            state[senderid]["state"] = "waiting_xha1"
            await msg.reply_image(path="chart1.png", text="""
    لطفا در این مرحله طبق عکس بالا مقادیر ایکس را مشخص کنید(میتوانند بجز عدد کلمه هم باشند.)
    مانند فرمت زیر:
    1.2.3.4.5 و ...
    یا
    یک.دو.سه.چهار.پنج و ...

    نکته : در بیشترین حالت 20 کلمه یا عدد میتوانید انتخاب کنید.
    نکته : ورودی های محور ایکس ها باید برابر با وای ها باشد!

    برای لغو : لغو
    """)
            return
        elif text == "میله ای عمودی":
            state[senderid]["shape"] = text
            state[senderid]["state"] = "waiting_xha2"
            await msg.reply_image(path="chart2.png", text="""
    لطفا در این مرحله طبق عکس بالا مقادیر ایکس را مشخص کنید(میتوانند بجز عدد کلمه هم باشند.)
    مانند فرمت زیر:
    1.2.3.4.5 و ...
    یا
    یک.دو.سه.چهار.پنج و ...

    نکته : در بیشترین حالت 20 کلمه یا عدد میتوانید انتخاب کنید.
    نکته : ورودی های محور ایکس ها باید برابر با وای ها باشد!

    برای لغو : لغو
    """)
            return
        elif text == "میله ای افقی":
            state[senderid]["shape"] = text
            state[senderid]["state"] = "waiting_xha3"
            await msg.reply_image(path="chart3.png", text="""
    لطفا در این مرحله طبق عکس بالا مقادیر ایکس را مشخص کنید(میتوانند بجز عدد کلمه هم باشند.)
    مانند فرمت زیر:
    1.2.3.4.5 و ...
    یا
    یک.دو.سه.چهار.پنج و ...

    نکته : در بیشترین حالت 20 کلمه یا عدد میتوانید انتخاب کنید.
    نکته : ورودی های محور ایکس ها باید برابر با وای ها باشد!

    برای لغو : لغو
    """)
            return
        elif text == "دایره ای":
            state[senderid]["shape"] = text
            state[senderid]["state"] = "waiting_xha4"
            await msg.reply_image(path="chart4.png", text="""
    لطفا در این مرحله طبق عکس بالا مقادیر داخل دایره ها که بزرگی هر نام را مشخص میکند را مشخص کنید(فقط عدد میتوانید انتخاب کنید.)
    مانند فرمت زیر:
    1.2.3.4.5 و ...

    نکته : در بیشترین حالت 20 کلمه یا عدد میتوانید انتخاب کنید.
    نکته : ورودی های مقادیر داخل دایره باید برابر با نام آن ها باشد!

    برای لغو : لغو
    """)
            return 
    elif senderid in state and state[senderid]["state"] == "waiting_xha1":
        if len(text.split(".")) > 20:
            await msg.reply("بیشتر از 20 عدد یا حرف انتخاب کردی دوباره امتحان کن.")
            return
        state[senderid]["xha1"] = text.split(".")
        xha1 = state[senderid]["xha1"]
        state[senderid]["x_len1"] = len(xha1)
        state[senderid]["state"] = "waiting_yha1"
        await msg.reply_image(path="chart1.png", text="""
لطفا در این مرحله طبق عکس بالا مقادیر وای را مشخص کنید(میتوانند بجز عدد کلمه هم باشند.)
مانند فرمت زیر:
1.2.3.4.5 و ...
یا
یک.دو.سه.چهار.پنج و ...

نکته : در بیشترین حالت 20 کلمه یا عدد میتوانید انتخاب کنید.

برای لغو : لغو
""")
        return
    elif senderid in state and state[senderid]["state"] == "waiting_xha2":
        if len(text.split(".")) > 20:
            await msg.reply("بیشتر از 20 عدد یا حرف انتخاب کردی دوباره امتحان کن.")
            return
        state[senderid]["xha1"] = text.split(".")
        xha1 = state[senderid]["xha1"]
        state[senderid]["x_len1"] = len(xha1)
        state[senderid]["state"] = "waiting_yha2"
        await msg.reply_image(path="chart2.png", text="""
لطفا در این مرحله طبق عکس بالا مقادیر وای را مشخص کنید(میتوانند بجز عدد کلمه هم باشند.)
مانند فرمت زیر:
1.2.3.4.5 و ...
یا
یک.دو.سه.چهار.پنج و ...

نکته : در بیشترین حالت 20 کلمه یا عدد میتوانید انتخاب کنید.

برای لغو : لغو
""")
        return
    elif senderid in state and state[senderid]["state"] == "waiting_xha3":
        if len(text.split(".")) > 20:
            await msg.reply("بیشتر از 20 عدد یا حرف انتخاب کردی دوباره امتحان کن.")
            return
        state[senderid]["xha1"] = text.split(".")
        xha1 = state[senderid]["xha1"]
        state[senderid]["x_len1"] = len(xha1)
        state[senderid]["state"] = "waiting_yha3"
        await msg.reply_image(path="chart3.png", text="""
لطفا در این مرحله طبق عکس بالا مقادیر وای را مشخص کنید(میتوانند بجز عدد کلمه هم باشند.)
مانند فرمت زیر:
1.2.3.4.5 و ...
یا
یک.دو.سه.چهار.پنج و ...

نکته : در بیشترین حالت 20 کلمه یا عدد میتوانید انتخاب کنید.

برای لغو : لغو
""")
        return
    elif senderid in state and state[senderid]["state"] == "waiting_xha4":
        if len(text.split(".")) > 20:
            await msg.reply("بیشتر از 20 عدد یا حرف انتخاب کردی دوباره امتحان کن.")
            return
        try:
            state[senderid]["xha1"] = list(map(int, text.split(".")))
            xha1 = state[senderid]["xha1"]
            state[senderid]["x_len1"] = len(xha1)
            state[senderid]["state"] = "waiting_yha4"
            await msg.reply_image(path="chart4.png", text="""
    لطفا در این مرحله طبق عکس بالا نام های مقادیر را مشخص کنید(میتوانند بجز عدد کلمه هم باشند.)
    مانند فرمت زیر:
    1.2.3.4.5 و ...
    یا
    یک.دو.سه.چهار.پنج و ...

    نکته : در بیشترین حالت 20 کلمه یا عدد میتوانید انتخاب کنید.

    برای لغو : لغو
    """)
            return
        except ValueError:
            await msg.reply("لطفا فقط عدد انتخاب کنید.")
            return
    elif senderid in state and state[senderid]["state"] == "waiting_yha1":
        if len(text.split(".")) > 20:
            await msg.reply("بیشتر از 20 عدد یا حرف انتخاب کردی دوباره امتحان کن.")
            return
        state[senderid]["yha1"] = text.split(".")
        yha1 = state[senderid]["yha1"]
        if len(yha1) != state[senderid]["x_len1"]:
            await msg.reply("ورودی های محور ایکس ها باید برابر با وای ها باشد!")
            return
        state[senderid]["state"] = "waiting_title"
        await msg.reply_image(path="chart1.png", text="""
لطفا موضوع نمودار را مشخص کنید(title)
حداکثر 25 حرف

برای لغو : لغو
""")
        return
    elif senderid in state and state[senderid]["state"] == "waiting_yha2":
        if len(text.split(".")) > 20:
            await msg.reply("بیشتر از 20 عدد یا حرف انتخاب کردی دوباره امتحان کن.")
            return
        state[senderid]["yha1"] = text.split(".")
        yha1 = state[senderid]["yha1"]
        if len(yha1) != state[senderid]["x_len1"]:
            await msg.reply("ورودی های محور ایکس ها باید برابر با وای ها باشد!")
            return
        state[senderid]["state"] = "waiting_title2"
        await msg.reply_image(path="chart2.png", text="""
لطفا موضوع نمودار را مشخص کنید(title)
حداکثر 25 حرف

برای لغو : لغو
""")
        return
    elif senderid in state and state[senderid]["state"] == "waiting_yha3":
        if len(text.split(".")) > 20:
            await msg.reply("بیشتر از 20 عدد یا حرف انتخاب کردی دوباره امتحان کن.")
            return
        state[senderid]["yha1"] = text.split(".")
        yha1 = state[senderid]["yha1"]
        if len(yha1) != state[senderid]["x_len1"]:
            await msg.reply("ورودی های محور ایکس ها باید برابر با وای ها باشد!")
            return
        state[senderid]["state"] = "waiting_title3"
        await msg.reply_image(path="chart3.png", text="""
لطفا موضوع نمودار را مشخص کنید(title)
حداکثر 25 حرف

برای لغو : لغو
""")
        return
    elif senderid in state and state[senderid]["state"] == "waiting_yha4":
        if len(text.split(".")) > 20:
            await msg.reply("بیشتر از 20 عدد یا حرف انتخاب کردی دوباره امتحان کن.")
            return
        state[senderid]["yha1"] = text.split(".")
        yha1 = state[senderid]["yha1"]
        if len(yha1) != state[senderid]["x_len1"]:
            await msg.reply("ورودی های محور ایکس ها باید برابر با وای ها باشد!")
            return
        state[senderid]["state"] = "waiting_title4"
        await msg.reply_image(path="chart4.png", text="""
لطفا موضوع نمودار را مشخص کنید(title)
حداکثر 25 حرف

برای لغو : لغو
""")
        return
    elif senderid in state and state[senderid]["state"] == "waiting_title":
        if len(text) > 25:
            await msg.reply("بیشتر از 25 حرف شد دوباره امتحان کن")
            return
        state[senderid]["title"] = text
        state[senderid]["state"] = "waiting_namex1"
        await msg.reply_image(path="chart1.png", text="""
نام محور ایکس هارا مشخص کن:
حداکثر 25 حرف

برای لغو : لغو
""")
        return
    elif senderid in state and state[senderid]["state"] == "waiting_title2":
        if len(text) > 25:
            await msg.reply("بیشتر از 25 حرف شد دوباره امتحان کن")
            return
        state[senderid]["title"] = text
        state[senderid]["state"] = "waiting_namex2"
        await msg.reply_image(path="chart2.png", text="""
نام محور ایکس هارا مشخص کن:
حداکثر 25 حرف

برای لغو : لغو
""")
        return
    elif senderid in state and state[senderid]["state"] == "waiting_title3":
        if len(text) > 25:
            await msg.reply("بیشتر از 25 حرف شد دوباره امتحان کن")
            return
        state[senderid]["title"] = text
        state[senderid]["state"] = "waiting_namex3"
        await msg.reply_image(path="chart3.png", text="""
نام محور ایکس هارا مشخص کن:
حداکثر 25 حرف

برای لغو : لغو
""")
        return
    elif senderid in state and state[senderid]["state"] == "waiting_title4":
        if len(text) > 25:
            await msg.reply("بیشتر از 25 حرف شد دوباره امتحان کن")
            return
        state[senderid]["title"] = text
        shape = state[senderid]["shape"]
        xha1 = state[senderid]["xha1"]
        yha1 = state[senderid]["yha1"]
        title = state[senderid]["title"]
        try:
            plt.figure()
            plt.pie(xha1, labels=yha1)
            plt.title(title)
            plt.savefig(f"{senderid}.png")
            plt.close()
            sent = await msg.reply_image(path=f"{senderid}.png", text=f"""
نمودار شما با اطلاعات زیر ساخته شد.
{shape}
{xha1}
{yha1}
{title}

لطفا نمودار را ذخیره کنید. این پیام بعد از 15 ثانیه حذف میشود.
""")
            await bot.delete_after(chatid, sent.message_id, 15)
            os.remove(f"{senderid}.png")
        except Exception as e:
            await msg.reply(f"error : {e}")
        finally:
            if os.path.exists(f"{senderid}.png"):
                os.remove(f"{senderid}.png")
            state.pop(senderid, None)
    elif senderid in state and state[senderid]["state"] == "waiting_namex1":
        if len(text) > 25:
            await msg.reply("بیشتر از 25 حرف شد دوباره امتحان کن")
            return
        state[senderid]["namex1"] = text
        state[senderid]["state"] = "waiting_namey1"
        await msg.reply_image(path="chart1.png", text="""
نام محور وای هارا مشخص کن:
حداکثر 25 حرف
""")
        return
    elif senderid in state and state[senderid]["state"] == "waiting_namex2":
        if len(text) > 25:
            await msg.reply("بیشتر از 25 حرف شد دوباره امتحان کن")
            return
        state[senderid]["namex1"] = text
        state[senderid]["state"] = "waiting_namey2"
        await msg.reply_image(path="chart2.png", text="""
نام محور وای هارا مشخص کن:
حداکثر 25 حرف
""")
        return
    elif senderid in state and state[senderid]["state"] == "waiting_namex3":
        if len(text) > 25:
            await msg.reply("بیشتر از 25 حرف شد دوباره امتحان کن")
            return
        state[senderid]["namex1"] = text
        state[senderid]["state"] = "waiting_namey3"
        await msg.reply_image(path="chart3.png", text="""
نام محور وای هارا مشخص کن:
حداکثر 25 حرف
""")
        return
    elif senderid in state and state[senderid]["state"] == "waiting_namey1":
        if len(text) > 25:
            await msg.reply("بیشتر از 25 حرف شد دوباره امتحان کن")
            return
        state[senderid]["namey1"] = text
        shape = state[senderid]["shape"]
        xha1 = state[senderid]["xha1"]
        yha1 = state[senderid]["yha1"]
        title = state[senderid]["title"]
        namex1 = state[senderid]["namex1"]
        namey1 = state[senderid]["namey1"]
        try:
            plt.figure()
            plt.plot(xha1, yha1)
            plt.title(title)
            plt.xlabel(namex1)
            plt.ylabel(namey1)
            plt.savefig(f"{senderid}.png")
            plt.close()
            sent2 = await msg.reply_image(path=f"{senderid}.png", text=f"""
نمودار شما با اطلاعات زیر ساخته شد.
{shape}
{xha1}
{yha1}
{title}
{namex1}
{namey1}

لطفا نمودار را ذخیره کنید. این پیام بعد از 15 ثانیه حذف میشود.
""")
            await bot.delete_after(chatid, sent2.message_id, 15)
            os.remove(f"{senderid}.png")
        except Exception as e:
            await msg.reply(f"error : {e}")
        finally:
            if os.path.exists(f"{senderid}.png"):
                os.remove(f"{senderid}.png")
            state.pop(senderid, None)
    elif senderid in state and state[senderid]["state"] == "waiting_namey2":
        if len(text) > 25:
            await msg.reply("بیشتر از 25 حرف شد دوباره امتحان کن")
            return
        state[senderid]["namey1"] = text
        shape = state[senderid]["shape"]
        xha1 = state[senderid]["xha1"]
        yha1 = state[senderid]["yha1"]
        title = state[senderid]["title"]
        namex1 = state[senderid]["namex1"]
        namey1 = state[senderid]["namey1"]
        try:
            plt.figure()
            plt.bar(xha1, yha1)
            plt.title(title)
            plt.xlabel(namex1)
            plt.ylabel(namey1)
            plt.savefig(f"{senderid}.png")
            plt.close()
            sent3 = await msg.reply_image(path=f"{senderid}.png", text=f"""
نمودار شما با اطلاعات زیر ساخته شد.
{shape}
{xha1}
{yha1}
{title}
{namex1}
{namey1}

لطفا نمودار را ذخیره کنید. این پیام بعد از 15 ثانیه حذف میشود.
""")
            await bot.delete_after(chatid, sent3.message_id, 15)
            os.remove(f"{senderid}.png")
        except Exception as e:
            await msg.reply(f"error : {e}")
        finally:
            if os.path.exists(f"{senderid}.png"):
                os.remove(f"{senderid}.png")
            state.pop(senderid, None)
    elif senderid in state and state[senderid]["state"] == "waiting_namey3":
        if len(text) > 25:
            await msg.reply("بیشتر از 25 حرف شد دوباره امتحان کن")
            return
        state[senderid]["namey1"] = text
        shape = state[senderid]["shape"]
        xha1 = state[senderid]["xha1"]
        yha1 = state[senderid]["yha1"]
        title = state[senderid]["title"]
        namex1 = state[senderid]["namex1"]
        namey1 = state[senderid]["namey1"]
        try:
            plt.figure()
            plt.barh(xha1, yha1)
            plt.title(title)
            plt.xlabel(namex1)
            plt.ylabel(namey1)
            plt.savefig(f"{senderid}.png")
            plt.close()
            sent4 = await msg.reply_image(path=f"{senderid}.png", text=f"""
نمودار شما با اطلاعات زیر ساخته شد.
{shape}
{xha1}
{yha1}
{title}
{namex1}
{namey1}

لطفا نمودار را ذخیره کنید. این پیام بعد از 15 ثانیه حذف میشود.
""")
            await bot.delete_after(chatid, sent4.message_id, 15)
            os.remove(f"{senderid}.png")
        except Exception as e:
            await msg.reply(f"error : {e}")
        finally:
            if os.path.exists(f"{senderid}.png"):
                os.remove(f"{senderid}.png")
            state.pop(senderid, None)

if __name__ == "__main__":
    asyncio.run(bot.run())