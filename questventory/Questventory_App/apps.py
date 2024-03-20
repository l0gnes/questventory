from django.apps import AppConfig


class QuestventoryAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "Questventory_App"

    # This makes sure that the subscriber is available whenever the server is started.
    # This method is called whenever Django starts up, and ensures resources are accessible
    # when they are needed.
    def ready(self):
        from .observerKeepTrackOfStock import StockObserver, LowStockSubscriber

        # Create an instance of the low stock subscriber, which notifies the user the stock
        # of a particular product is low.
        restock_subscriber = LowStockSubscriber(observer=StockObserver.get_instance())

        # Tell the observer to listen and relay updates of game stock to the `restock_subscriber`
        StockObserver.get_instance().subscribe(restock_subscriber)
