# Laboratorio - Patrones de Diseño (Ingeniería de Software II)
# Incluye definiciones de clases y bloque de pruebas.

import copy

# ==========================================
# 1. PATRONES CREACIONALES
# ==========================================

# 1.1 Builder
class Coffee:
    def __init__(self, size=None, milk=None, sugar=0, extras=None):
        self.size = size
        self.milk = milk
        self.sugar = sugar
        self.extras = extras or []
        
    def __str__(self):
        return f"Coffee (size={self.size}, milk={self.milk}, sugar={self.sugar}, extras={self.extras})"

class CoffeeBuilder:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self._size = None
        self._milk = None
        self._sugar = 0
        self._extras = []
        return self
        
    def set_size(self, size):
        self._size = size
        return self
        
    def add_milk(self, milk_type):
        self._milk = milk_type
        return self
        
    def add_sugar(self, spoons):
        self._sugar = spoons
        return self
        
    def add_extra(self, extra):
        self._extras.append(extra)
        return self
        
    def build(self):
        coffee = Coffee(self._size, self._milk, self._sugar, self._extras)
        self.reset()
        return coffee

# 1.2 Prototype
class PromoBanner:
    def __init__(self, title, text, discount):
        self.title = title
        self.text = text
        self.discount = discount
        
    def clone(self):
        return copy.deepcopy(self)
        
    def __str__(self):
        return f"[{self.title}] {self.text} ({self.discount}% off)"

# 1.3 Singleton
class AppConfig:
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance
        
    def __init__(self, db_url=None):
        if not hasattr(self, "db_url"):
            self.db_url = db_url or "sqlite://local.db"

# 1.4 Factory Method
class Chocolate:
    def prepare(self):
        raise NotImplementedError

class ChocolateBar(Chocolate):
    def prepare(self):
        return "Preparando una barra de chocolate Wonka"

class FizzyLiftingDrink(Chocolate):
    def prepare(self):
        return "Preparando un Fizzy Lifting Drink (bebida burbujeante)"

class EverlastingGobstopper(Chocolate):
    def prepare(self):
        return "Preparando un Everlasting Gobstopper (caramelo eterno)"

class WonkaFactory:
    def create_candy(self, candy_type: str) -> Chocolate:
        candy_type = candy_type.lower()
        if candy_type == "bar":
            return ChocolateBar()
        elif candy_type == "fizzy":
            return FizzyLiftingDrink()
        elif candy_type == "gobstopper":
            return EverlastingGobstopper()
        else:
            raise ValueError("Ese dulce no existe en la fábrica de Willy Wonka.")

# ==========================================
# 2. PATRONES ESTRUCTURALES
# ==========================================

# 2.1 Adapter
class PaymentProcessor:
    def pay(self, amount: float) -> str:
        raise NotImplementedError

class LegacyPaymentGateway:
    def make_payment(self, value_in_cents: int) -> str:
        return f"Pago legacy procesado por {value_in_cents} centavos"

class LegacyPaymentAdapter(PaymentProcessor):
    def __init__(self, legacy_gateway: LegacyPaymentGateway):
        self.legacy = legacy_gateway
        
    def pay(self, amount: float) -> str:
        cents = int(amount * 100)
        return self.legacy.make_payment(cents)

# 2.2 Decorator
class Notifier:
    def send(self, message: str) -> None:
        raise NotImplementedError

class EmailNotifier(Notifier):
    def send(self, message: str) -> None:
        print(f"[Email] {message}")

class NotifierDecorator(Notifier):
    def __init__(self, wrapped: Notifier):
        self._wrapped = wrapped
        
    def send(self, message: str) -> None:
        self._wrapped.send(message)

class SMSDecorator(NotifierDecorator):
    def send(self, message: str) -> None:
        super().send(message)
        print(f"[SMS] {message}")

class SlackDecorator(NotifierDecorator):
    def send(self, message: str) -> None:
        super().send(message)
        print(f"[Slack] {message}")

# 2.3 Facade
class Projector:
    def on(self): print("Proyector encendido")
    def off(self): print("Proyector apagado")

class SoundSystem:
    def set_volume(self, level): print(f"Volumen en {level}")
    def off(self): print("Sonido apagado")

class StreamingPlayer:
    def play(self, movie): print(f"Reproduciendo '{movie}'")
    def stop(self): print("Reproducción detenida")

