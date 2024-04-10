# loop though a list
import pygame as pg

FPS = 30

clock = pg.time.Clock()

frames = ["frame1", "frame2", "frame3", "frame4"]

# print(len(frames))
current_frame = 0

frames_length = len(frames)

then = 0
# print(frames[frame_length])

# print(current_frame%frames_length)


# write  loop that prints in terminal all frames infinetly
while True:
    # print("One_Piece")
    now = pg.time.get_ticks()
    clock.tick(FPS)
    if now - then > 250:
        print(now)
        then = now
        print(frames[current_frame%frames_length])
        current_frame += 1