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
        endereco = driver.find_element(by=By.NAME, value="endereco")
        cntt = driver.find_element(by=By.NAME, value="cntt")
        tipo = driver.find_element(by=By.NAME, value="tipo")
        botaosave = driver.find_element(by=By.XPATH, value="/html/body/section/div/form/button")

        nome.send_keys(f"Starbucks")
        endereco.send_keys(f"Avenida do Café, 321")
        cntt.send_keys("81999999999")
        chooser = Select(tipo)
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
        endereco = driver.find_element(by=By.NAME, value="endereco")
        cntt = driver.find_element(by=By.NAME, value="cntt")
        tipo = driver.find_element(by=By.NAME, value="tipo")
        botaosave = driver.find_element(by=By.XPATH, value="/html/body/section/div/form/button")

        nome.send_keys(f"Starbucks")
        endereco.send_keys(f"Avenida do Café, 321")
        cntt.send_keys("81999999999")
        chooser = Select(tipo)
        chooser.select_by_visible_text("expresso")
        time.sleep(2)
        botaosave.send_keys(Keys.ENTER)
        time.sleep(2)

        #Alterando as informações para adicionar uma cafeteria não registrada

        nome = driver.find_element(by=By.NAME, value="nome")
        endereco = driver.find_element(by=By.NAME, value="endereco")
        cntt = driver.find_element(by=By.NAME, value="cntt")
        tipo = driver.find_element(by=By.NAME, value="tipo")
        botaosave = driver.find_element(by=By.XPATH, value="/html/body/section/div/form/button")

        nome.send_keys(f"Delta Expresso")
        endereco.send_keys(f"Avenida do Café, 456")
        cntt.send_keys("81999999998")
        chooser = Select(tipo)
        chooser.select_by_visible_text("cappuccino")
        time.sleep(2)
        botaosave.send_keys(Keys.ENTER)
        time.sleep(2)
        self.assertEqual(driver.find_element(by=By.XPATH, value="/html/body/section/div[2]/div/a[2]/div/div[1]").text, "Delta Expresso por Avenida do Café, 456 (81999999998)")
        botaologout = driver.find_element(by=By.XPATH, value="/html/body/div/ul/li[6]/a")
        botaologout.send_keys(Keys.ENTER)
        time.sleep(3)

class RemoverCafeteria(LiveServerTestCase):

    def test_1(self):
        #Fazendo registro do usuário

        driver.get("http://127.0.0.1:8000/mainapp/cadastro/")
        usuario = driver.find_element(by=By.NAME, value="username")
        email = driver.find_element(by=By.NAME, value="email")
        senha = driver.find_element(by=By.NAME, value="password")
        botao = driver.find_element(by=By.XPATH, value="/html/body/section/div/div/div/div/div/form/button")

        usuario.send_keys(f"user2")
        email.send_keys(f"user2@gmail.com")
        senha.send_keys("Senha1234")
        time.sleep(2)
        botao.send_keys(Keys.ENTER)
        time.sleep(2)

        usuariologin = driver.find_element(by=By.NAME, value="username")
        senhalogin = driver.find_element(by=By.NAME, value="password")
        botaologin = driver.find_element(by=By.XPATH, value="/html/body/section/div/div/div/div/div[2]/form/div[3]/button")

        usuariologin.send_keys(f"user2")
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
        endereco = driver.find_element(by=By.NAME, value="endereco")
        cntt = driver.find_element(by=By.NAME, value="cntt")
        tipo = driver.find_element(by=By.NAME, value="tipo")
        botaosave = driver.find_element(by=By.XPATH, value="/html/body/section/div/form/button")

        nome.send_keys(f"São Braz")
        endereco.send_keys(f"Rua José Braz, 333")
        cntt.send_keys("81999999993")
        chooser = Select(tipo)
        chooser.select_by_visible_text("macchiato")
        time.sleep(2)
        botaosave.send_keys(Keys.ENTER)
        time.sleep(2)

        #Removendo a cafeteria

        botaoacesso = driver.find_element(by=By.XPATH, value="/html/body/section/div[2]/div/a")
        botaoacesso.send_keys(Keys.ENTER)
        time.sleep(2)
        botaodel = driver.find_element(by=By.XPATH, value="/html/body/section/div[1]/div/div[2]/div/button")
        botaodel.send_keys(Keys.ENTER)
        time.sleep(2)
        botaodel2 = driver.find_element(by=By.XPATH, value="/html/body/section/div[2]/div/div/div[3]/form/button")
        botaodel2.send_keys(Keys.ENTER)
        time.sleep(3)
        self.assertEqual(driver.find_element(by=By.XPATH, value="/html/body/section/div[2]/div/p").text, ("Nenhuma cafeterias adicionada ainda."))
        botaologout = driver.find_element(by=By.XPATH, value="/html/body/div/ul/li[6]/a")
        botaologout.send_keys(Keys.ENTER)
        time.sleep(2)

