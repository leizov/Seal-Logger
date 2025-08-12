import random, datetime, logging

class FileSealLogger(logging.Formatter):
    def __init__(self, logger_prefix: str):
        super().__init__()
        self.logger_prefix = logger_prefix
    def format(self, record):
        try:
            time_str = datetime.datetime.now().strftime('%H:%M:%S')
            return (
                f"[{self.logger_prefix}][{time_str}] {record.levelname[0]}: {record.msg}"
            )
        except Exception as e:
            print(f'ошибка в файловом логгере: {e}')
            return super().format(record)

class ConsoleSealLogger(logging.Formatter):
    def __init__(self, logger_prefix: str):
        super().__init__()
        self.logger_prefix = logger_prefix
        self.time_color = '\033[38;5;175m'
        self.frames = ["ᶘ ᵒᴥᵒᶅ", "ᶘ ͡°ᴥ͡°ᶅ", "ᶘ ͡ᵔᴥ ͡ᵔᶅ"]
        self.seal_index = 0
        self.reset = '\033[0m'
        self.level_colors = {
            'DEBUG': '\033[38;5;117m',
            'INFO': '\033[38;5;183m',
            'WARNING': '\033[38;5;219m',
            'ERROR': '\033[38;5;207m',
            'CRITICAL': '\033[38;5;201m'
        }
        self.prefix_colors = [
            (135,206,235), (72,209,204),(230,240,255),(65, 105, 225),(175, 238, 238),
            (255,218,233),(255,209,230),(255, 105, 180),(255, 192, 203)
        ]
        self.prefix_index = 0

    def add_gradient(self, text):
        colors = ['\033[38;5;159m', '\033[38;5;183m', '\033[38;5;219m', '\033[38;5;207m']
        result = []
        for i, char in enumerate(text):
            color = colors[i % len(colors)]
            result.append(f"{color}{char}")
        return ''.join(result) + self.reset

    def get_seal(self):
        self.seal_index += 1
        seal = self.frames[self.seal_index % len(self.frames)]
        return seal

    def gradient_text(self, text, start_color, end_color):
        result = []
        length = len(text)
        for i, char in enumerate(text):
            # Интерполяция между начальным и конечным цветом
            r = int(start_color[0] + (end_color[0] - start_color[0]) * (i / length))
            g = int(start_color[1] + (end_color[1] - start_color[1]) * (i / length))
            b = int(start_color[2] + (end_color[2] - start_color[2]) * (i / length))
            result.append(f"\033[38;2;{r};{g};{b}m{char}")
        return ''.join(result) + '\033[0m'

    def get_prefix_color(self):
        colors = []
        self.prefix_index += 1
        first_actual_index = self.prefix_index % len(self.prefix_colors)
        second_actual_index = (self.prefix_index + 1 ) % len(self.prefix_colors)
        colors.append(self.prefix_colors[first_actual_index])
        colors.append(self.prefix_colors[second_actual_index])
        return colors

    def format(self, record):
        try:
            time_str = datetime.datetime.now().strftime('%H:%M:%S')
            level_color = self.level_colors.get(record.levelname, '')
            seal = f'\n\033[38;2;0;127;255m{self.get_seal()}' \
                if random.randint(1,10) in (1,2) else ''
            prefix_color = self.get_prefix_color()
            final_prefix = self.gradient_text(f'[{self.logger_prefix}]', prefix_color[0], prefix_color[1])

            return (
                f"{final_prefix}{self.time_color}〘{time_str}〙➤{self.reset} "
                f"{level_color}{record.levelname[0]}: {record.msg}"
                f"{seal}{self.reset}"
            )
        except Exception as e:
            print(f'ошибка в логере: {e}')