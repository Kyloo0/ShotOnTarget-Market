from django.test import TestCase, Client
from .models import Product

# Create your tests here.
class ProductModelTest(TestCase):
    def test_show_page(self):
        response = Client().get('')
        self.assertEqual(response.status_code, 200)

    def test_create_product(self):
        product = Product.objects.create(
            name = "Bola Jabulani",
            price = 500000,
            description = "Bola resmi Piala Dunia 2010 tanda tangan pemain Spanyol",
            category = "match equipment",
            stock = 20
        )
        self.assertEqual(product.name, "Bola Jabulani")
        self.assertEqual(product.price, 500000)
        self.assertEqual(product.description, "Bola resmi Piala Dunia 2010 tanda tangan pemain Spanyol")
        self.assertEqual(product.category, "match equipment")
        self.assertEqual(product.stock, 20)

    def test_create_purchased_product(self):
        product = Product.objects.create(
            name = "Jersey Cristiano Ronaldo",
            description = "Jersey Portugal nomor punggung 7",
            category = "team kit",
            quantity_purchased = 5
        )
        self.assertEqual(product.quantity_purchased, 5)

    def test_best_seller_product(self):
        product = Product.objects.create(
            name = "Sepatu Nike Mercurial",
            quantity_purchased = 15
        )
        self.assertTrue(product.is_thebest_seller)

    def test_update_stock(self):
        product = Product.objects.create(
            name = "Sepatu Adidas Predator",
            stock = 30,
            quantity_purchased = 10
        )
        product.update_stok()
        self.assertEqual(product.stock, 20)
    
    def test_total_price(self):
        product = Product.objects.create(
            name = "Bola Nike Flight",
            price = 600000,
            quantity_purchased = 3
        )
        self.assertEqual(product.total_price(), 1800000)