class FavoritarCafeteria(LiveServerTestCase):

    def test_1(self):
        #Fazendo registro do usuário

        driver.get("http://127.0.0.1:8000/mainapp/cadastro/")
        usuario = driver.find_element(by=By.NAME, value="username")
        email = driver.find_element(by=By.NAME, value="email")
        senha = driver.find_element(by=By.NAME, value="password")
        botao = driver.find_element(by=By.XPATH, value="/html/body/section/div/div/div/div/div/form/button")

        usuario.send_keys(f"user3")
        email.send_keys(f"user3@gmail.com")
        senha.send_keys("Senha1234")
        time.sleep(2)
        botao.send_keys(Keys.ENTER)
        time.sleep(2)

        usuariologin = driver.find_element(by=By.NAME, value="username")
        senhalogin = driver.find_element(by=By.NAME, value="password")
        botaologin = driver.find_element(by=By.XPATH, value="/html/body/section/div/div/div/div/div[2]/form/div[3]/button")

        usuariologin.send_keys(f"user3")
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
        endereco = driver.find_element(by=By.NAME, value="endereco")
        cntt = driver.find_element(by=By.NAME, value="cntt")
        tipo = driver.find_element(by=By.NAME, value="tipo")
        botaosave = driver.find_element(by=By.XPATH, value="/html/body/section/div/form/button")

        nome.send_keys(f"Santa Clara")
        endereco.send_keys(f"Rua Café Preto, 101")
        cntt.send_keys("81999999101")
        chooser = Select(tipo)
        chooser.select_by_visible_text("Grão específico")
        time.sleep(2)
        botaosave.send_keys(Keys.ENTER)
        time.sleep(2)

        #Adicionando a cafeteria aos favoritos

        botaoacesso = driver.find_element(by=By.XPATH, value="/html/body/section/div[2]/div/a")
        botaoacesso.send_keys(Keys.ENTER)
        time.sleep(2)
        botaoeditar = driver.find_element(by=By.XPATH, value="/html/body/section/div[1]/div/div[2]/div/a[2]")
        botaoeditar.send_keys(Keys.ENTER)
        time.sleep(1)
        status = driver.find_element(by=By.NAME, value="status_cafeteria")
        chooser = Select(status)
        chooser.select_by_visible_text("Favorita")
        time.sleep(2)
        botaosubmit = driver.find_element(by=By.XPATH, value="/html/body/section/div/form/button")
        botaosubmit.send_keys(Keys.ENTER)
        time.sleep(3)
        self.assertEqual(driver.find_element(by=By.XPATH, value="/html/body/section/div[2]/div/a/div/div[2]").text, ("Status da cafeteria: Favorita"))
        botaologout = driver.find_element(by=By.XPATH, value="/html/body/div/ul/li[6]/a")
        botaologout.send_keys(Keys.ENTER)
        time.sleep(2)

