from django.db import models
import os
from pydoc import locate


# Create your models here.
class Report(models.Model):
    name = models.CharField(max_length=255)
    form = models.CharField(max_length=512)

    @property 
    def filename(self):
        return self.name.lower().replace(' ', '_')

    @property
    def template_path(self):
        return os.path.join('reports', self.filename + '_template.html')

    @property
    def render_func(self):
        return locate('reports.scripts.' + self.filename + '.render')

    def save(self,*args, **kwargs):
        if self.pk:
            super().save(*args, **kwargs)
            return

        py_dir = os.path.join('reports', 'scripts', self.filename + '.py')
        if os.path.exists(py_dir):
            super().save(*args, **kwargs)
            return
            
        with open(py_dir, 'w') as f:
            f.writelines([
                'def render(filters):\n',
                '   context = {}\n'
                '   return context\n',
                '\n',
            ])
        
        with open(os.path.join('reports', 'templates', 'reports', self.filename + '_template.html'), 'w') as f:
            f.writelines(['<!-- write your report here -->'])

        super().save(*args, **kwargs)
