import pygame
import pygame.locals
import socket
import select
import random
import time

class GameClient(object):
  def __init__(self, addr="127.0.0.1", serverport=9009):
    self.clientport = random.randrange(8000, 8999)
    self.conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Bind to localhost - set to external ip to connect from other computers
    self.conn.bind(("127.0.0.1", self.clientport))
    self.addr = addr
    self.serverport = serverport
    
    self.read_list = [self.conn]
    self.write_list = []
    
    self.setup_pygame()
  
  def setup_pygame(self, width=400, height=300):
    self.screen = pygame.display.set_mode((width, height))
    self.bg_surface = pygame.image.load("bg.png").convert()
    
    self.image = pygame.image.load("sprite.png").convert_alpha()
    
    pygame.event.set_allowed(None)
    pygame.event.set_allowed([pygame.locals.QUIT,
                              pygame.locals.KEYDOWN])
    pygame.key.set_repeat(50, 50)
    
  def run(self):
    running = True
    clock = pygame.time.Clock()
    tickspeed = 30
    
    try:
      # Initialize connection to server
      self.conn.sendto("c", (self.addr, self.serverport))
      while running:
        clock.tick(tickspeed)
        
        # select on specified file descriptors
        readable, writable, exceptional = (
            select.select(self.read_list, self.write_list, [], 0)
        )
        for f in readable:
          if f is self.conn:
            msg, addr = f.recvfrom(32)
            self.screen.blit(self.bg_surface, (0,0))  # Draw the background
            for position in msg.split('|'):
              x, sep, y = position.partition(',')
              try:
                self.screen.blit(self.image, (int(x), int(y)))
              except:
                pass  # If something goes wrong, don't draw anything.
            

        for event in pygame.event.get():
          if event.type == pygame.QUIT or event.type == pygame.locals.QUIT:
            running = False
            break
          elif event.type == pygame.locals.KEYDOWN:
            if event.key == pygame.locals.K_UP:
              self.conn.sendto("uu", (self.addr, self.serverport))
            elif event.key == pygame.locals.K_DOWN:
              self.conn.sendto("ud", (self.addr, self.serverport))
            elif event.key == pygame.locals.K_LEFT:
              self.conn.sendto("ul", (self.addr, self.serverport))
            elif event.key == pygame.locals.K_RIGHT:
              self.conn.sendto("ur", (self.addr, self.serverport))
            pygame.event.clear(pygame.locals.KEYDOWN)

        pygame.display.update()
    finally:
      self.conn.sendto("d", (self.addr, self.serverport))


if __name__ == "__main__":
  g = GameClient()
  g.run()