class RemoverFavorito(LiveServerTestCase):

    def test_1(self):
        #Fazendo registro do usuário

        driver.get("http://127.0.0.1:8000/mainapp/cadastro/")
        usuario = driver.find_element(by=By.NAME, value="username")
        email = driver.find_element(by=By.NAME, value="email")
        senha = driver.find_element(by=By.NAME, value="password")
        botao = driver.find_element(by=By.XPATH, value="/html/body/section/div/div/div/div/div/form/button")

        usuario.send_keys(f"user4")
        email.send_keys(f"user4@gmail.com")
        senha.send_keys("Senha1234")
        time.sleep(2)
        botao.send_keys(Keys.ENTER)
        time.sleep(2)

        usuariologin = driver.find_element(by=By.NAME, value="username")
        senhalogin = driver.find_element(by=By.NAME, value="password")
        botaologin = driver.find_element(by=By.XPATH, value="/html/body/section/div/div/div/div/div[2]/form/div[3]/button")

        usuariologin.send_keys(f"user4")
        senhalogin.send_keys("Senha1234")
        time.sleep(2)
        botaologin.send_keys(Keys.ENTER)
        time.sleep(2)

        #Direcionando para a página de adicionar cafeterias

        botaocafeterias = driver.find_element(by=By.XPATH, value="/html/body/div/ul/li[3]/a")
        botaocafeterias.send_keys(Keys.ENTER)
        time.sleep(1)
        botaoadd = driver.find_element(by=By.XPATH, value="/html/body/section/div[2]/a")
        botaoadd.send_keys(Keys.ENTER)
        time.sleep(1)

        #Adicionando uma cafeteria

        nome = driver.find_element(by=By.NAME, value="nome")
        endereco = driver.find_element(by=By.NAME, value="endereco")
        cntt = driver.find_element(by=By.NAME, value="cntt")
        tipo = driver.find_element(by=By.NAME, value="tipo")
        botaosave = driver.find_element(by=By.XPATH, value="/html/body/section/div/form/button")

        nome.send_keys(f"Degutti")
        endereco.send_keys(f"Avenida do Café, 48")
        cntt.send_keys("81999999948")
        chooser = Select(tipo)
        chooser.select_by_visible_text("Irish coffee")
        time.sleep(2)
        botaosave.send_keys(Keys.ENTER)
        time.sleep(2)

        #Adicionando a cafeteria aos favoritos

        botaoacesso = driver.find_element(by=By.XPATH, value="/html/body/section/div[2]/div/a")
        botaoacesso.send_keys(Keys.ENTER)
        time.sleep(1)
        botaoeditar = driver.find_element(by=By.XPATH, value="/html/body/section/div[1]/div/div[2]/div/a[2]")
        botaoeditar.send_keys(Keys.ENTER)
        time.sleep(1)
        status = driver.find_element(by=By.NAME, value="status_cafeteria")
        chooser = Select(status)
        chooser.select_by_visible_text("Favorita")
        time.sleep(2)
        botaosubmit = driver.find_element(by=By.XPATH, value="/html/body/section/div/form/button")
        botaosubmit.send_keys(Keys.ENTER)
        time.sleep(2)

        #Removendo a cafeteria diretamente da página de favoritos

        botaofavoritas = driver.find_element(by=By.XPATH, value="/html/body/div/ul/li[5]/a")
        botaofavoritas.send_keys(Keys.ENTER)
        time.sleep(2)
        botaodel = driver.find_element(by=By.XPATH, value="/html/body/section/div/div/div/div[2]/form/button")
        botaodel.send_keys(Keys.ENTER)
        time.sleep(2)
        self.assertEqual(driver.find_element(by=By.XPATH, value="/html/body/section/div/div[2]/p").text, ("Nenhuma cafeteria no favoritos."))
        botaologout = driver.find_element(by=By.XPATH, value="/html/body/div/ul/li[6]/a")
        botaologout.send_keys(Keys.ENTER)
        time.sleep(2)

    def test_2(self):
        #Fazendo login do usuário

        driver.get("http://127.0.0.1:8000/mainapp/login/")
        usuariologin = driver.find_element(by=By.NAME, value="username")
        senhalogin = driver.find_element(by=By.NAME, value="password")
        botaologin = driver.find_element(by=By.XPATH, value="/html/body/section/div/div/div/div/div[2]/form/div[3]/button")

        usuariologin.send_keys(f"user4")
        senhalogin.send_keys("Senha1234")
        time.sleep(2)
        botaologin.send_keys(Keys.ENTER)
        time.sleep(2)

        #Refavoritando a cafeteria
        botaocafeterias = driver.find_element(by=By.XPATH, value="/html/body/div/ul/li[3]/a")
        botaocafeterias.send_keys(Keys.ENTER)
        time.sleep(1)
        botaoacesso = driver.find_element(by=By.XPATH, value="/html/body/section/div[2]/div/a")
        botaoacesso.send_keys(Keys.ENTER)
        time.sleep(1)
        botaoeditar = driver.find_element(by=By.XPATH, value="/html/body/section/div[1]/div/div[2]/div/a[2]")
        botaoeditar.send_keys(Keys.ENTER)
        time.sleep(1)
        status = driver.find_element(by=By.NAME, value="status_cafeteria")
        chooser = Select(status)
        chooser.select_by_visible_text("Favorita")
        time.sleep(1)
        botaosubmit = driver.find_element(by=By.XPATH, value="/html/body/section/div/form/button")
        botaosubmit.send_keys(Keys.ENTER)
        time.sleep(2)
        botaofavoritas = driver.find_element(by=By.XPATH, value="/html/body/div/ul/li[5]/a")
        botaofavoritas.send_keys(Keys.ENTER)
        time.sleep(2)
        
        #Removendo a cafeteria pela página de edição
        botaocafeterias = driver.find_element(by=By.XPATH, value="/html/body/div/ul/li[3]/a")
        botaocafeterias.send_keys(Keys.ENTER)
        time.sleep(1)
        botaoacesso = driver.find_element(by=By.XPATH, value="/html/body/section/div[2]/div/a")
        botaoacesso.send_keys(Keys.ENTER)
        time.sleep(1)
        botaoeditar = driver.find_element(by=By.XPATH, value="/html/body/section/div[1]/div/div[2]/div/a[2]")
        botaoeditar.send_keys(Keys.ENTER)
        time.sleep(1)
        status = driver.find_element(by=By.NAME, value="status_cafeteria")
        chooser = Select(status)
        chooser.select_by_visible_text("Não Favorita")
        time.sleep(2)
        botaosubmit = driver.find_element(by=By.XPATH, value="/html/body/section/div/form/button")
        botaosubmit.send_keys(Keys.ENTER)
        time.sleep(3)

        #Checando se a cafeteria foi mesmo removida dos favoritos
        botaofavoritas = driver.find_element(by=By.XPATH, value="/html/body/div/ul/li[5]/a")
        botaofavoritas.send_keys(Keys.ENTER)
        time.sleep(3)
        self.assertEqual(driver.find_element(by=By.XPATH, value="/html/body/section/div/div/p").text, ("Nenhuma cafeteria no favoritos."))
        botaologout = driver.find_element(by=By.XPATH, value="/html/body/div/ul/li[6]/a")
        botaologout.send_keys(Keys.ENTER)
        time.sleep(2)

