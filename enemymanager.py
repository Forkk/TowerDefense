"""
This module handles the spawning of enemies.
"""

import pygame
import enemy



class EnemyManager:

    """
    The event ID for a event to spawn a basic enemy. When a
    basic enemy is scheduled to spawn, an event with this ID
    is posted to the event queue.
    """
    SPAWN_EVENT_BASIC = pygame.USEREVENT

    """
    The time (in milliseconds) at which the last spawning of
    a wave of enemies occurred.
    """
    last_wave_time = 0

    """
    The amount of time between waves.
    """
    wave_interval = 5000

    """
    The number of basic enemies to spawn during a given wave.
    """
    basic_enemies = 1

    """
    The time between spawning two enemies during a wave. This
    is so that enemies don't overlap on the screen.
    """
    spawn_interval = 1000

    """
    The list of enemies in the game.
    """
    enemies = []

    """
    The sprites of all enemies in the game.
    """
    spritegroup = pygame.sprite.Group()

    """
    Whether or not a wave is present.
    """
    wave_present = False

    def __init__(self):
        self.last_wave_time = pygame.time.get_ticks()

    def update(self):
        # Update the enemies
        for enemy in EnemyManager.enemies:
            enemy.update()
            if(enemy.dead()):
                EnemyManager.enemies.remove(enemy)
                enemy.sprite.kill() # Remove the sprite from the sprite group
            
        EnemyManager.current_time = pygame.time.get_ticks()
        # If enough time has passed, spawn a wave
        if(EnemyManager.current_time - EnemyManager.last_wave_time >= EnemyManager.wave_interval):
            # Spawn a wave!
            EnemyManager.wave_present = True
            EnemyManager.last_wave_time = EnemyManager.current_time
        if(EnemyManager.wave_present): # Push the enemies onto the queue as timers
            # Spawn the number of enemies, seperated by a time
            # equal to spawn_interval
            for index in range(0, EnemyManager.basic_enemies):
                # For simplicity, we assume that the time it takes for each of
                # these statements to run is negligible. 
                pygame.time.set_timer(EnemyManager.SPAWN_EVENT_BASIC, EnemyManager.spawn_interval*index)
            # Increase the difficulty!
            EnemyManager.basic_enemies += 1

    """
    Draw all enemies in the game to the screen.
    """
    def draw(self, surface):
        EnemyManager.spritegroup.draw(surface)

    """
    Given a pygame event from the event queue, spawn an enemy (if necessary)
    """
    def spawnEnemy(self, event):
        if(event.type == EnemyManager.SPAWN_EVENT_BASIC):
            EnemyManager.enemies.add(enemy.Enemy())
        

