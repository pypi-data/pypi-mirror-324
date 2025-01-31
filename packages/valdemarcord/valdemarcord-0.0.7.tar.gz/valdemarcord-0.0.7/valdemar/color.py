from colorama import init
init()

class Color:
    @staticmethod
    def fade_text(text: str, start_rgb: tuple, end_rgb: tuple) -> str:
        result = ""
        length = len(text)
        for i in range(length):
            progress = i / (length - 1) if length > 1 else 0
            r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * progress)
            g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * progress)
            b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * progress)
            result += f"\033[38;2;{r};{g};{b}m{text[i]}"
        return result + "\033[0m"

    #warm
    @classmethod
    def red_to_orange(cls, text: str) -> str:
        return cls.fade_text(text, (255, 0, 0), (255, 165, 0))
    
    @classmethod
    def orange_to_yellow(cls, text: str) -> str:
        return cls.fade_text(text, (255, 165, 0), (255, 255, 0))
    
    @classmethod
    def yellow_to_red(cls, text: str) -> str:
        return cls.fade_text(text, (255, 255, 0), (255, 0, 0))

    #cool ig
    @classmethod
    def blue_to_purple(cls, text: str) -> str:
        return cls.fade_text(text, (0, 0, 255), (128, 0, 128))
    
    @classmethod
    def purple_to_pink(cls, text: str) -> str:
        return cls.fade_text(text, (128, 0, 128), (255, 192, 203))
    
    @classmethod
    def cyan_to_blue(cls, text: str) -> str:
        return cls.fade_text(text, (0, 255, 255), (0, 0, 255))

    #nature
    @classmethod
    def green_to_yellow(cls, text: str) -> str:
        return cls.fade_text(text, (0, 255, 0), (255, 255, 0))
    
    @classmethod
    def forest_to_lime(cls, text: str) -> str:
        return cls.fade_text(text, (34, 139, 34), (50, 205, 50))
    
    @classmethod
    def teal_to_cyan(cls, text: str) -> str:
        return cls.fade_text(text, (0, 128, 128), (0, 255, 255))

    # sunset
    @classmethod
    def purple_to_orange(cls, text: str) -> str:
        return cls.fade_text(text, (128, 0, 128), (255, 165, 0))
    
    @classmethod
    def pink_to_gold(cls, text: str) -> str:
        return cls.fade_text(text, (255, 192, 203), (255, 215, 0))
    
    @classmethod
    def magenta_to_red(cls, text: str) -> str:
        return cls.fade_text(text, (255, 0, 255), (255, 0, 0))

    # ocean
    @classmethod
    def deep_blue_to_cyan(cls, text: str) -> str:
        return cls.fade_text(text, (0, 0, 139), (0, 255, 255))
    
    @classmethod
    def turquoise_to_blue(cls, text: str) -> str:
        return cls.fade_text(text, (64, 224, 208), (0, 0, 255))
    
    @classmethod
    def aqua_to_marine(cls, text: str) -> str:
        return cls.fade_text(text, (127, 255, 212), (0, 128, 128))

    # special
    @classmethod
    def rainbow(cls, text: str) -> str:
        colors = [(255,0,0), (255,127,0), (255,255,0), (0,255,0), (0,0,255), (75,0,130), (148,0,211)]
        result = ""
        for i, char in enumerate(text):
            color = colors[i % len(colors)]
            result += f"\033[38;2;{color[0]};{color[1]};{color[2]}m{char}"
        return result + "\033[0m"
    
    @classmethod
    def neon_pulse(cls, text: str) -> str:
        return cls.fade_text(text, (255, 0, 255), (0, 255, 255))
    
    @classmethod
    def fire(cls, text: str) -> str:
        return cls.fade_text(text, (255, 0, 0), (255, 215, 0))
    
    @classmethod
    def ice(cls, text: str) -> str:
        return cls.fade_text(text, (173, 216, 230), (0, 191, 255))
    # Add these new methods to your existing Color class:

    # Cosmic Colors
    @classmethod
    def galaxy_purple_to_blue(cls, text: str) -> str:
        return cls.fade_text(text, (147, 51, 234), (0, 183, 255))
    
    @classmethod
    def nebula_pink_to_teal(cls, text: str) -> str:
        return cls.fade_text(text, (255, 0, 255), (0, 128, 128))
    
    @classmethod
    def starlight_white_to_blue(cls, text: str) -> str:
        return cls.fade_text(text, (255, 255, 255), (30, 144, 255))

    # Tropical Vibes
    @classmethod
    def sunset_orange_to_pink(cls, text: str) -> str:
        return cls.fade_text(text, (255, 110, 0), (255, 89, 143))
    
    @classmethod
    def paradise_green_to_blue(cls, text: str) -> str:
        return cls.fade_text(text, (0, 255, 162), (0, 196, 255))
    
    @classmethod
    def tropical_yellow_to_green(cls, text: str) -> str:
        return cls.fade_text(text, (255, 222, 0), (0, 255, 144))

    # Neon Dreams
    @classmethod
    def cyber_blue_to_purple(cls, text: str) -> str:
        return cls.fade_text(text, (0, 255, 255), (255, 0, 255))
    
    @classmethod
    def retro_pink_to_blue(cls, text: str) -> str:
        return cls.fade_text(text, (255, 51, 153), (51, 153, 255))
    
    @classmethod
    def synthwave_purple_to_pink(cls, text: str) -> str:
        return cls.fade_text(text, (128, 0, 255), (255, 0, 128))

    # Royal Colors
    @classmethod
    def royal_gold_to_purple(cls, text: str) -> str:
        return cls.fade_text(text, (255, 215, 0), (138, 43, 226))
    
    @classmethod
    def emerald_to_sapphire(cls, text: str) -> str:
        return cls.fade_text(text, (0, 168, 107), (15, 82, 186))
    
    @classmethod
    def ruby_to_amethyst(cls, text: str) -> str:
        return cls.fade_text(text, (224, 17, 95), (153, 102, 204))

    # Electric Vibes
    @classmethod
    def voltage_yellow_to_cyan(cls, text: str) -> str:
        return cls.fade_text(text, (255, 255, 0), (0, 255, 255))
    
    @classmethod
    def plasma_blue_to_pink(cls, text: str) -> str:
        return cls.fade_text(text, (51, 153, 255), (255, 51, 153))
    
    @classmethod
    def lightning_white_to_blue(cls, text: str) -> str:
        return cls.fade_text(text, (255, 255, 255), (0, 128, 255))

    # Candy Colors
    @classmethod
    def bubblegum_pink_to_blue(cls, text: str) -> str:
        return cls.fade_text(text, (255, 182, 193), (135, 206, 235))
    
    @classmethod
    def cotton_candy_blue_to_pink(cls, text: str) -> str:
        return cls.fade_text(text, (137, 207, 240), (255, 182, 193))
    
    @classmethod
    def lollipop_red_to_white(cls, text: str) -> str:
        return cls.fade_text(text, (255, 0, 0), (255, 255, 255))