class HomeTheaterFacade:
    def __init__(self, projector, sound, player):
        self.projector = projector
        self.sound = sound
        self.player = player
        
    def ver_pelicula(self, movie):
        self.projector.on()
        self.sound.set_volume(7)
        self.player.play(movie)
        
    def terminar(self):
        self.player.stop()
        self.sound.off()
        self.projector.off()

# 2.4 Composite
class FileSystemItem:
    def __init__(self, name: str):
        self.name = name
        
    def get_size(self) -> int:
        raise NotImplementedError

class File(FileSystemItem):
    def __init__(self, name: str, size: int):
        super().__init__(name)
        self._size = size
        
    def get_size(self) -> int:
        return self._size

class Folder(FileSystemItem):
    def __init__(self, name: str):
        super().__init__(name)
        self.children: list[FileSystemItem] = []
        
    def add(self, item: FileSystemItem):
        self.children.append(item)
        
    def get_size(self) -> int:
        return sum(child.get_size() for child in self.children)


# ==========================================
# 3. PATRONES DE COMPORTAMIENTO
# ==========================================

# 3.1 Strategy
class DiscountStrategy:
    def apply(self, total: float) -> float:
        raise NotImplementedError

class NoDiscount(DiscountStrategy):
    def apply(self, total): return total

class StudentDiscount(DiscountStrategy):
    def apply(self, total): return total * 0.90

class EmployeeDiscount(DiscountStrategy):
    def apply(self, total): return total * 0.80

class VIPDiscount(DiscountStrategy):
    def apply(self, total): return total * 0.70

class Cart:
    def __init__(self, strategy: DiscountStrategy):
        self.items = []
        self.strategy = strategy
        
    def add(self, price: float):
        self.items.append(price)
        
    def total(self) -> float:
        return self.strategy.apply(sum(self.items))

# 3.2 Observer
class Subscriber:
    def update(self, video: str):
        raise NotImplementedError

class Channel:
    def __init__(self, name: str):
        self.name = name
        self._subs: list[Subscriber] = []
        
    def subscribe(self, sub: Subscriber):
        self._subs.append(sub)
        
    def unsubscribe(self, sub: Subscriber):
        self._subs.remove(sub)
        
    def publish(self, video: str):
        print(f"\n{self.name} publicó: {video}")
        for sub in self._subs:
            sub.update(video)

class EmailSubscriber(Subscriber):
    def __init__(self, email): self.email = email
    def update(self, video):
        print(f" -> Email a {self.email}: nuevo video '{video}'")

class MobileSubscriber(Subscriber):
    def __init__(self, user): self.user = user
    def update(self, video):
        print(f" -> Push a {self.user}: '{video}'")

# 3.3 Command
class Light:
    def __init__(self): self.is_on = False
    def turn_on(self): self.is_on = True; print("Luz: ON")
    def turn_off(self): self.is_on = False; print("Luz: OFF")

class Command:
    def execute(self): raise NotImplementedError
    def undo(self): raise NotImplementedError

class TurnOnCommand(Command):
    def __init__(self, light): self.light = light
    def execute(self): self.light.turn_on()
    def undo(self): self.light.turn_off()

class TurnOffCommand(Command):
    def __init__(self, light): self.light = light
    def execute(self): self.light.turn_off()
    def undo(self): self.light.turn_on()

class RemoteControl:
    def __init__(self): self.history: list[Command] = []
    def press(self, command: Command):
        command.execute()
        self.history.append(command)
        
    def undo(self):
        if self.history:
            self.history.pop().undo()

# 3.4 Template Method
class Report:
    def generate(self, data: dict) -> str:
        parts = [self.header(data), self.body(data), self.footer(data)]
        return "\n".join(parts)
        
    def header(self, data): raise NotImplementedError
    def body(self, data): raise NotImplementedError
    def footer(self, data): raise NotImplementedError

class TextReport(Report):
    def header(self, data): return f"=== {data['title']} ==="
    def body(self, data): return data['content']
    def footer(self, data): return f"-- Generado por {data['author']} --"

class HTMLReport(Report):
    def header(self, data): return f"<h1>{data['title']}</h1>"
    def body(self, data): return f"<p>{data['content']}</p>"
    def footer(self, data): return f"<footer>{data['author']}</footer>"

