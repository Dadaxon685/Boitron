# core/models.py

from django.db import models

class User(models.Model):
    tg_id = models.BigIntegerField(unique=True)
    name = models.CharField(max_length=150)
    balance = models.IntegerField(default=0)
    is_premium = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.tg_id})"

# ===== SAVOLLAR UCHUN TIZIM =====
class BookEdition(models.Model):
    """Darslik davri: 2017-2019 yoki 2022-2024"""
    name = models.CharField(max_length=100, verbose_name="Davri")
    start_year = models.IntegerField()
    end_year = models.IntegerField()

    def __str__(self):
        return f"{self.start_year}–{self.end_year}"

class Grade(models.Model):
    """Sinf: 6, 7, 8, 9, 10, 11"""
    number = models.IntegerField(choices=[(i, f"{i}-sinf") for i in range(6, 12)])

    def __str__(self):
        return f"{self.number}-sinf"

class Topic(models.Model):
    """Mavzu: Hujayra, DNK, Fotosintez..."""
    name = models.CharField(max_length=200, verbose_name="Mavzu nomi")
    edition = models.ForeignKey(BookEdition, on_delete=models.CASCADE, related_name='topics')
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='topics')

    class Meta:
        verbose_name = "Mavzu"
        verbose_name_plural = "Mavzular"

    def __str__(self):
        return f"{self.grade} | {self.name} ({self.edition})"

class PracticeQuestion(models.Model):
    """Savol + javob (faqat ko'rish uchun)"""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField(verbose_name="Savol")
    answer_text = models.TextField(verbose_name="Javob / Tushuntirish")

    def __str__(self):
        return f"Savol: {self.question_text[:50]}..."
    


# Testlar uchun
class Test(models.Model):
    title = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='tests')
    def __str__(self):
        return self.title

class TestQuestion(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, null=True, blank=True)
    text = models.TextField()
    option_a = models.CharField(max_length=300)
    option_b = models.CharField(max_length=300)
    option_c = models.CharField(max_length=300)
    CORRECT_CHOICES = [('A', 'A'), ('B', 'B'), ('C', 'C')]
    correct_answer = models.CharField(max_length=1, choices=CORRECT_CHOICES)

    def __str__(self):
        return f"Test: {self.text[:50]}..."
    

# core/models.py

class Announcement(models.Model):
    message = models.TextField(verbose_name="Xabar matni", help_text="HTML ishlatish mumkin, lekin tavsiya etilmaydi")
    is_active = models.BooleanField(default=True, verbose_name="Ko'rsatilsinmi?")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Bildirishnoma"
        verbose_name_plural = "Bildirishnomalar"
        ordering = ['-created_at']

    def __str__(self):
        return self.message[:50] + ("..." if len(self.message) > 50 else "")
    






# models.py


class PaymentSettings(models.Model):
    title = models.CharField(max_length=100, default="Balansni to'ldirish")
    user_label = models.CharField(max_length=100, default="Foydalanuvchi:")
    card_label = models.CharField(max_length=100, default="To'lov uchun karta raqami:")
    card_number = models.CharField(max_length=20, default="8600 1234 5678 9012")
    card_type = models.CharField(max_length=50, default="Humo / UzCard")
    admin_label = models.CharField(max_length=100, default="Admin bilan bog'lanish:")
    admin_telegram = models.CharField(max_length=100, default="@biotron_admin")
    admin_telegram_link = models.URLField(default="https://t.me/biotron_admin")
    instruction_title = models.CharField(max_length=100, default="✅ To'lovni tasdiqlash:")
    instruction_text = models.TextField(
        default="1. Yuqoridagi karta raqamiga kerakli summani o'tkazing.<br>\n"
                "2. <strong>To'lov chekining (skrinshot) rasm</strong>ni yuqoridagi Telegram admin @biotron_admin ga yuboring.<br>\n"
                "3. Balans 5 daqiqada hisobingizga qo'shiladi."
    )
    
    def __str__(self):
        return "To'lov sozlamalari"

    class Meta:
        verbose_name = "To'lov sozlamasi"
        verbose_name_plural = "To'lov sozlamalari"