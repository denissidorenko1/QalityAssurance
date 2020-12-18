#from django.test import TestCase

# Create your tests here.
from selenium import webdriver
import unittest
from selenium.webdriver.common.keys import Keys
import time

time.sleep(5)
class Test2(unittest.TestCase):
    def setUp(self):
        self.driver =webdriver.Chrome("C:\chromedriver\chromedriver.exe")
        self.driver.get("http://127.0.0.1:8000/ru/routesearcher/")

    def testSimplePath(self):
        driver= self.driver
        x01 = driver.find_element_by_name("x01")
        input_a = driver.find_element_by_name("a_node")
        input_b = driver.find_element_by_name("b_node")
        input_a.send_keys("0")
        input_b.send_keys("1")
        x01.click()
        send = driver.find_element_by_name("submit")
        send.click()
        path = driver.find_element_by_id("pth")
        print(path.text)
        self.assertEqual(path.text, "Путь: 0 1")

    def testNoPath(self):
        driver = self.driver
        input_a = driver.find_element_by_name("a_node")
        input_b = driver.find_element_by_name("b_node")
        input_a.send_keys("0")
        input_b.send_keys("5")
        send = driver.find_element_by_name("submit")
        send.click()
        path = driver.find_element_by_id("pth")
        self.assertEqual(path.text, "Путь: Пути нет")

    def testDefault(self):
        driver = self.driver
        input_a = driver.find_element_by_name("a_node")
        input_b = driver.find_element_by_name("b_node")
        path = driver.find_element_by_id("pth")
        self.assertEqual(input_a.text, "")
        self.assertEqual(input_b.text, "")
        self.assertEqual(path.text, "Путь:")

    def testFieldMissing(self):
        driver = self.driver
        input_a = driver.find_element_by_name("a_node")
        input_a.send_keys("0")
        send = driver.find_element_by_name("submit")
        send.click()
        path = driver.find_element_by_id("pth")
        self.assertEqual(path.text, "Путь:")
