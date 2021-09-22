from django.apps import AppConfig


class PaymentConfig(AppConfig):
    name = 'payment'

    def ready(self):
        print("at ready")
        import payment.signals
