from django.db import models

class Categoria(models.Model):
   nome = models.CharField(max_length=100)

   def __str__(self):
      return self.nome

class Produto(models.Model):
   id_produto = models.AutoField(primary_key=True)
   nome = models.CharField(max_length=100)
   preco = models.DecimalField(max_digits=10,decimal_places=2)  #casas decimais
   descricao = models.TextField()
   categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, blank=True, null=True)
   imagem = models.ImageField(upload_to='produtos/', null=True, blank=True)

   def __str__(self):
      return self.nome
   
class Estoque(models.Model):
   id_produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
   quantidade = models.IntegerField()
   data = models.DateField()

   def __str__(self):
      return f"Produto: {self.id_produto.nome} - Quantidade: {self.quantidade} - Data de Aquisicao: {self.data}"

class Venda(models.Model):
   id_venda = models.IntegerField(primary_key=True)
   id_produto = models.ForeignKey(Estoque, on_delete=models.CASCADE)
   quantidade = models.IntegerField()
   data = models.DateField()
   total = models.DecimalField(max_digits=10,decimal_places=2)

   def __str__(self):
      return f"Venda: {self.id_venda} - Produto: {self.id_produto.nome} - Quantidade: {self.quantidade} - Data: {self.data} - Total: {self.total}"