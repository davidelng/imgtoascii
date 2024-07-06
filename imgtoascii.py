from PIL import Image, ImageDraw, ImageFont
from shutil import get_terminal_size


class AsciiArt:
    def __init__(self, path:str) -> None:
            self._img = Image.open(path)
            self._max_width = self._img.size[0]
            self._max_height = self._img.size[1]
            self._ascii_chars = " .:-=+*#%@"
            self._filled_chars = "░▒▓█"

    def _resize(self, cols:int, fit_terminal:bool=False) -> Image.Image:
        """
        Resize the image and fit terminal width if necessary.
        The width will be set to half the specified width, because using a monospace font
        we're going to duplicate every ascii char to make a square like a pixel
        """
        resized_width = cols//2
        if fit_terminal:
            t_width, t_height = get_terminal_size()
            if cols > t_width:
                resized_width = t_width//2
        elif cols > self._max_width:
            resized_width = self._max_width
        resized_height = int((self._max_height/self._max_width) * resized_width)
        return self._img.resize(
            (resized_width, resized_height), Image.Resampling.NEAREST)
    
    def _get_brightness_char(self, brightness:int, fill:bool=False) -> str:
        """
        Return the most appropriate char (doubled to fit a square) in the ascii grayscale
        based on the brightness of the pixel (a value between 0 and 255)
        """
        grayscale = self._filled_chars if fill else self._ascii_chars
        index = (brightness*(len(grayscale)-1))//255
        return grayscale[index]*2

    def _get_ansi_color(self, char:str, rgb:int|tuple) -> str:
        """
        Return the ansii string to display colored characters in the terminal if true color is supported.
        """
        if type(rgb) == int:
            r = g = b = rgb
        else:
            r, g, b = rgb
        return f"\x1b[38;2;{r};{g};{b}m{char}\x1b[0m"
    
    def _get_ascii_string(self, cols:int, colors:bool=False, fill:bool=False) -> str:
        """
        Returns an ascii art string
        """
        img = self._resize(cols, True)
        if img.mode != "RGB" and colors:
            img = img.convert("RGB")
        grayscale = img.convert("L")

        ascii_string = ""
        width, height = img.size

        for h in range(height):
            for w in range(width):
                px = grayscale.getpixel((w, h))
                char = self._get_brightness_char(px, fill)
                if colors:
                    char = self._get_ansi_color(char, img.getpixel((w, h)))
                ascii_string += char
            ascii_string += "\n"
        
        return ascii_string

    def _get_chars_string(self, cols:int, chars:str, colors:bool=False) -> str:
        """
        Return a representation of the image with the specified characters
        instead of the default grayscale ascii characters
        """
        if chars == "":
            raise ValueError("Chars cannot be empty")

        img = self._resize(cols, True)
        if colors:
            img = img.convert("RGB")
        else:
            img = img.convert("L")

        ascii_string = ""
        width, height = img.size
        i = 0 

        for h in range(height):
            for w in range(width):
                px = img.getpixel((w, h))
                for x in range(2):
                    char = self._get_ansi_color(chars[i], px)
                    ascii_string += char
                    i = (i + 1) % len(chars)
            ascii_string += "\n"

        return ascii_string

    def to_terminal(self, cols:int, colors:bool=False, fill:bool=False, chars:str|None=None) -> None:
        """
        Prints the ascii art into the terminal
        """
        ascii_string = ""
        if chars is None:
            ascii_string = self._get_ascii_string(cols, colors, fill)
        else:
            ascii_string = self._get_chars_string(cols, chars, colors)
        print(ascii_string)

    def to_file(self, cols:int, output:str, fill:bool=False):
        """
        Save the ascii art into a file as text
        """
        img = self._resize(cols)
        grayscale = img.convert("L")
        width, height = img.size
        ascii_string = ""
        for h in range(height):
            for w in range(width):
                px = grayscale.getpixel((w, h))
                char = self._get_brightness_char(px, fill)
                ascii_string += char
            ascii_string += "\n"
        f = open(output, "w")
        f.write(ascii_string)
        f.close()

    # TODO: Make a better implementation
    def to_png(self, cols:int, output:str, colors:bool=False, fill:bool=False) -> None:
        """
        Save the ascii art into a png image
        """
        char_height = 12
        char_width = 12

        img = self._resize(cols)
        img = img.convert("RGB")
        grayscale = img.convert("L")

        width, height = img.size

        out = Image.new("RGB", (width*char_width, height*char_height), color=(0,0,0))
        canvas = ImageDraw.Draw(out)
        font = ImageFont.truetype("fonts/FiraMono-Regular.ttf", char_height)

        for h in range(height):
            for w in range(width):
                px = grayscale.getpixel((w, h))
                char = self._get_brightness_char(px, fill)
                if colors:
                    rgb = img.getpixel((w,h))
                else:
                    rgb = (px, px, px)
                canvas.text((w*char_width,h*char_height), char, font=font, fill=rgb)

        out.save(output)
