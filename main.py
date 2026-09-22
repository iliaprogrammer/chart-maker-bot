import asyncio
import matplotlib.pyplot as plt
from rubka.asynco import Robot
from rubka.context import Message
import os

bot = Robot("YOUR_BOT_TOKEN")
state = {}

@bot.on_message_text()
async def main(bot: Robot, msg: Message):
    text = msg.text
    chatid = msg.chat_id
    senderid = msg.sender_id

    keywords_rasm = ["/rasm", "draw", "/draw", "/start"]
    keywords_help = ["help", "guide", "/help", "help"]
    keywords_cancel = ["/cancel", "cancel", "cancel"]

    shapes = ["Line", "Vertical Bar", "Horizontal Bar", "Pie"]

    if text in keywords_rasm:
        state[senderid] = {
            "state": "waiting_shape",
            "shape": "...",
            "xha1": "...",
            "yha1": "...",
            "title": "...",
            "namex1": "...",
            "namey1": "..."
        }

        await msg.reply("""
Hello! Please choose the type of chart from the list below:

Line
Vertical Bar
Horizontal Bar
Pie

To cancel: cancel
""")
        return

    if text in keywords_help:
        await msg.reply("""To create a chart, use one of the following commands:

/rasm
/start
draw
/draw
""")
        return

    if text in keywords_cancel:
        if senderid not in state:
            await msg.reply("You are not currently creating a chart.")
            return

        state.pop(senderid, None)
        await msg.reply("Chart creation has been cancelled.")
        return

    if senderid in state and state[senderid]["state"] == "waiting_shape":
        if text not in shapes:
            await msg.reply("This chart type is not available in the list. Please try again.")
            return

        if text == "Line":
            state[senderid]["shape"] = text
            state[senderid]["state"] = "waiting_xha1"

            await msg.reply_image(path="chart1.png", text="""
Please enter the X-axis values according to the image above.
They can be numbers or words.

Example:

1.2.3.4.5 ...

or

one.two.three.four.five ...

Note: You can enter a maximum of 20 words or numbers.
Note: The number of X-axis values must be equal to the number of Y-axis values.

To cancel: cancel
""")
            return

        elif text == "Vertical Bar":
            state[senderid]["shape"] = text
            state[senderid]["state"] = "waiting_xha2"

            await msg.reply_image(path="chart2.png", text="""
Please enter the X-axis values according to the image above.
They can be numbers or words.

Example:

1.2.3.4.5 ...

or

one.two.three.four.five ...

Note: You can enter a maximum of 20 words or numbers.
Note: The number of X-axis values must be equal to the number of Y-axis values.

To cancel: cancel
""")
            return

        elif text == "Horizontal Bar":
            state[senderid]["shape"] = text
            state[senderid]["state"] = "waiting_xha3"

            await msg.reply_image(path="chart3.png", text="""
Please enter the X-axis values according to the image above.
They can be numbers or words.

Example:

1.2.3.4.5 ...

or

one.two.three.four.five ...

Note: You can enter a maximum of 20 words or numbers.
Note: The number of X-axis values must be equal to the number of Y-axis values.

To cancel: cancel
""")
            return

        elif text == "Pie":
            state[senderid]["shape"] = text
            state[senderid]["state"] = "waiting_xha4"

            await msg.reply_image(path="chart4.png", text="""
Please enter the values inside the pie chart that determine the size of each label.
Only numbers are allowed.

Example:

1.2.3.4.5 ...

Note: You can enter a maximum of 20 values.
Note: The number of values must be equal to the number of labels.

To cancel: cancel
""")
            return

    elif senderid in state and state[senderid]["state"] == "waiting_xha1":
        if len(text.split(".")) > 20:
            await msg.reply("You entered more than 20 values. Please try again.")
            return

        state[senderid]["xha1"] = text.split(".")
        xha1 = state[senderid]["xha1"]
        state[senderid]["x_len1"] = len(xha1)
        state[senderid]["state"] = "waiting_yha1"

        await msg.reply_image(path="chart1.png", text="""
Please enter the Y-axis values according to the image above.
They can be numbers or words.

Example:

1.2.3.4.5 ...

or

one.two.three.four.five ...

Note: You can enter a maximum of 20 words or numbers.

To cancel: cancel
""")
        return

    elif senderid in state and state[senderid]["state"] == "waiting_xha2":
        if len(text.split(".")) > 20:
            await msg.reply("You entered more than 20 values. Please try again.")
            return

        state[senderid]["xha1"] = text.split(".")
        xha1 = state[senderid]["xha1"]
        state[senderid]["x_len1"] = len(xha1)
        state[senderid]["state"] = "waiting_yha2"

        await msg.reply_image(path="chart2.png", text="""
Please enter the Y-axis values according to the image above.
They can be numbers or words.

Example:

1.2.3.4.5 ...

or

one.two.three.four.five ...

Note: You can enter a maximum of 20 words or numbers.

To cancel: cancel
""")
        return

    elif senderid in state and state[senderid]["state"] == "waiting_xha3":
        if len(text.split(".")) > 20:
            await msg.reply("You entered more than 20 values. Please try again.")
            return

        state[senderid]["xha1"] = text.split(".")
        xha1 = state[senderid]["xha1"]
        state[senderid]["x_len1"] = len(xha1)
        state[senderid]["state"] = "waiting_yha3"

        await msg.reply_image(path="chart3.png", text="""
Please enter the Y-axis values according to the image above.
They can be numbers or words.

Example:

1.2.3.4.5 ...

or

one.two.three.four.five ...

Note: You can enter a maximum of 20 words or numbers.

To cancel: cancel
""")
        return

    elif senderid in state and state[senderid]["state"] == "waiting_xha4":
        if len(text.split(".")) > 20:
            await msg.reply("You entered more than 20 values. Please try again.")
            return

        try:
            state[senderid]["xha1"] = list(map(int, text.split(".")))
            xha1 = state[senderid]["xha1"]
            state[senderid]["x_len1"] = len(xha1)
            state[senderid]["state"] = "waiting_yha4"

            await msg.reply_image(path="chart4.png", text="""
Please enter the labels for the values.
They can be numbers or words.

Example:

1.2.3.4.5 ...

or

one.two.three.four.five ...

Note: You can enter a maximum of 20 labels.

To cancel: cancel
""")
            return

        except ValueError:
            await msg.reply("Please enter numbers only.")
            return

    elif senderid in state and state[senderid]["state"] == "waiting_yha1":
        if len(text.split(".")) > 20:
            await msg.reply("You entered more than 20 values. Please try again.")
            return

        state[senderid]["yha1"] = text.split(".")
        yha1 = state[senderid]["yha1"]

        if len(yha1) != state[senderid]["x_len1"]:
            await msg.reply("The number of X-axis values must be equal to the number of Y-axis values!")
            return

        state[senderid]["state"] = "waiting_title"

        await msg.reply_image(path="chart1.png", text="""
Please enter the chart title.

Maximum 25 characters.

To cancel: cancel
""")
        return

    elif senderid in state and state[senderid]["state"] == "waiting_yha2":
        if len(text.split(".")) > 20:
            await msg.reply("You entered more than 20 values. Please try again.")
            return

        state[senderid]["yha1"] = text.split(".")
        yha1 = state[senderid]["yha1"]

        if len(yha1) != state[senderid]["x_len1"]:
            await msg.reply("The number of X-axis values must be equal to the number of Y-axis values!")
            return

        state[senderid]["state"] = "waiting_title2"

        await msg.reply_image(path="chart2.png", text="""
Please enter the chart title.

Maximum 25 characters.

To cancel: cancel
""")
        return

    elif senderid in state and state[senderid]["state"] == "waiting_yha3":
        if len(text.split(".")) > 20:
            await msg.reply("You entered more than 20 values. Please try again.")
            return

        state[senderid]["yha1"] = text.split(".")
        yha1 = state[senderid]["yha1"]

        if len(yha1) != state[senderid]["x_len1"]:
            await msg.reply("The number of X-axis values must be equal to the number of Y-axis values!")
            return

        state[senderid]["state"] = "waiting_title3"

        await msg.reply_image(path="chart3.png", text="""
Please enter the chart title.

Maximum 25 characters.

To cancel: cancel
""")
        return

    elif senderid in state and state[senderid]["state"] == "waiting_yha4":
        if len(text.split(".")) > 20:
            await msg.reply("You entered more than 20 values. Please try again.")
            return

        state[senderid]["yha1"] = text.split(".")
        yha1 = state[senderid]["yha1"]

        if len(yha1) != state[senderid]["x_len1"]:
            await msg.reply("The number of values must be equal to the number of labels!")
            return

        state[senderid]["state"] = "waiting_title4"

        await msg.reply_image(path="chart4.png", text="""
Please enter the chart title.

Maximum 25 characters.

To cancel: cancel
""")
        return

    elif senderid in state and state[senderid]["state"] == "waiting_title":
        if len(text) > 25:
            await msg.reply("The title is longer than 25 characters. Please try again.")
            return

        state[senderid]["title"] = text
        state[senderid]["state"] = "waiting_namex1"

        await msg.reply_image(path="chart1.png", text="""
Please enter the name of the X-axis.

Maximum 25 characters.

To cancel: cancel
""")
        return

    elif senderid in state and state[senderid]["state"] == "waiting_title2":
        if len(text) > 25:
            await msg.reply("The title is longer than 25 characters. Please try again.")
            return

        state[senderid]["title"] = text
        state[senderid]["state"] = "waiting_namex2"

        await msg.reply_image(path="chart2.png", text="""
Please enter the name of the X-axis.

Maximum 25 characters.

To cancel: cancel
""")
        return

    elif senderid in state and state[senderid]["state"] == "waiting_title3":
        if len(text) > 25:
            await msg.reply("The title is longer than 25 characters. Please try again.")
            return

        state[senderid]["title"] = text
        state[senderid]["state"] = "waiting_namex3"

        await msg.reply_image(path="chart3.png", text="""
Please enter the name of the X-axis.

Maximum 25 characters.

To cancel: cancel
""")
        return

    elif senderid in state and state[senderid]["state"] == "waiting_title4":
        if len(text) > 25:
            await msg.reply("The title is longer than 25 characters. Please try again.")
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
Your chart has been created with the following information.

