import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementClickInterceptedException,
    ElementNotInteractableException,
    WebDriverException,
)
import logging
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime
import time

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("selenium_test.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 创建截图目录
screenshot_dir = "screenshots"
os.makedirs(screenshot_dir, exist_ok=True)

def take_screenshot(driver, name):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = os.path.join(screenshot_dir, f"{name}_{timestamp}.png")
    try:
        driver.save_screenshot(filepath)
        logger.info(f"截图已保存到: {filepath}")
    except Exception as e:
        logger.error(f"保存截图失败: {e}")

def click_element(driver, element):
    try:
        # 使用Actions类进行点击
        actions = ActionChains(driver)
        actions.move_to_element(element).click().perform()
        logger.info("使用Actions类成功点击元素")
    except Exception as e:
        logger.warning(f"使用Actions类点击元素失败: {e}")
        try:
            # 尝试使用JavaScript点击
            driver.execute_script("arguments[0].scrollIntoView(true);", element)
            driver.execute_script("arguments[0].click();", element)
            logger.info("使用JavaScript成功点击元素")
        except Exception as js_e:
            logger.error(f"使用JavaScript点击元素失败: {js_e}")
            raise

def main():
    # 配置Edge选项
    options = Options()
    # 如果需要无头模式，可以启用以下选项
    # options.add_argument('--headless')
    options.add_argument("--start-maximized")  # 最大化窗口以避免元素被遮挡

    username = "testuser"
    password = "testpassword"

    name = "test_name"
    amount = "100"

    # 初始化WebDriver
    try:
        driver = webdriver.Edge(options=options)
        logger.info("已启动Edge浏览器实例")
    except WebDriverException as e:
        logger.error(f"无法启动Edge WebDriver: {e}")
        return

    wait = WebDriverWait(driver, 20)  # 增加等待时间至20秒

    try:
        # 打开首页
        logger.info("打开首页: http://localhost:5173/")
        driver.get("http://localhost:5173/")
        take_screenshot(driver, "homepage_loaded")

        # 等待页面完全加载
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "container")))
        logger.info("页面容器已加载")
        
        # 尝试点击注册按钮
        logger.info("尝试点击注册按钮")

        # 使用更精确的XPath选择器
        register_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div/div[2]/button[2]'))
        )
        logger.info("找到注册按钮，尝试点击")
        click_element(driver, register_button)
        logger.info("已点击注册按钮")

        take_screenshot(driver, "after_click_register")

        # 填写注册表单
        logger.info("填写注册表单")
        try:
            username_input = driver.find_element(By.XPATH, '//*[@id="app"]/main/div/div/form/div[1]/div/div/div/div/input')
            password_input = driver.find_element(By.XPATH, '//*[@id="app"]/main/div/div/form/div[2]/div/div/div/div/input')

            username_input.send_keys(username)
            password_input.send_keys(password)

            logger.info("已填写用户名和密码")
        except (TimeoutException, NoSuchElementException) as e:
            logger.error(f"填写注册表单失败: {e}")
            take_screenshot(driver, "fill_register_form_failed")
            return

        # 提交注册表单
        logger.info("提交注册表单")
        try:
            # 根据前端代码，提交按钮的文本可能是“提交”，请确认实际文本
            submit_register = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/main/div/div/form/div[3]/div/div/div/div/button'))
            )
            submit_register.click()
            logger.info("已点击提交注册表单按钮")
        except (TimeoutException, NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException) as e:
            logger.error(f"提交注册表单失败: {e}")
            take_screenshot(driver, "submit_register_failed")
            return

        # 验证注册成功
        logger.info("验证注册是否成功")
        try:
            success_message = WebDriverWait(driver, 1).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".ant-message-success"))
            )
            print(success_message.text)
            assert "Register successful! Please login." in success_message.text
            logger.info("注册成功")
            take_screenshot(driver, "registration_success")
        except (TimeoutException, NoSuchElementException, AssertionError) as e:
            logger.error(f"注册验证失败: {e}")
            take_screenshot(driver, "registration_verification_failed")
            return
        
        time.sleep(3)  # 等待3秒，确保页面完全加载

        # 填写登录表单
        logger.info("填写登录表单")
        try:
            username_input = driver.find_element(By.XPATH, '//*[@id="app"]/main/div/div/form/div[1]/div/div/div/div/input')
            password_input = driver.find_element(By.XPATH, '//*[@id="app"]/main/div/div/form/div[2]/div/div/div/div/input')

            username_input.send_keys(username)
            password_input.send_keys(password)
            logger.info("已填写登录用户名和密码")
        except (TimeoutException, NoSuchElementException) as e:
            logger.error(f"填写登录表单失败: {e}")
            take_screenshot(driver, "fill_login_form_failed")
            return

        # 提交登录表单
        logger.info("提交登录表单")
        try:
            # 根据前端代码，提交按钮的文本可能是“提交”，请确认实际文本
            submit_login = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/main/div/div/form/div[3]/div/div/div/div/button'))
            )
            submit_login.click()
            logger.info("已点击提交登录表单按钮")
        except (TimeoutException, NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException) as e:
            logger.error(f"提交登录表单失败: {e}")
            take_screenshot(driver, "submit_login_failed")
            return

        # 验证登录成功
        logger.info("验证登录是否成功")
        try:
            success_message = WebDriverWait(driver, 1).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".ant-message-success"))
            )
            print(success_message.text)
            assert "Login successful!" in success_message.text
            logger.info("登录成功")
            take_screenshot(driver, "login_success")
        except (TimeoutException, NoSuchElementException, AssertionError) as e:
            logger.error(f"登录验证失败: {e}")
            take_screenshot(driver, "login_verification_failed")
            return

        
        
        # 等待页面加载完成
        time.sleep(3)

        # 尝试打开客服
        logger.info("尝试点击客服按钮")

        # 使用更精确的XPath选择器
        customer_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/section/aside/div[1]/ul/li[2]'))
        )
        logger.info("找到客服按钮，尝试点击")
        click_element(driver, customer_button)
        logger.info("已点击客服按钮")

        take_screenshot(driver, "after_click_customer")

        # 等待页面加载完成
        time.sleep(3)

        # 检验客服输出1

        logger.info("检查客服输出1")
        try:
            output = WebDriverWait(driver, 1).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/section/section/main/div/div/div/div[2]/div[1]/div[1]/div/div/div[2]/div[2]/div/p'))
            )
            print(output.text)
            assert f"{username}您好，请问有什么可以帮您?" in output.text
            logger.info("客服输出正确")
            take_screenshot(driver, "customer_service_correct")
        except (TimeoutException, NoSuchElementException, AssertionError) as e:
            logger.error(f"客服输出错误: {e}")
            take_screenshot(driver, "customer_service_incorrect")
            return

        # 等待用户沉默
        time.sleep(10)

        # 检验客服输出2

        logger.info("检查客服输出2")
        try:
            output = WebDriverWait(driver, 1).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/section/section/main/div/div/div/div[2]/div[1]/div[2]/div/div/div[2]/div[2]/div/p'))
            )
            print(output.text)
            assert "听不清，请您大声一点可以吗" in output.text
            logger.info("客服输出正确")
            take_screenshot(driver, "customer_service_correct")
        except (TimeoutException, NoSuchElementException, AssertionError) as e:
            logger.error(f"客服输出错误: {e}")
            take_screenshot(driver, "customer_service_incorrect")
            return
        
        # 等待用户输入
        time.sleep(3)

        # 输入文本
        logger.info("输入文本")
        try:
            text = "投诉"

            text_input = driver.find_element(By.XPATH, '//*[@id="app"]/section/section/main/div/div/div/div[2]/div[2]/textarea')

            text_input.send_keys(text)
            logger.info("已填写文本投诉")
        except (TimeoutException, NoSuchElementException) as e:
            logger.error(f"填写文本投诉失败: {e}")
            take_screenshot(driver, "fill_text_failed")
            return
        
        # 提交文本投诉
        logger.info("提交文本投诉")
        try:
            submit_text = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/section/section/main/div/div/div/div[2]/div[2]/button'))
            )
            submit_text.click()
            logger.info("已点击提交文本投诉按钮")
        except (TimeoutException, NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException) as e:
            logger.error(f"提交文本投诉失败: {e}")
            take_screenshot(driver, "submit_text_failed")
            return
        
        # 验证文本投诉提交成功
        logger.info("验证是否提交文本投诉成功")
        try:
            output = WebDriverWait(driver, 1).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/section/section/main/div/div/div/div[2]/div[1]/div[3]/div/div/div[2]/div[2]/div/p'))
            )
            print(output.text)
            assert "投诉" in output.text
            logger.info("提交文本投诉成功")
            take_screenshot(driver, "submit_text_success")
        except (TimeoutException, NoSuchElementException, AssertionError) as e:
            logger.error(f"提交文本投诉验证失败: {e}")
            take_screenshot(driver, "submit_text_verification_failed")
            return
        
        # 等待页面加载完成
        time.sleep(3)

        # 检查客服输出3
        logger.info("检查客服输出3")
        try:
            output = WebDriverWait(driver, 1).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/section/section/main/div/div/div/div[2]/div[1]/div[4]/div/div/div[2]/div[2]/div/p'))
            )
            print(output.text)
            assert "您的意见是我们改进工作的动力，请问您还有什么补充?" in output.text
            logger.info("客服输出正确")
            take_screenshot(driver, "customer_service_correct")
        except (TimeoutException, NoSuchElementException, AssertionError) as e:
            logger.error(f"客服输出错误: {e}")
            take_screenshot(driver, "customer_service_incorrect")
            return
        
        # 等待用户输入
        time.sleep(3)

        # 输入文本
        logger.info("输入文本")
        try:
            text = "账单"

            text_input = driver.find_element(By.XPATH, '//*[@id="app"]/section/section/main/div/div/div/div[2]/div[2]/textarea')

            text_input.send_keys(text)
            logger.info("已填写文本账单")
        except (TimeoutException, NoSuchElementException) as e:
            logger.error(f"填写文本账单失败: {e}")
            take_screenshot(driver, "fill_text_failed")
            return
        
        # 提交文本账单
        logger.info("提交文本账单")
        try:
            submit_text = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/section/section/main/div/div/div/div[2]/div[2]/button'))
            )
            submit_text.click()
            logger.info("已点击提交文本账单按钮")
        except (TimeoutException, NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException) as e:
            logger.error(f"提交文本账单失败: {e}")
            take_screenshot(driver, "submit_text_failed")
            return
        
        # 验证文本账单提交成功
        logger.info("验证是否提交文本账单成功")
        try:
            output = WebDriverWait(driver, 1).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/section/section/main/div/div/div/div[2]/div[1]/div[5]/div/div/div[2]/div[2]/div/p'))
            )
            print(output.text)
            assert "账单" in output.text
            logger.info("提交文本账单成功")
            take_screenshot(driver, "submit_text_success")
        except (TimeoutException, NoSuchElementException, AssertionError) as e:
            logger.error(f"提交文本账单验证失败: {e}")
            take_screenshot(driver, "submit_text_verification_failed")
            return

        # 等待页面加载完成
        time.sleep(3)

        # 检查客服输出4
        logger.info("检查客服输出4")
        try:
            output = WebDriverWait(driver, 1).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/section/section/main/div/div/div/div[2]/div[1]/div[6]/div/div/div[2]/div[2]/div/p'))
            )
            print(output.text)
            assert "感谢您的来电，再见" in output.text
            logger.info("客服输出正确")
            take_screenshot(driver, "customer_service_correct")
        except (TimeoutException, NoSuchElementException, AssertionError) as e:
            logger.error(f"客服输出错误: {e}")
            take_screenshot(driver, "customer_service_incorrect")
            return
        
        # 测试全部正确
        logger.info("客服测试1 正确")
        take_screenshot(driver, "all_correct")

    except Exception as e:
        logger.error(f"发生未预料的错误: {e}")
        take_screenshot(driver, "unexpected_error")
    finally:
        logger.info("关闭浏览器")
        driver.quit()


    try:
        driver = webdriver.Edge(options=options)
        logger.info("已启动Edge浏览器实例")
    except WebDriverException as e:
        logger.error(f"无法启动Edge WebDriver: {e}")
        return

    wait = WebDriverWait(driver, 20)  # 增加等待时间至20秒

    try:
        # 打开首页
        logger.info("打开首页: http://localhost:5173/")
        driver.get("http://localhost:5173/")
        take_screenshot(driver, "homepage_loaded")

        # 等待页面完全加载
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "container")))
        logger.info("页面容器已加载")

        # 找到并点击登录按钮
        logger.info("尝试点击登录按钮")
        try:
            login_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div/div[2]/button[1]'))
            )
            click_element(driver, login_button)
            logger.info("已点击登录按钮")
        except (TimeoutException, NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException) as e:
            logger.error(f"点击登录按钮失败: {e}")
            take_screenshot(driver, "click_login_failed")
            return

        take_screenshot(driver, "after_click_login")

        # 填写登录表单
        logger.info("填写登录表单")
        try:
            username_input = driver.find_element(By.XPATH, '//*[@id="app"]/main/div/div/form/div[1]/div/div/div/div/input')
            password_input = driver.find_element(By.XPATH, '//*[@id="app"]/main/div/div/form/div[2]/div/div/div/div/input')

            username_input.send_keys(username)
            password_input.send_keys(password)
            logger.info("已填写登录用户名和密码")
        except (TimeoutException, NoSuchElementException) as e:
            logger.error(f"填写登录表单失败: {e}")
            take_screenshot(driver, "fill_login_form_failed")
            return

        # 提交登录表单
        logger.info("提交登录表单")
        try:
            # 根据前端代码，提交按钮的文本可能是“提交”，请确认实际文本
            submit_login = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/main/div/div/form/div[3]/div/div/div/div/button'))
            )
            submit_login.click()
            logger.info("已点击提交登录表单按钮")
        except (TimeoutException, NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException) as e:
            logger.error(f"提交登录表单失败: {e}")
            take_screenshot(driver, "submit_login_failed")
            return

        # 验证登录成功
        logger.info("验证登录是否成功")
        try:
            success_message = WebDriverWait(driver, 1).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".ant-message-success"))
            )
            print(success_message.text)
            assert "Login successful!" in success_message.text
            logger.info("登录成功")
            take_screenshot(driver, "login_success")
        except (TimeoutException, NoSuchElementException, AssertionError) as e:
            logger.error(f"登录验证失败: {e}")
            take_screenshot(driver, "login_verification_failed")
            return
        
        # 等待页面加载完成
        time.sleep(3)
        
        # 尝试打开信息设置
        logger.info("尝试点击信息设置按钮")

        # 使用更精确的XPath选择器
        info_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/section/aside/div[1]/ul/li[1]'))
        )
        logger.info("找到信息设置按钮，尝试点击")
        click_element(driver, info_button)
        logger.info("已点击信息设置按钮")

        take_screenshot(driver, "after_click_info")

        # 填写信息表单
        logger.info("填写信息表单")
        try:

            name_input = driver.find_element(By.XPATH, '//*[@id="app"]/section/section/main/div/form/div[2]/div/div[2]/div/div/input')
            amount_input = driver.find_element(By.XPATH, '//*[@id="app"]/section/section/main/div/form/div[3]/div/div[2]/div/div/input')

            name_input.send_keys(name)
            amount_input.send_keys(amount)
            logger.info("已填写信息表单")
        except (TimeoutException, NoSuchElementException) as e:
            logger.error(f"填写信息表单失败: {e}")
            take_screenshot(driver, "fill_info_form_failed")
            return

        # 提交信息表单
        logger.info("提交信息表单")
        try:
            submit_login = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/section/section/main/div/form/div[4]/div/div/div/div/button'))
            )
            submit_login.click()
            logger.info("已点击提交信息表单按钮")
        except (TimeoutException, NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException) as e:
            logger.error(f"提交信息表单失败: {e}")
            take_screenshot(driver, "submit_info_failed")
            return

        # 验证信息表单提交成功
        logger.info("验证是否提交信息表单成功")
        try:
            success_message = WebDriverWait(driver, 1).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".ant-message-success"))
            )
            print(success_message.text)
            assert "Set Infomation successful!" in success_message.text
            logger.info("提交信息表单成功")
            take_screenshot(driver, "info_commit_success")
        except (TimeoutException, NoSuchElementException, AssertionError) as e:
            logger.error(f"提交信息验证失败: {e}")
            take_screenshot(driver, "info_commit_verification_failed")
            return
        
        # 等待页面加载完成
        time.sleep(3)

        # 尝试打开客服
        logger.info("尝试点击客服按钮")

        # 使用更精确的XPath选择器
        customer_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/section/aside/div[1]/ul/li[2]'))
        )
        logger.info("找到客服按钮，尝试点击")
        click_element(driver, customer_button)
        logger.info("已点击客服按钮")

        take_screenshot(driver, "after_click_customer")

        # 等待页面加载完成
        time.sleep(3)

        # 检验客服输出1

        logger.info("检查客服输出1")
        try:
            output = WebDriverWait(driver, 1).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/section/section/main/div/div/div/div[2]/div[1]/div[1]/div/div/div[2]/div[2]/div/p'))
            )
            print(output.text)
            assert f"{name}您好，请问有什么可以帮您?" in output.text
            logger.info("客服输出正确")
            take_screenshot(driver, "customer_service_correct")
        except (TimeoutException, NoSuchElementException, AssertionError) as e:
            logger.error(f"客服输出错误: {e}")
            take_screenshot(driver, "customer_service_incorrect")
            return
        
        # 等待用户输入
        time.sleep(3)

        text = "账单"
        # 输入文本
        logger.info("输入文本")
        try:
            text = "账单"

            text_input = driver.find_element(By.XPATH, '//*[@id="app"]/section/section/main/div/div/div/div[2]/div[2]/textarea')

            text_input.send_keys(text)
            logger.info("已填写文本账单")
        except (TimeoutException, NoSuchElementException) as e:
            logger.error(f"填写文本账单失败: {e}")
            take_screenshot(driver, "fill_text_failed")
            return
        
        # 提交文本账单
        logger.info("提交文本账单")
        try:
            submit_text = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/section/section/main/div/div/div/div[2]/div[2]/button'))
            )
            submit_text.click()
            logger.info("已点击提交文本账单按钮")
        except (TimeoutException, NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException) as e:
            logger.error(f"提交文本账单失败: {e}")
            take_screenshot(driver, "submit_text_failed")
            return
        
        # 验证文本账单提交成功
        logger.info("验证是否提交文本账单成功")
        try:
            output = WebDriverWait(driver, 1).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/section/section/main/div/div/div/div[2]/div[1]/div[2]/div/div/div[2]/div[2]/div/p'))
            )
            print(output.text)
            assert "账单" in output.text
            logger.info("提交文本账单成功")
            take_screenshot(driver, "submit_text_success")
        except (TimeoutException, NoSuchElementException, AssertionError) as e:
            logger.error(f"提交文本账单验证失败: {e}")
            take_screenshot(driver, "submit_text_verification_failed")
            return
        
        # 等待页面加载完成
        time.sleep(3)
        
        # 检查客服输出2
        logger.info("检查客服输出2")
        try:
            output = WebDriverWait(driver, 1).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/section/section/main/div/div/div/div[2]/div[1]/div[3]/div/div/div[2]/div[2]/div/p'))
            )
            print(output.text)
            assert f"您的本月账单是{amount}元，感谢您的来电，再见" in output.text
            logger.info("客服输出正确")
            take_screenshot(driver, "customer_service_correct")
        except (TimeoutException, NoSuchElementException, AssertionError) as e:
            logger.error(f"客服输出错误: {e}")
            take_screenshot(driver, "customer_service_incorrect")
            return
        
        # 测试2全部正确
        logger.info("客服测试2 正确")
        take_screenshot(driver, "all_correct")

        # 测试全部正确
        logger.info("客服测试全部正确")
        take_screenshot(driver, "all_correct")
        
    except Exception as e:
        logger.error(f"发生未预料的错误: {e}")
        take_screenshot(driver, "unexpected_error")
    finally:
        logger.info("关闭浏览器")
        driver.quit()

if __name__ == "__main__":
    main()
