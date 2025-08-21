'''
| Make the project in edit mode

>>>  pip install -e .

>>> command here ????

|
'''
import platform
from argparse import ArgumentParser, Namespace
import asyncio
from googletrans import Translator


def get_cli_value()->tuple[float,float,str]:
   pass


async def translate_text():
     async with Translator() as translator:
       result = await translator.translate('안녕하세요.')
       print(result)  # <Translated src=ko dest=en text=Good evening. pronunciation=Good evening.>
       result = await translator.translate('안녕하세요.', dest='ja')
       print(result)  # <Translated src=ko dest=ja text=こんにちは。 pronunciation=Kon'nichiwa.>
       result = await translator.translate('veritas lux mea', src='la')
       print(result)  # <Translated src=la dest=en text=The truth is my light pronunciation=The truth is my light>
       result = await translator.translate('Hej ', src='sv')
       print(result)  # <Translated src=la dest=en text=The truth is my light pronunciation=The truth is my lightsss>

def main()-> None:
    asyncio.run(translate_text())
    """
    This is the main function that executes the program.
    This function uses argparse to handle input from the command line.

    Command-line arguments
    ----------------------
    -p : float
        energy warning level; default to 50 dBm
    -d : str
        device name default to 'ttyACM0'

    Examples:
        >>> rfcentral -p 65.55 -d ttyACM0
    """
    parser = ArgumentParser(prog="rfcentral", usage="rfcentral -p 65.55 -d ttyACM0",description="RF Central Command Line Interface")


    parser.add_argument(
        '-p',
        help='frequency engergy power level; if exceeded will give beep as warning',
        type=float,
        nargs='?',
        default=50.00,
        metavar='power'
     )
    parser.add_argument(
        '-d',
        help= 'device name  or RF device receiver name',
        type= str,
        default = 'ttyACM0',
        nargs='?',
        metavar = 'device'

     )

    args : Namespace = parser.parse_args()
    power:float = args.p
    device:str = args.d


# this is important so that it does not run from pytest
if __name__ == "__main__":
    main()

