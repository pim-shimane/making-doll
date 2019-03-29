#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import pygame


def main():
    pygame.init()
    joys = pygame.joystick.Joystick(0)
    joys.init()

    while True:
            events = pygame.event.get()
            for event in events:
                    if event.type == pygame.JOYBUTTONDOWN or event.type == pygame.JOYHATMOTION:
                            print(event)
            time.sleep(0.1)

if __name__ == '__main__':
    main()
