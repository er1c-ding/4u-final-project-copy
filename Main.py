import World
import Entity
import time

if __name__ == "__main__":
    world = World.World()
    print("Select simulation speed.")
    tick_duration = 1 / float(input("Options: 0.5x speed, 1x speed, 2x speed, 5x speed, 10x speed \n").replace("x speed", ""))

    while tick_duration not in [0.1, 0.2, 0.5, 1, 2]:
        print("Invalid option")
        tick_duration = 1 / float(input("Options: 0.5x speed, 1x speed, 2x speed, 5x speed, 10x speed \n").replace("x speed", ""))

    while True:
        world.run()
        if Entity.Human.get_population() == 0:
            print(f"All humans have died. Civilization survived {world.tick} ticks.")
            break
        time.sleep(tick_duration)