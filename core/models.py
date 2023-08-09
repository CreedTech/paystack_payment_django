import secrets
from django.db import models
from .paystack import PayStack
  
# Create your models here.
class Payment(models.Model):
    amount = models.PositiveIntegerField()
    ref = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    verified = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    

    class Meta:
        verbose_name = ("Payment")
        verbose_name_plural = ("Payments")
        ordering = ['-date_created']

    def __str__(self):
        return f"Payment: {self.amount}"
    
    def save(self, *args, **kwargs):
        while not self.ref:
            ref = secrets.token_urlsafe(50)
            object_with_similar_ref = Payment.objects.filter(ref=ref)
            if not object_with_similar_ref:
                self.ref = ref
        super().save(*args, **kwargs)

    def amount_value(self):
        return self.amount * 100

    def verify_payment(self):
        paystack = PayStack()
        status, result = paystack.verify_payment(self.ref, self.amount)
        if status:
            if result['amount'] / 100 == self.amount:
                self.verified = True
            self.save()
        if self.verified:
                return True
        return False

    # def get_absolute_url(self):
    #     return reverse("Payment_detail", kwargs={"pk": self.pk})