class AdicionarDesejo(LiveServerTestCase):

    def test_1(self):
        #Fazendo registro do usuário

        driver.get("http://127.0.0.1:8000/mainapp/cadastro/")
        usuario = driver.find_element(by=By.NAME, value="username")
        email = driver.find_element(by=By.NAME, value="email")
        senha = driver.find_element(by=By.NAME, value="password")
        botao = driver.find_element(by=By.XPATH, value="/html/body/section/div/div/div/div/div/form/button")

        usuario.send_keys(f"user5")
        email.send_keys(f"user5@gmail.com")
        senha.send_keys("Senha1234")
        time.sleep(2)
        botao.send_keys(Keys.ENTER)
        time.sleep(2)

        usuariologin = driver.find_element(by=By.NAME, value="username")
        senhalogin = driver.find_element(by=By.NAME, value="password")
        botaologin = driver.find_element(by=By.XPATH, value="/html/body/section/div/div/div/div/div[2]/form/div[3]/button")

        usuariologin.send_keys(f"user5")
        senhalogin.send_keys("Senha1234")
        time.sleep(2)
        botaologin.send_keys(Keys.ENTER)
        time.sleep(2)

        #Direcionando para a página de adicionar à lista de desejos

        botaolista = driver.find_element(by=By.XPATH, value="/html/body/div/ul/li[4]/a")
        botaolista.send_keys(Keys.ENTER)
        time.sleep(2)
        botaoadd = driver.find_element(by=By.XPATH, value="/html/body/section/div/div/a")
        botaoadd.send_keys(Keys.ENTER)
        time.sleep(2)

        #Adicionando uma cafeteria à lista de desejos

        nome = driver.find_element(by=By.NAME, value="nome")
        endereco = driver.find_element(by=By.NAME, value="endereco")
        cntt = driver.find_element(by=By.NAME, value="cntt")
        tipo = driver.find_element(by=By.NAME, value="tipo")
        botaosave = driver.find_element(by=By.XPATH, value="/html/body/section/div[2]/form/button")

        nome.send_keys(f"Versado")
        endereco.send_keys(f"Praça do Tiradentes, 75")
        cntt.send_keys("81999999975")
        chooser = Select(tipo)
        chooser.select_by_visible_text("caffè latte")
        time.sleep(2)
        botaosave.send_keys(Keys.ENTER)
        time.sleep(2)
        self.assertEqual(driver.find_element(by=By.XPATH, value="/html/body/section/div/div[1]/p").text, ("cafeteria adicionada à lista de desejos com sucesso."))
        botaologout = driver.find_element(by=By.XPATH, value="/html/body/div/ul/li[6]/a")
        botaologout.send_keys(Keys.ENTER)
        time.sleep(2)