{shape}
{xha1}
{yha1}
{title}

Please save the chart. This message will be deleted after 15 seconds.
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
            await msg.reply("The name is longer than 25 characters. Please try again.")
            return

        state[senderid]["namex1"] = text
        state[senderid]["state"] = "waiting_namey1"

        await msg.reply_image(path="chart1.png", text="""
Please enter the name of the Y-axis.

Maximum 25 characters.
""")
        return

    elif senderid in state and state[senderid]["state"] == "waiting_namex2":
        if len(text) > 25:
            await msg.reply("The name is longer than 25 characters. Please try again.")
            return

        state[senderid]["namex1"] = text
        state[senderid]["state"] = "waiting_namey2"

        await msg.reply_image(path="chart2.png", text="""
Please enter the name of the Y-axis.

Maximum 25 characters.
""")
        return

    elif senderid in state and state[senderid]["state"] == "waiting_namex3":
        if len(text) > 25:
            await msg.reply("The name is longer than 25 characters. Please try again.")
            return

        state[senderid]["namex1"] = text
        state[senderid]["state"] = "waiting_namey3"

        await msg.reply_image(path="chart3.png", text="""
Please enter the name of the Y-axis.

Maximum 25 characters.
""")
        return

    elif senderid in state and state[senderid]["state"] == "waiting_namey1":
        if len(text) > 25:
            await msg.reply("The name is longer than 25 characters. Please try again.")
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
Your chart has been created with the following information.

{shape}
{xha1}
{yha1}
{title}
{namex1}
{namey1}

Please save the chart. This message will be deleted after 15 seconds.
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
            await msg.reply("The name is longer than 25 characters. Please try again.")
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
Your chart has been created with the following information.

{shape}
{xha1}
{yha1}
{title}
{namex1}
{namey1}

Please save the chart. This message will be deleted after 15 seconds.
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
            await msg.reply("The name is longer than 25 characters. Please try again.")
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
Your chart has been created with the following information.

{shape}
{xha1}
{yha1}
{title}
{namex1}
{namey1}

Please save the chart. This message will be deleted after 15 seconds.
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