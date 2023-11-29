import lightbulb
import math

plugin = lightbulb.Plugin('convert')
plugin.add_checks(
    lightbulb.guild_only
)

DISTANCE = ["cm", "m", "km", "in", "ft", "yd", "mi"]
VELOCITY = ["m/s", "kmh", "mph"]
MASS = ["mg", "g", "kg", "oz", "lbs"]
TEMP = ["c", "f", "k"]
TIME = ["s", "min", "hr", "day"]

options = DISTANCE + VELOCITY + MASS + TEMP + TIME

@plugin.command
@lightbulb.option('unit2', "Second unit", type=str, required=True, choices=options)
@lightbulb.option('unit1', "First unit", type=str, required=True, choices=options)
@lightbulb.option('num', "Number to convert", type=float, required=True)
@lightbulb.command('convert','Convert between units', pass_options=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def convert(ctx: lightbulb.Context, num: float, unit1: str, unit2: str):
    try:
        if unit1 in DISTANCE and unit2 in DISTANCE:
            # cm -> unit
            if unit1 == "cm" and unit2 == "m":
                result = num/100
            elif unit1 == "cm" and unit2 == "km":
                result = num/100000
            elif unit1 == "cm" and unit2 == "in":
                result = num/2.54
            elif unit1 == "cm" and unit2 == "ft":
                result = num/30.48
            elif unit1 == "cm" and unit2 == "yd":
                result = num/91.44
            elif unit1 == "cm" and unit2 == "mi":
                result = num/160900

            # m -> unit
            elif unit1 == "m" and unit2 == "cm":
                result = num*100
            elif unit1 == "m" and unit2 == "km":
                result = num*1000
            elif unit1 == "m" and unit2 == "in":
                result = num*39.37
            elif unit1 == "m" and unit2 == "ft":
                result = num*3.281
            elif unit1 == "m" and unit2 == "yd":
                result = num*1.094
            elif unit1 == "m" and unit2 == "mi":
                result = num/1609
            
            # km -> unit
            elif unit1 == "km" and unit2 == "cm":
                result = num*100000
            elif unit1 == "km" and unit2 == "m":
                result = num*1000
            elif unit1 == "km" and unit2 == "in":
                result = num*39370
            elif unit1 == "km" and unit2 == "ft":
                result = num*3281
            elif unit1 == "km" and unit2 == "yd":
                result = num*1094
            elif unit1 == "km" and unit2 == "mi":
                result = num/1.609

            # in -> unit
            elif unit1 == "in" and unit2 == "cm":
                result = num*2.54
            elif unit1 == "in" and unit2 == "m":
                result = num/39.37
            elif unit1 == "in" and unit2 == "km":
                result = num/39370
            elif unit1 == "in" and unit2 == "ft":
                result = num/12
            elif unit1 == "in" and unit2 == "yd":
                result = num/36
            elif unit1 == "in" and unit2 == "mi":
                result = num/63360
            
            # ft -> unit
            elif unit1 == "ft" and unit2 == "cm":
                result = num*30.48
            elif unit1 == "ft" and unit2 == "m":
                result = num/3.281
            elif unit1 == "ft" and unit2 == "km":
                result = num/3281
            elif unit1 == "ft" and unit2 == "in":
                result = num*12
            elif unit1 == "ft" and unit2 == "yd":
                result = num/3
            elif unit1 == "ft" and unit2 == "mi":
                result = num/5280

            # yd -> unit
            elif unit1 == "yd" and unit2 == "cm":
                result = num*91.44
            elif unit1 == "yd" and unit2 == "m":
                result = num/1.094
            elif unit1 == "yd" and unit2 == "km":
                result = num/1094
            elif unit1 == "yd" and unit2 == "in":
                result = num*36
            elif unit1 == "yd" and unit2 == "ft":
                result = num*3
            elif unit1 == "yd" and unit2 == "mi":
                result = num/1760

            # mi -> unit
            elif unit1 == "mi" and unit2 == "cm":
                result = num*160900
            elif unit1 == "mi" and unit2 == "m":
                result = num*1609
            elif unit1 == "mi" and unit2 == "km":
                result = num*1.609
            elif unit1 == "mi" and unit2 == "in":
                result = num*63360
            elif unit1 == "mi" and unit2 == "ft":
                result = num*5280
            elif unit1 == "mi" and unit2 == "yd":
                result = num*1760
            
            else:
                result = num
            

        elif unit1 in VELOCITY and unit2 in VELOCITY:
            # m/s -> unit
            if unit1 == "m/s" and unit2 == "kmh":
                result = num*3.6
            elif unit1 == "m/s" and unit2 == "mph":
                result = num*2.237

            # kmh -> unit
            elif unit1 == "kmh" and unit2 == "m/s":
                result = num/3.6
            elif unit1 == "kmh" and unit2 == "mph":
                result = num/1.609
            
            # mps -> unit
            elif unit1 == "mph" and unit2 == "m/s":
                result = num/2.237
            elif unit1 == "mph" and unit2 == "kmh":
                result = num*1.609

            else:
                result = num

        elif unit1 in MASS and unit2 in MASS:
            # mg -> unit
            if unit1 == "mg" and unit2 == "g":
                result = num/1000
            elif unit1 == "mg" and unit2 == "kg":
                result = num/1000000
            elif unit1 == "mg" and unit2 == "oz":
                result = num/28350
            elif unit1 == "mg" and unit2 == "lbs":
                result = num/453600


            # g -> unit
            elif unit1 == "g" and unit2 == "mg":
                result = num*1000
            elif unit1 == "g" and unit2 == "kg":
                result = num/1000
            elif unit1 == "g" and unit2 == "oz":
                result = num/28.35
            elif unit1 == "g" and unit2 == "lbs":
                result = num/453.6
            
            # kg -> unit
            elif unit1 == "kg" and unit2 == "mg":
                result = num*1000000
            elif unit1 == "kg" and unit2 == "g":
                result = num*1000
            elif unit1 == "kg" and unit2 == "oz":
                result = num*35.274
            elif unit1 == "kg" and unit2 == "lbs":
                result = num*2.205

            # oz -> unit
            elif unit1 == "oz" and unit2 == "mg":
                result = num*28350
            elif unit1 == "oz" and unit2 == "g":
                result = num*28.35
            elif unit1 == "oz" and unit2 == "kg":
                result = num/35.274
            elif unit1 == "oz" and unit2 == "lbs":
                result = num/16
            
            # lbs -> unit
            elif unit1 == "lbs" and unit2 == "mg":
                result = num*453600
            elif unit1 == "lbs" and unit2 == "g":
                result = num*453.6
            elif unit1 == "lbs" and unit2 == "kg":
                result = num/2.205
            elif unit1 == "lbs" and unit2 == "oz":
                result = num*16
            
            else:
                result = num

        elif unit1 in TEMP and unit2 in TEMP:
            # c -> unit
            if unit1 == "c" and unit2 == "f":
                result = (num * (9/5)) + 32
            elif unit1 == "c" and unit2 == "k":
                result = num + 273.15 

            # f -> unit
            elif unit1 == "f" and unit2 == "c":
                result = (num -32) * (5/9)
            elif unit1 == "f" and unit2 == "k":
                result = (num - 32) * (5/9) + 273.15 
            
            # k -> unit
            elif unit1 == "k" and unit2 == "c":
                result = num - 273.15 
            elif unit1 == "k" and unit2 == "f":
                result = (num - 273.15 ) * (9/5) + 32

            else:
                result = num

        elif unit1 in TIME and unit2 in TIME:
            # s -> unit
            if unit1 == "s" and unit2 == "min":
                result = num/60
            elif unit1 == "s" and unit2 == "hr":
                result = num/3600
            elif unit1 == "s" and unit2 == "day":
                result = num/86400
            
            # min -> unit
            elif unit1 == "min" and unit2 == "s":
                result = num*60
            elif unit1 == "min" and unit2 == "hr":
                result = num/60
            elif unit1 == "min" and unit2 == "day":
                result = num/1440

            # hr -> unit
            elif unit1 == "hr" and unit2 == "s":
                result = num*3600
            elif unit1 == "hr" and unit2 == "min":
                result = num*60
            elif unit1 == "hr" and unit2 == "day":
                result = num/24

            # day -> unit
            elif unit1 == "day" and unit2 == "s":
                result = num*86400
            elif unit1 == "day" and unit2 == "min":
                result = num*1440
            elif unit1 == "day" and unit2 == "hr":
                result = num*24

            else:
                result = num
        else:
            await ctx.respond("Unable to convert those units.")
            return
        
        await ctx.respond(f"{num}{unit1} = {result}{unit2}")
    except:
        await ctx.respond("That conversion results in a number that is too big or small for me to compute.")

def load(bot):
    bot.add_plugin(plugin)
