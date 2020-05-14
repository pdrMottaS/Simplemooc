from django.db import models
from django.conf import settings
from simplemooc.core.mail import send_mail_template
from django.utils import timezone
import datetime

class CourseManager(models.Manager):

    def search(self,query):
        return self.get_queryset().filter(
            models.Q(name__icontains=query) | 
            models.Q(description__icontains=query)
        )


class Course(models.Model):
    name=models.CharField('name', max_length=100)
    slug=models.SlugField('atalho')
    description=models.TextField('Descrição Curta', blank=True)
    about=models.TextField('Sobre', blank=True)
    start_date=models.DateField('Data de Início', null=True, blank=True)
    image=models.ImageField(upload_to='courses/images', verbose_name='Imagem', null=True, blank=True)
    created_at=models.DateTimeField('Criado em', auto_now_add=True)
    updated_at=models.DateTimeField('Atualizado em', auto_now=True)
    objects=CourseManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
         return "/courses/%s/" % self.slug
    
    def release_lessons(self):
        today=timezone.now().date()
        return self.lessons.filter(release_date__lte=today)
    
    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural='Cursos'
        ordering= ['name']

class Enrollment(models.Model):

    STATUS_CHOICE=(
        (0,'Pendente'),
        (1,'Aprovado'),
        (2,'Cancelado')
    )

    user=models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='user', related_name='enrollments', on_delete=models.DO_NOTHING)
    course=models.ForeignKey(Course, verbose_name='course', related_name='enrollments', on_delete=models.DO_NOTHING)
    status=models.IntegerField('Status',choices=STATUS_CHOICE,default=1,blank=True)
    created_at=models.DateTimeField('Criado em', auto_now_add=True)
    updated_at=models.DateTimeField('Atualizado em', auto_now=True)

    def activate(self):
        self.status=1
        self.save()

    def is_approved(self):
        return self.status==1

    class Meta:
        verbose_name='Inscrição'
        verbose_name_plural='Inscrições'
        unique_together=(('user','course'))

class Announcements(models.Model):
    course=models.ForeignKey(Course, verbose_name='Curso', related_name='announcements',on_delete=models.DO_NOTHING)
    title=models.CharField('Título', max_length=100)
    content=models.TextField('Conteúdo')
    created_at=models.DateTimeField('Criado em', auto_now_add=True)
    updated_at=models.DateTimeField('Atualizado em', auto_now=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name='Anúncio'
        verbose_name_plural='Anúncios'
        ordering=['-created_at']

class Comment(models.Model):
    announcement=models.ForeignKey(Announcements, verbose_name='Anúncio', related_name='comments', on_delete=models.DO_NOTHING)
    user=models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Usuário', on_delete=models.DO_NOTHING)
    comment=models.TextField('Comentário')
    created_at=models.DateTimeField('Criado em', auto_now_add=True)
    updated_at=models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name='Comentário'
        verbose_name_plural='Comentários'
        ordering=['created_at']

def post_save_announcement(instance, created, **kwargs):
    if created:
        subject=instance.title
        context={
            'announcement':instance
        }
        template_name='courses/announcement_mail.html'
        enrollments=Enrollment.objects.filter(course=instance.course, status=1)
        for enrollment in enrollments:
            recipient_list=[enrollment.user.email]
            send_mail_template(subject,template_name,context,recipient_list)

models.signals.post_save.connect(
    post_save_announcement, sender=Announcements,dispatch_uid='post_save_announcement'
)

class Lessons(models.Model):
    name=models.CharField('Name',max_length=100)
    description=models.TextField('Descrição', blank=True)
    numbers=models.IntegerField('Número(Ordem)', blank=True, default=0)
    release_date=models.DateField('Data de Liberação', blank=True, null=True)
    course=models.ForeignKey(Course, verbose_name='curso', related_name='lessons', on_delete=models.DO_NOTHING)
    created_at=models.DateTimeField('Criado em', auto_now_add=True)
    updated_at=models.DateTimeField('Atualizado em', auto_now=True)

    def __str__(self):
        return self.name
    
    def is_available(self):
        if self.release_date:
            today=timezone.now().date()
            return self.release_date <= today
        return False

    class Meta:
        verbose_name='Aula'
        verbose_name_plural='Aulas'
        ordering=['numbers']

class Material(models.Model):
    name=models.CharField('Name',max_length=100)
    embedded=models.TextField('Vídeo Embedded', blank=True)
    files=models.FileField(upload_to='lessons/materials', blank=True, null=True)
    lesson=models.ForeignKey(Lessons,verbose_name='aula', related_name='materials', on_delete=models.DO_NOTHING)

    def is_embedded(self):
        return bool(self.embedded)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name='Material'
        verbose_name_plural='Materiais'