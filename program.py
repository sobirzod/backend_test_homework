class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self, training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.training_type = training_type
        self.distance = distance
        self.speed = speed
        self.calories = calories
        self.duration = duration

    def get_message(self) -> str:
        TYPE_TRAINING = 'Тип тренировки:'
        DURATION = 'Длительность:'
        DISTANCE = 'Дистанция:'
        SPEED = 'Ср. скорость:'
        CALORIES = 'Потрачено ккал:'
        text_for_output = "{} {}; {} {} ч.; {} {} км; {} {} км/ч; {} {}."
        return text_for_output.format(
            TYPE_TRAINING,
            self.training_type,
            DURATION,
            format(self.duration, '.3f'),
            DISTANCE,
            format(self.distance, '.3f'),
            SPEED,
            format(self.speed, '.3f'),
            CALORIES,
            format(self.calories, '.3f'))


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: float = 1000
    HOUR_TO_MIN: float = 60

    def __init__(self, action: float,
                 duration: float,
                 weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed = self.get_distance() / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError()

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info_message = InfoMessage(self.__class__.__name__,
                                   self.duration,
                                   self.get_distance(),
                                   self.get_mean_speed(),
                                   self.get_spent_calories())
        return info_message


class Running(Training):
    """Тренировка: бег."""
    ratio_Run_1: float = 18
    ratio_Run_2: float = 20

    def get_spent_calories(self) -> float:
        calories_1 = self.ratio_Run_1 * self.get_mean_speed()
        calories = ((calories_1 - self.ratio_Run_2) * self.weight
                    / self.M_IN_KM * self.duration * self.HOUR_TO_MIN)
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    ratio_SpW_1: float = 0.035
    ratio_SpW_2: float = 0.029
    ratio_SpW_3 = 2

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 height: int) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        operat_1 = self.ratio_SpW_1 * self.weight
        operat_2 = self.get_mean_speed()**self.ratio_SpW_3 // self.height
        operat_3 = operat_2 * self.ratio_SpW_2 * self.weight
        calories = (operat_1 + operat_3) * self.duration * self.HOUR_TO_MIN
        return calories


class Swimming(Training):
    """Тренировка: плавание."""
    koeff_SW_1: float = 1.1
    koeff_SW_2: float = 2
    LEN_STEP: float = 1.38

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.lenght_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Средняя скорость."""
        self.speed = (self.lenght_pool * self.count_pool
                      / super().M_IN_KM / self.duration)
        return self.speed

    def get_spent_calories(self) -> float:
        operation_1 = self.get_mean_speed() + self.koeff_SW_1
        calories = operation_1 * self.koeff_SW_2 * self.weight
        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    type_dict = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    if workout_type in type_dict.keys():
        workout = type_dict[workout_type](*data)
        return workout
    else:
        print('Нет такой тренировки!!!')


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [1500, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
