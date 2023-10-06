from poker import PokerApp
from interface import GraphicsInterface


interface = GraphicsInterface()
app = PokerApp(interface)
app.run()
