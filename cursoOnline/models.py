from django.db import models

# "Curso"(Course) Table Model
class Curso(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.CharField(max_length=2000)
    linkname = models.CharField(max_length=200, default="null")
    def __str__(self):
        return self.nome

# "Participante"(User) Table Model
class Participante(models.Model):
    nome = models.CharField(max_length=200)
    password = models.CharField(max_length=20)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    passed = models.BooleanField(default=False)
    def __str__(self):
        return self.nome

# "Mensagem"(Post) Table Model
class Mensagem(models.Model):
    link = models.CharField(max_length=2000, default="null")
    content = models.CharField(max_length=2000)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    pub_date = models.DateTimeField('data de publicacao')
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    participante = models.ForeignKey(Participante, on_delete=models.CASCADE)
    isLink = models.BooleanField(default=False)
    def __str__(self):
        return self.content

# "Questao"(Questio) Table Model
class Questao(models.Model):
    questao_texto = models.CharField(max_length=200)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    def __str__(self):
        return self.questao_texto

# "Opcao"(Option) Table Model
class Opcao(models.Model):
    questao = models.ForeignKey(Questao, on_delete=models.CASCADE)
    opcao_texto = models.CharField(max_length=200)
    certo= models.BooleanField(default=False)
    votos = models.IntegerField(default=0)
    def __str__(self):
        return self.opcao_texto