# 3.5 State
class OrderState:
    def pay(self, order): print("Acción no permitida en este estado")
    def ship(self, order): print("Acción no permitida en este estado")
    def deliver(self, order): print("Acción no permitida en este estado")

class Pending(OrderState):
    def pay(self, order):
        print("Pago recibido")
        order.state = Paid()

class Paid(OrderState):
    def ship(self, order):
        print("Pedido enviado")
        order.state = Shipped()

class Shipped(OrderState):
    def deliver(self, order):
        print("Pedido entregado")
        order.state = Delivered()

class Delivered(OrderState):
    pass # estado final

class Order:
    def __init__(self):
        self.state: OrderState = Pending()
        
    def pay(self): self.state.pay(self)
    def ship(self): self.state.ship(self)
    def deliver(self): self.state.deliver(self)


# ==========================================
# BLOQUE DE PRUEBAS (EJECUCIÓN)
# ==========================================
if __name__ == '__main__':
    print("--- 1.1 Builder ---")
    builder = CoffeeBuilder()
    latte = (builder.set_size("grande")
             .add_milk("almendra")
             .add_sugar(2)
             .add_extra("canela")
             .build())
    espresso = builder.set_size("pequeño").build()
    print(latte)
    print(espresso)
    print("\n--- 1.2 Prototype ---")
    base_promo = PromoBanner(title="Promo de la semana", text="Café + croissant", discount=20)
    promo_lunes = base_promo.clone()
    promo_lunes.title = "Lunes de energía"
    promo_viernes = base_promo.clone()
    promo_viernes.discount = 30
    print(base_promo)
    print(promo_lunes)
    print(promo_viernes)
    
    print("\n--- 1.3 Singleton ---")
    config1 = AppConfig("postgres://prod")
    config2 = AppConfig("otro") 
    print("Config1:", config1.db_url)
    print("Config2:", config2.db_url)
    print("¿Son el mismo objeto?:", config1 is config2)
    
    print("\n--- 1.4 Factory Method ---")
    factory = WonkaFactory()
    print(factory.create_candy("bar").prepare())
    print(factory.create_candy("fizzy").prepare())
    print(factory.create_candy("gobstopper").prepare())

    print("\n--- 2.1 Adapter ---")
    gateway = LegacyPaymentGateway()
    processor = LegacyPaymentAdapter(gateway)
    print(processor.pay(25.50))
    
    print("\n--- 2.2 Decorator ---")
    notifier = SlackDecorator(SMSDecorator(EmailNotifier()))
    notifier.send("Servidor caído")
    
    print("\n--- 2.3 Facade ---")
    theater = HomeTheaterFacade(Projector(), SoundSystem(), StreamingPlayer())
    theater.ver_pelicula("Interstellar")
    theater.terminar()
    
    print("\n--- 2.4 Composite ---")
    root = Folder("proyecto")
    root.add(File("README.md", 2))
    src = Folder("src")
    src.add(File("main.py", 10))
    src.add(File("utils.py", 5))
    root.add(src)
    print(f"Tamaño total de la carpeta raíz: {root.get_size()}")
    
    print("\n--- 3.1 Strategy ---")
    cart = Cart(StudentDiscount())
    cart.add(100); cart.add(50)
    print(f"Total estudiante: {cart.total()}")
    cart.strategy = VIPDiscount()
    print(f"Total VIP: {cart.total()}")
    
    print("\n--- 3.2 Observer ---")
    channel = Channel("DevTalks")
    channel.subscribe(EmailSubscriber("ana@x.com"))
    channel.subscribe(MobileSubscriber("@carlos"))
    channel.publish("Patrones de Diseño en Python")
    
    print("\n--- 3.3 Command ---")
    light = Light()
    remote = RemoteControl()
    remote.press(TurnOnCommand(light))
    remote.press(TurnOffCommand(light))
    remote.undo()
    remote.undo()
    
    print("\n--- 3.4 Template Method ---")
    data = {"title": "Ventas Q4", "content": "Crecimos 12%", "author": "C. Sierra"}
    print(TextReport().generate(data))
    print()
    print(HTMLReport().generate(data))
    
    print("\n--- 3.5 State ---")
    order = Order()
    order.ship()
    order.pay()
    order.ship()
    order.deliver()
