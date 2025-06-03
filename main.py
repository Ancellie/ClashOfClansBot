import pyautogui
import time
import cv2
import numpy as np
from PIL import ImageGrab

def click_button(position, delay=1):
    pyautogui.click(position)
    time.sleep(delay)

def wait_for_template(template_path, threshold=0.8, timeout=60):
    start_time = time.time()
    while time.time() - start_time < timeout:
        screenshot = np.array(ImageGrab.grab())
        gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
        template = cv2.imread(template_path, 0)
        result = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)
        if max_val >= threshold:
            print(f"✅ Знайдено шаблон: {template_path}")
            return True
        time.sleep(2)
    print(f"❌ Шаблон не знайдено: {template_path}")
    return False

# ⚙️ Координати кнопок на емуляторі — потрібно оновити!
coords = {
    'attack': (547, 820),
    'find_match': (1441, 557),
    'return_home': (1141, 791),
    'next': (1708, 720),
    'choice': (702, 829),
    'deploy_army': [(1252, 180), (1354, 265), (1447, 326), (1597, 430), (1597, 430)], # куди клікати для армії
    'select_troop': (683, 831)
}

while True:
    time.sleep(5)
    print("🟢 Початок циклу атаки")

    # 1. Натиснути "Attack!"
    click_button(coords['attack'], delay=1)

    # 2. Натиснути "Find a Match"
    click_button(coords['find_match'], delay=2)

    # 3. Очікувати завантаження села (можна замінити на шаблон будівлі)
    print("🕵️ Очікуємо село...")
    time.sleep(5)

    # 4. Вибрати тип війська
    print("🧙‍♂️ Вибір війська")
    click_button(coords['select_troop'], delay=1)

    # 5. Розмістити армію
    print("⚔️ Розміщення армії")
    for pos in coords['deploy_army']:
        pyautogui.click(pos)
        pyautogui.click(pos)
        time.sleep(1)

    # 6. Очікувати завершення атаки (пошук шаблону кнопки "Return Home")
    print("🕓 Очікуємо завершення бою")
    if wait_for_template("screenshots/return_home.jpg", timeout=120):
        click_button(coords['return_home'], delay=3)

    # 7. Очікування перед наступною атакою
    print("🔁 Очікування перед наступною атакою...")
    time.sleep(30)
