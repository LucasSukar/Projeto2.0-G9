from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import time
driver = webdriver.Chrome()


class AdicionarCafeteria(LiveServerTestCase):


    def test_1(self):
        #Fazendo registro do usuário

        driver.get("http://127.0.0.1:8000/mainapp/cadastro/")
        usuario = driver.find_element(by=By.NAME, value="username")
        email = driver.find_element(by=By.NAME, value="email")
        senha = driver.find_element(by=By.NAME, value="password")
        botao = driver.find_element(by=By.XPATH, value="/html/body/section/div/div/div/div/div/form/button")

        usuario.send_keys(f"user1")
        email.send_keys(f"user1@gmail.com")
        senha.send_keys("Senha1234")
        time.sleep(2)
        botao.send_keys(Keys.ENTER)
        time.sleep(2)

        usuariologin = driver.find_element(by=By.NAME, value="username")
        senhalogin = driver.find_element(by=By.NAME, value="password")
        botaologin = driver.find_element(by=By.XPATH, value="/html/body/section/div/div/div/div/div[2]/form/div[3]/button")

        usuariologin.send_keys(f"user1")
        senhalogin.send_keys("Senha1234")
        time.sleep(2)
        botaologin.send_keys(Keys.ENTER)
        time.sleep(2)

        #Direcionando para a página de adicionar cafeterias

        botaocafeterias = driver.find_element(by=By.XPATH, value="/html/body/div/ul/li[3]/a")
        botaocafeterias.send_keys(Keys.ENTER)
        time.sleep(2)
        botaoadd = driver.find_element(by=By.XPATH, value="/html/body/section/div[2]/a")
        botaoadd.send_keys(Keys.ENTER)
        time.sleep(2)

        #Adicionando uma cafeteria

        nome = driver.find_element(by=By.NAME, value="nome")
        autor = driver.find_element(by=By.NAME, value="autor")
        anopublicado = driver.find_element(by=By.NAME, value="anopublicado")
        genero = driver.find_element(by=By.NAME, value="genero")
        botaosave = driver.find_element(by=By.XPATH, value="/html/body/section/div/form/button")

        nome.send_keys(f"Starbucks")
        autor.send_keys(f"Avenida do Café, 321")
        anopublicado.send_keys("81999999999")
        chooser = Select(genero)
        chooser.select_by_visible_text("expresso")
        time.sleep(2)
        botaosave.send_keys(Keys.ENTER)
        time.sleep(2)
        self.assertEqual(driver.find_element(by=By.XPATH, value="/html/body/section/div[2]/div/a/div/div[1]").text, "Starbucks por Avenida do Café, 321 (81999999999)")
        botaologout = driver.find_element(by=By.XPATH, value="/html/body/div/ul/li[6]/a")
        botaologout.send_keys(Keys.ENTER)
        time.sleep(3)


    def test_2(self):
        #Fazendo login do usuário

        driver.get("http://127.0.0.1:8000/mainapp/login/")
        usuariologin = driver.find_element(by=By.NAME, value="username")
        senhalogin = driver.find_element(by=By.NAME, value="password")
        botaologin = driver.find_element(by=By.XPATH, value="/html/body/section/div/div/div/div/div[2]/form/div[3]/button")

        usuariologin.send_keys(f"user1")
        senhalogin.send_keys("Senha1234")
        time.sleep(2)
        botaologin.send_keys(Keys.ENTER)
        time.sleep(2)

        #Direcionando para a página de adicionar cafeterias

        botaocafeterias = driver.find_element(by=By.XPATH, value="/html/body/div/ul/li[3]/a")
        botaocafeterias.send_keys(Keys.ENTER)
        time.sleep(2)
        botaoadd = driver.find_element(by=By.XPATH, value="/html/body/section/div[2]/a")
        botaoadd.send_keys(Keys.ENTER)
        time.sleep(2)

        #Adicionando uma cafeteria já registrada

        nome = driver.find_element(by=By.NAME, value="nome")
        autor = driver.find_element(by=By.NAME, value="autor")
        anopublicado = driver.find_element(by=By.NAME, value="anopublicado")
        genero = driver.find_element(by=By.NAME, value="genero")
        botaosave = driver.find_element(by=By.XPATH, value="/html/body/section/div/form/button")

        nome.send_keys(f"Starbucks")
        autor.send_keys(f"Avenida do Café, 321")
        anopublicado.send_keys("81999999999")
        chooser = Select(genero)
        chooser.select_by_visible_text("expresso")
        time.sleep(2)
        botaosave.send_keys(Keys.ENTER)
        time.sleep(2)

        #Alterando as informações para adicionar uma cafeteria não registrada

        nome = driver.find_element(by=By.NAME, value="nome")
        autor = driver.find_element(by=By.NAME, value="autor")
        anopublicado = driver.find_element(by=By.NAME, value="anopublicado")
        genero = driver.find_element(by=By.NAME, value="genero")
        botaosave = driver.find_element(by=By.XPATH, value="/html/body/section/div/form/button")

        nome.send_keys(f"Delta Expresso")
        autor.send_keys(f"Avenida do Café, 456")
        anopublicado.send_keys("81999999998")
        chooser = Select(genero)
        chooser.select_by_visible_text("cappuccino")
        time.sleep(2)
        botaosave.send_keys(Keys.ENTER)
        time.sleep(2)
        self.assertEqual(driver.find_element(by=By.XPATH, value="/html/body/section/div[2]/div/a[2]/div/div[1]").text, "Delta Expresso por Avenida do Café, 456 (81999999998)")
        botaologout = driver.find_element(by=By.XPATH, value="/html/body/div/ul/li[6]/a")
        botaologout.send_keys(Keys.ENTER)
        time.sleep(3)