class GerenciarDesejos(LiveServerTestCase):

    def test_1(self):
        #Fazendo registro do usuário

        driver.get("http://127.0.0.1:8000/mainapp/cadastro/")
        usuario = driver.find_element(by=By.NAME, value="username")
        email = driver.find_element(by=By.NAME, value="email")
        senha = driver.find_element(by=By.NAME, value="password")
        botao = driver.find_element(by=By.XPATH, value="/html/body/section/div/div/div/div/div/form/button")

        usuario.send_keys(f"user6")
        email.send_keys(f"user6@gmail.com")
        senha.send_keys("Senha1234")
        time.sleep(2)
        botao.send_keys(Keys.ENTER)
        time.sleep(2)

        usuariologin = driver.find_element(by=By.NAME, value="username")
        senhalogin = driver.find_element(by=By.NAME, value="password")
        botaologin = driver.find_element(by=By.XPATH, value="/html/body/section/div/div/div/div/div[2]/form/div[3]/button")

        usuariologin.send_keys(f"user6")
        senhalogin.send_keys("Senha1234")
        time.sleep(2)
        botaologin.send_keys(Keys.ENTER)
        time.sleep(2)

        #Direcionando para a página de adicionar à lista de desejos

        botaolista = driver.find_element(by=By.XPATH, value="/html/body/div/ul/li[4]/a")
        botaolista.send_keys(Keys.ENTER)
        time.sleep(2)
        botaoadd = driver.find_element(by=By.XPATH, value="/html/body/section/div/div/a")
        botaoadd.send_keys(Keys.ENTER)
        time.sleep(2)

        #Adicionando uma cafeteria à lista de desejos

        nome = driver.find_element(by=By.NAME, value="nome")
        endereco = driver.find_element(by=By.NAME, value="endereco")
        cntt = driver.find_element(by=By.NAME, value="cntt")
        tipo = driver.find_element(by=By.NAME, value="tipo")
        botaosave = driver.find_element(by=By.XPATH, value="/html/body/section/div[2]/form/button")

        nome.send_keys(f"Harina")
        endereco.send_keys(f"Avenida Grão Forte, 208")
        cntt.send_keys("8199999208")
        chooser = Select(tipo)
        chooser.select_by_visible_text("duplo")
        botaosave.send_keys(Keys.ENTER)
        time.sleep(3)

        #Movendo a cafeteria na lista de desejos para a lista de cafeterias frequentadas
        
        botaomover = driver.find_element(by=By.XPATH, value="/html/body/section/div/div[2]/div/div/form[1]/button")
        botaomover.send_keys(Keys.ENTER)
        time.sleep(2)
        botaocafeterias = driver.find_element(by=By.XPATH, value="/html/body/div/ul/li[3]/a")
        botaocafeterias.send_keys(Keys.ENTER)
        time.sleep(4)
        self.assertEqual(driver.find_element(by=By.XPATH, value="/html/body/section/div[2]/div/a/div/div[1]").text, ("Harina por Avenida Grão Forte, 208 (8199999208)"))
        botaologout = driver.find_element(by=By.XPATH, value="/html/body/div/ul/li[6]/a")
        botaologout.send_keys(Keys.ENTER)
        time.sleep(2)

    def test_2(self):
        #Fazendo login do usuário

        driver.get("http://127.0.0.1:8000/mainapp/login/")
        usuariologin = driver.find_element(by=By.NAME, value="username")
        senhalogin = driver.find_element(by=By.NAME, value="password")
        botaologin = driver.find_element(by=By.XPATH, value="/html/body/section/div/div/div/div/div[2]/form/div[3]/button")

        usuariologin.send_keys(f"user6")
        senhalogin.send_keys("Senha1234")
        time.sleep(2)
        botaologin.send_keys(Keys.ENTER)
        time.sleep(2)

        #Direcionando para a página de adicionar à lista de desejos

        botaolista = driver.find_element(by=By.XPATH, value="/html/body/div/ul/li[4]/a")
        botaolista.send_keys(Keys.ENTER)
        time.sleep(2)
        botaoadd = driver.find_element(by=By.XPATH, value="/html/body/section/div/div/a")
        botaoadd.send_keys(Keys.ENTER)
        time.sleep(2)

        #Adicionando uma cafeteria à lista de desejos

        nome = driver.find_element(by=By.NAME, value="nome")
        endereco = driver.find_element(by=By.NAME, value="endereco")
        cntt = driver.find_element(by=By.NAME, value="cntt")
        tipo = driver.find_element(by=By.NAME, value="tipo")
        botaosave = driver.find_element(by=By.XPATH, value="/html/body/section/div[2]/form/button")

        nome.send_keys(f"Go Coffee")
        endereco.send_keys(f"Avenida Grão Forte, 207")
        cntt.send_keys("8199999207")
        chooser = Select(tipo)
        chooser.select_by_visible_text("duplo")
        botaosave.send_keys(Keys.ENTER)
        time.sleep(3)

        #Removendo cafeteria da lista de desejos

        botaodel = driver.find_element(by=By.XPATH, value="/html/body/section/div/div[2]/div/div/form[2]/button")
        botaodel.send_keys(Keys.ENTER)
        time.sleep(3)
        time.sleep(4)
        self.assertEqual(driver.find_element(by=By.XPATH, value="/html/body/section/div/div[1]/p").text, ("cafeteria removida da lista de desejos com sucesso."))
        botaologout = driver.find_element(by=By.XPATH, value="/html/body/div/ul/li[6]/a")
        botaologout.send_keys(Keys.ENTER)
        time.sleep(2)