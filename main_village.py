import pyautogui
import time
import cv2
import numpy as np
from PIL import ImageGrab
import keyboard


class ClashBot:
    def __init__(self):
        # ⚙️ Координати кнопок на емуляторі
        self.coords = {
            'attack': (369, 827),
            'find_match': (1247, 582),
            'return_home': (978, 798),
            'next': (1544, 720),
            'choice': (702, 829),
            # Позиції для розміщення різних військ
            'deploy_positions': {
                'ground_troops': [(1267, 171), (1387, 285), (1539, 395), (1570, 582), (1316, 255)],
                'spells': [(967, 267), (1123, 379), (1264, 493), (1389, 589), (1047, 460)],
                'heavy_troops': [(1188, 181)]
            }
        }

        # Клавіші для вибору військ (1, 2, 3, 4, 5, 6...)
        self.troop_keys = {
            'electro': '1',
            'king': 'r',
            'queen': 'e',
            'warder': 'w',
            'champion': 'q',
            'rage': 'a',
            'barracks': 'z'
        }

        # Стратегія атаки: тип війська + позиції
        self.attack_strategy = [
            {'troop': 'electro', 'key': '1', 'positions': 'ground_troops', 'clicks_per_position': 2},
            {'troop': 'king', 'key': 'r', 'positions': 'heavy_troops', 'clicks_per_position': 1},
            {'troop': 'queen', 'key': 'e', 'positions': 'heavy_troops', 'clicks_per_position': 1},
            {'troop': 'warder', 'key': 'w', 'positions': 'heavy_troops', 'clicks_per_position': 1},
            {'troop': 'champion', 'key': 'q', 'positions': 'heavy_troops', 'clicks_per_position': 1},
            {'troop': 'barracks', 'key': 'z', 'positions': 'heavy_troops', 'clicks_per_position': 1},
            {'troop': 'rage', 'key': 'a', 'positions': 'spells', 'clicks_per_position': 1}
        ]

    def click_button(self, position, delay=1):
        """Клік по координатам з затримкою"""
        pyautogui.click(position)
        time.sleep(delay)
        print(f"🖱️ Клік по координатам: {position}")

    def wait_for_template(self, template_path, threshold=0.8, timeout=60):
        """Очікування появи шаблону на екрані"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                screenshot = np.array(ImageGrab.grab())
                gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
                template = cv2.imread(template_path, 0)

                if template is None:
                    print(f"❌ Не вдалося завантажити шаблон: {template_path}")
                    return False

                result = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
                _, max_val, _, max_loc = cv2.minMaxLoc(result)

                if max_val >= threshold:
                    print(f"✅ Знайдено шаблон: {template_path}")
                    return True
            except Exception as e:
                print(f"❌ Помилка при пошуку шаблону: {e}")

            time.sleep(2)

        print(f"❌ Шаблон не знайдено за {timeout}с: {template_path}")
        return False

    def start_attack(self):
        """Початок атаки"""
        print("🟢 Початок атаки")
        self.click_button(self.coords['attack'], delay=1)

    def find_match(self):
        """Пошук противника"""
        print("🔍 Пошук противника")
        self.click_button(self.coords['find_match'], delay=2)

    def wait_for_battle_start(self):
        """Очікування початку битви"""
        print("🕵️ Очікуємо завантаження села...")
        self.wait_for_template("screenshots/next.jpg", timeout=60)

    def select_troop(self, troop_type=None, key=None):
        """Вибір типу війська за клавішею"""
        if key:
            # Вибір за клавішею
            print(f"⌨️ Вибір війська клавішею: {key}")
            keyboard.press_and_release(key)
            time.sleep(0.3)
            return True
        elif troop_type and troop_type in self.troop_keys:
            # Вибір за типом війська
            key_to_press = self.troop_keys[troop_type]
            print(f"⌨️ Вибір війська {troop_type} клавішею: {key_to_press}")
            keyboard.press_and_release(key_to_press)
            time.sleep(0.3)
            return True
        else:
            print(f"❌ Невідомий тип війська або клавіша: {troop_type}/{key}")
            return False

    def deploy_troops(self, positions_key, clicks_per_position=1):
        """Розміщення військ по заданим позиціям"""
        if positions_key in self.coords['deploy_positions']:
            positions = self.coords['deploy_positions'][positions_key]
            print(f"⚔️ Розміщення військ по позиціях: {positions_key}")

            for pos in positions:
                for _ in range(clicks_per_position):
                    pyautogui.click(pos)
                    time.sleep(0.3)  # Коротка пауза між кліками
                time.sleep(0.5)  # Пауза між позиціями
        else:
            print(f"❌ Невідомі позиції: {positions_key}")

    def execute_attack_strategy(self):
        """Виконання стратегії атаки"""
        print("⚔️ Початок розміщення армії за стратегією")

        for step in self.attack_strategy:
            troop_type = step['troop']
            key = step.get('key')  # Отримуємо клавішу, якщо вона є
            positions = step['positions']
            clicks = step['clicks_per_position']

            # Вибираємо тип війська (пріоритет клавіші)
            if self.select_troop(troop_type=troop_type, key=key):
                # Розміщуємо військо
                self.deploy_troops(positions, clicks)
                time.sleep(1)  # Пауза між різними типами військ
            else:
                print(f"⚠️ Пропускаємо {troop_type} - не вдалося вибрати")

    def wait_for_battle_end(self):
        """Очікування завершення битви"""
        print("🕓 Очікуємо завершення бою...")
        if self.wait_for_template("screenshots/return_home.jpg", timeout=180):
            print("✅ Битва завершена!")
            return True
        else:
            print("⚠️ Битва не завершилась вчасно")
            return False

    def return_home(self):
        """Повернення додому"""
        print("🏠 Повертаємося додому")
        self.click_button(self.coords['return_home'], delay=3)

    def wait_before_next_attack(self, delay=5):
        """Очікування перед наступною атакою"""
        print(f"🔁 Очікування {delay}с перед наступною атакою...")
        time.sleep(delay)

    def full_attack_cycle(self):
        """Повний цикл атаки"""
        try:
            # 1. Початок атаки
            self.start_attack()

            # 2. Пошук противника
            self.find_match()

            # 3. Очікування початку битви
            self.wait_for_battle_start()

            # 4. Виконання стратегії атаки
            self.execute_attack_strategy()

            # 5. Очікування завершення битви
            if self.wait_for_battle_end():
                # 6. Повернення додому
                self.return_home()
            else:
                print("⚠️ Примусове завершення битви")
                self.return_home()

            return True

        except Exception as e:
            print(f"❌ Помилка під час атаки: {e}")
            return False

    def run_bot(self, max_attacks=None):
        """Запуск бота з необмеженою кількістю атак"""
        attack_count = 0

        print("🤖 Запуск бота Clash of Clans")
        print(f"📋 Стратегія атаки: {len(self.attack_strategy)} типів військ")

        while True:
            try:
                attack_count += 1
                print(f"\n🔄 Атака #{attack_count}")

                # Виконуємо повний цикл атаки
                success = self.full_attack_cycle()

                if success:
                    print(f"✅ Атака #{attack_count} завершена успішно")
                else:
                    print(f"⚠️ Атака #{attack_count} завершена з помилками")

                # Перевіряємо чи досягли максимальної кількості атак
                if max_attacks and attack_count >= max_attacks:
                    print(f"🏁 Досягнуто максимальну кількість атак: {max_attacks}")
                    break

                # Очікування перед наступною атакою
                self.wait_before_next_attack(30)

            except KeyboardInterrupt:
                print("\n⏹️ Бот зупинено користувачем")
                break
            except Exception as e:
                print(f"❌ Критична помилка: {e}")
                print("🔄 Спроба продовжити через 10 секунд...")
                time.sleep(10)


# Використання бота
if __name__ == "__main__":
    time.sleep(5)
    # Створюємо екземпляр бота
    bot = ClashBot()

    # Можна налаштувати власну стратегію
    # bot.attack_strategy = [
    #     {'troop': 'dragon', 'key': '5', 'positions': 'heavy_troops', 'clicks_per_position': 1},
    #     {'troop': 'wizard', 'key': '4', 'positions': 'ranged_troops', 'clicks_per_position': 3}
    # ]

    # Або використовувати тільки клавіші без назв військ:
    # bot.attack_strategy = [
    #     {'troop': 'troop1', 'key': '1', 'positions': 'ground_troops', 'clicks_per_position': 3},
    #     {'troop': 'troop2', 'key': '2', 'positions': 'ranged_troops', 'clicks_per_position': 4}
    # ]

    # Запускаємо бота
    bot.run_bot()  # Нескінченний цикл
    # bot.run_bot(max_attacks=5)  # Обмежена кількість атак