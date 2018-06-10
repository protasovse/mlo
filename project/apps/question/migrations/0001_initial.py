# Generated by Django 2.0.2 on 2018-06-10 06:15

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
    ]

    operations = [
        migrations.RunSQL("INSERT INTO `dbmail_mailtemplate` (`id`,`name`,`subject`,`message`,`slug`,`num_of_retries`,`priority`,`is_html`,`is_admin`,`is_active`,`enable_log`,`created`,`updated`,`context_note`,`interval`,`base_id`,`category_id`,`from_email_id`) VALUES (12,'Уведомление эксперта о новом вопросе (подписка)','Новый вопрос: бесплатная консультация','<p>Новый вопрос по интересной вам теме: <a href=\"{{protocol}}://{{site}}{{question.get_absolute_url}}\">{{protocol}}://{{site}}{{question.get_absolute_url}}</a></p>\r\n\r\n<p><b>Заголовок вопроса: «{{question.title}}»</b></p>\r\n\r\n{{question.html_content|safe}}\r\n\r\n<p><a href=\"{{protocol}}://{{site}}{{question.get_absolute_url}}\">Ответить</a></p>','new_question_to_expert',1,6,1,0,1,1,'2018-06-10 04:03:53','2018-06-10 06:04:57','',NULL,1,2,1);")
    ]
