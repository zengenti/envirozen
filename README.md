# envirozen
Environmental monitoring and control of a room

### Temperature Control for Server Room

This project was initiated using an Arduino to regulate the server room's temperature. It employs two 1.5Kw fans to introduce external ambient air into the room whenever the temperature falls below the (MAX3) threshold. This process creates a positive pressure inside the room, expelling warmer air through specialized vents. The primary objective is to conserve energy on cooler days by leveraging the ambient air, reducing the reliance on air conditioning units when they're not necessary.

As of October 2023 this will developed into Python for deployment onto a more powerful Rasberry Pi

**Started**: October 2022  
**Reason**: Before the cost of electricity started to rise  
**Author**: Nic Kilby

**Component List**

Rasbpberry Pi 4 or better [Raspberry Pi 4 Model B][1]
Enviro Indoor (Pico W Aboard) – Enviro Indoor + Accessory Kit [Enviro Indoor ][2]


[1]: https://www.raspberrypi.com/products/raspberry-pi-4-model-b/
[2]: https://shop.pimoroni.com/products/enviro-indoor?variant=40055644717139
