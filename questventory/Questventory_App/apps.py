from django.apps import AppConfig


class QuestventoryAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "Questventory_App"
    
    
    # This makes sure that the subscriber is available whenever the server is started.
    def ready(self):
        from .observerKeepTrackOfStock import global_stock_observer, LowStockSubscriber
        restock_subscriber = LowStockSubscriber(observer=global_stock_observer)
        global_stock_observer.subscribe(restock_subscriber)